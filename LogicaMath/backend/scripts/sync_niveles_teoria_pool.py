"""
Script de Sustitución y Sincronización Completa de la Tabla niveles_teoria_pool (Local -> VPS Prod)
Resuelve la desalineación de teoría entre Fases (Operatoria Decimal en Fase 5, Geometría en Fase 6).
"""

import sys
import os
import json
import psycopg2
from psycopg2.extras import execute_values

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def prepare_val(val):
    if isinstance(val, (dict, list)):
        return json.dumps(val)
    return val

def get_connections():
    loc_env = load_env_file("Datos_localhost/.env.local")
    rem_env = load_env_file("Datos_Producion/.env")

    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    rem_url = rewrite_db_url(rem_env["DATABASE_URL"], "localhost", 5435)

    return psycopg2.connect(loc_url), psycopg2.connect(rem_url)

def main():
    print("=" * 85)
    print("🚀 SINCRONIZANDO TABLA niveles_teoria_pool (LOCAL -> VPS PROD)")
    print("=" * 85)

    loc_conn, rem_conn = get_connections()
    loc_cur = loc_conn.cursor()
    rem_cur = rem_conn.cursor()

    # Mapeo de usuarios por email para revisado_por
    loc_cur.execute("SELECT id, email FROM users;")
    loc_users = {r[0]: r[1] for r in loc_cur.fetchall()}

    rem_cur.execute("SELECT id, email FROM users;")
    rem_users_by_email = {r[1]: r[0] for r in rem_cur.fetchall()}
    rem_user_ids = set(rem_users_by_email.values())

    user_id_map = {}
    for loc_id, email in loc_users.items():
        if email in rem_users_by_email:
            user_id_map[loc_id] = rem_users_by_email[email]
        else:
            user_id_map[loc_id] = None

    def map_user(uid):
        if not uid:
            return None
        if uid in rem_user_ids:
            return uid
        return user_id_map.get(uid, None)

    # 1. Eliminar teoría en VPS Prod para reemplazo completo por la versión de Desarrollo Local
    rem_cur.execute("TRUNCATE TABLE niveles_teoria_pool RESTART IDENTITY CASCADE;")
    rem_conn.commit()
    print("  ✓ Tabla niveles_teoria_pool truncada limpiamente en VPS Prod.")

    # 2. Obtener todas las filas de teoría de Local DB
    loc_cur.execute("""
        SELECT id, fase_id, modulo_id, nivel_id, titulo, texto_descubrimiento, 
               diccionario, advertencia, ejemplos, interactivos, revisado_admin, 
               revisado_por, fecha_revision
        FROM niveles_teoria_pool
        ORDER BY id;
    """)
    rows = loc_cur.fetchall()
    total_local = len(rows)
    print(f"[*] Filas de teoría locales encontradas: {total_local}")

    processed_rows = []
    for r in rows:
        r_list = list(r)
        
        # Mapear usuario revisado_por (idx 11)
        r_list[11] = map_user(r_list[11])

        processed_rows.append(tuple(prepare_val(v) for v in r_list))

    # 3. Insertar las 134 filas de teoría locales en VPS Prod
    insert_sql = """
        INSERT INTO niveles_teoria_pool (
            id, fase_id, modulo_id, nivel_id, titulo, texto_descubrimiento, 
            diccionario, advertencia, ejemplos, interactivos, revisado_admin, 
            revisado_por, fecha_revision
        ) VALUES %s;
    """
    execute_values(rem_cur, insert_sql, processed_rows)
    rem_conn.commit()

    # Ajustar secuencia
    rem_cur.execute("SELECT setval('niveles_teoria_pool_id_seq', (SELECT MAX(id) FROM niveles_teoria_pool));")
    rem_conn.commit()

    # 4. Verificar paridad por Fase ID
    print("\n--- RECUENTO DE TEORÍA POR FASE TRAS LA SINCRONIZACIÓN ---")
    rem_cur.execute("SELECT fase_id, COUNT(*), MIN(titulo) FROM niveles_teoria_pool GROUP BY fase_id ORDER BY fase_id;")
    for r in rem_cur.fetchall():
        print(f"  VPS Prod - Fase {r[0]:<2}: {r[1]:<3} niveles | Ejemplo: '{r[2]}'")

    print("=" * 85)
    print(f"✅ TABLA niveles_teoria_pool SINCRONIZADA CON ÉXITO ({total_local} REGISTROS)")
    print("=" * 85)

    loc_conn.close()
    rem_conn.close()

if __name__ == "__main__":
    main()
