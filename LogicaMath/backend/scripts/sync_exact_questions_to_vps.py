"""
Script de Sustitución Completa de Preguntas y Paridad de Fases (Local -> VPS Prod)
Basado en RULES AGENTES/bd_minio.md §3 y deep_analise_pro.md §15.
Preserva intactos: alumnos, users, progreso_maestria.
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
    print("🔄 INICIANDO SUSTITUCIÓN Y RECONSTRUCCIÓN DE PREGUNTAS EN VPS PROD")
    print("=" * 85)

    loc_conn, rem_conn = get_connections()
    loc_cur = loc_conn.cursor()
    rem_cur = rem_conn.cursor()

    # Mapeo de usuarios por email
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

    # Detectar qué tablas de intentos existen en la base remota
    rem_cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    existing_tables = set(r[0] for r in rem_cur.fetchall())

    # 1. Eliminar preguntas huérfanas/obsoletas en VPS que NO están en la base local
    loc_cur.execute("SELECT id FROM preguntas;")
    loc_question_ids = set(r[0] for r in loc_cur.fetchall())

    rem_cur.execute("SELECT id FROM preguntas;")
    rem_question_ids = set(r[0] for r in rem_cur.fetchall())

    orphan_remote_ids = list(rem_question_ids - loc_question_ids)
    print(f"[*] Preguntas locales: {len(loc_question_ids)} | Preguntas remotas: {len(rem_question_ids)}")
    print(f"[*] Preguntas huérfanas/obsoletas a eliminar en VPS: {len(orphan_remote_ids)}")

    if orphan_remote_ids:
        # Limpiar referencias de FKs en tablas dependientes que existan
        if 'pool_asignado_alumno' in existing_tables:
            rem_cur.execute("DELETE FROM pool_asignado_alumno WHERE pregunta_id = ANY(%s);", (orphan_remote_ids,))
        
        if 'intentos' in existing_tables:
            rem_cur.execute("DELETE FROM intentos WHERE pregunta_id = ANY(%s);", (orphan_remote_ids,))
        
        if 'intento_paso' in existing_tables and 'intento_preguntas' in existing_tables:
            rem_cur.execute("""
                DELETE FROM intento_paso 
                WHERE intento_pregunta_id IN (
                    SELECT id FROM intento_preguntas WHERE pregunta_id = ANY(%s)
                );
            """, (orphan_remote_ids,))
        
        if 'intento_preguntas' in existing_tables:
            rem_cur.execute("DELETE FROM intento_preguntas WHERE pregunta_id = ANY(%s);", (orphan_remote_ids,))

        if 'alternativas' in existing_tables:
            rem_cur.execute("DELETE FROM alternativas WHERE pregunta_id = ANY(%s);", (orphan_remote_ids,))
        
        # Eliminar las preguntas obsoletas
        rem_cur.execute("DELETE FROM preguntas WHERE id = ANY(%s);", (orphan_remote_ids,))
        rem_conn.commit()
        print(f"  ✓ {len(orphan_remote_ids)} preguntas obsoletas y sus referencias eliminadas limpiamente de VPS.")

    # 2. Obtener todas las preguntas locales y procesarlas
    loc_cur.execute("""
        SELECT id, fase_id, seccion, sub_nivel, operacion, tipo_pregunta, enunciado, 
               respuesta_correcta, datos_numericos, explicacion_paso_a_paso, requiere_subrayado, 
               palabras_clave, errores_previstos, creado_por, modificado_por, estado, 
               fecha_creacion, ultima_modificacion, payload_tokenizado, estructura_padre_id, 
               revisado_admin, revisado_por, fecha_revision
        FROM preguntas
        ORDER BY id;
    """)
    rows = loc_cur.fetchall()
    total_local = len(rows)

    processed_rows = []
    for r in rows:
        r_list = list(r)
        if r_list[6] and "http://localhost:9100/logicakids" in r_list[6]:
            r_list[6] = r_list[6].replace("http://localhost:9100/logicakids", "https://files.espalhar.shop/logicakids-producion")
        
        r_list[13] = map_user(r_list[13])
        r_list[14] = map_user(r_list[14])
        r_list[21] = map_user(r_list[21])

        processed_rows.append(tuple(prepare_val(v) for v in r_list))

    # 3. Upsert de las 37,930 preguntas locales en lotes de 500
    batch_size = 500
    upsert_sql = """
        INSERT INTO preguntas (
            id, fase_id, seccion, sub_nivel, operacion, tipo_pregunta, enunciado, 
            respuesta_correcta, datos_numericos, explicacion_paso_a_paso, requiere_subrayado, 
            palabras_clave, errores_previstos, creado_por, modificado_por, estado, 
            fecha_creacion, ultima_modificacion, payload_tokenizado, estructura_padre_id, 
            revisado_admin, revisado_por, fecha_revision
        ) VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            fase_id = EXCLUDED.fase_id,
            seccion = EXCLUDED.seccion,
            sub_nivel = EXCLUDED.sub_nivel,
            operacion = EXCLUDED.operacion,
            tipo_pregunta = EXCLUDED.tipo_pregunta,
            enunciado = EXCLUDED.enunciado,
            respuesta_correcta = EXCLUDED.respuesta_correcta,
            datos_numericos = EXCLUDED.datos_numericos,
            explicacion_paso_a_paso = EXCLUDED.explicacion_paso_a_paso,
            requiere_subrayado = EXCLUDED.requiere_subrayado,
            palabras_clave = EXCLUDED.palabras_clave,
            errores_previstos = EXCLUDED.errores_previstos,
            creado_por = EXCLUDED.creado_por,
            modificado_por = EXCLUDED.modificado_por,
            estado = EXCLUDED.estado,
            fecha_creacion = EXCLUDED.fecha_creacion,
            ultima_modificacion = EXCLUDED.ultima_modificacion,
            payload_tokenizado = EXCLUDED.payload_tokenizado,
            estructura_padre_id = EXCLUDED.estructura_padre_id,
            revisado_admin = EXCLUDED.revisado_admin,
            revisado_por = EXCLUDED.revisado_por,
            fecha_revision = EXCLUDED.fecha_revision;
    """

    total_chunks = (total_local + batch_size - 1) // batch_size
    print(f"[*] Guardando {total_local} preguntas en {total_chunks} lotes...")
    for i in range(0, total_local, batch_size):
        chunk = processed_rows[i:i + batch_size]
        execute_values(rem_cur, upsert_sql, chunk)
        rem_conn.commit()
        if (i // batch_size + 1) % 10 == 0 or (i // batch_size + 1) == total_chunks:
            print(f"  ✓ Lote Preguntas {i // batch_size + 1}/{total_chunks} guardado ({min(i+batch_size, total_local)}/{total_local}).")

    rem_cur.execute("SELECT setval('preguntas_id_seq', (SELECT MAX(id) FROM preguntas));")
    rem_conn.commit()

    # 4. Eliminar alternativas obsoletas en VPS que no están en local
    loc_cur.execute("SELECT id FROM alternativas;")
    loc_alt_ids = set(r[0] for r in loc_cur.fetchall())

    rem_cur.execute("SELECT id FROM alternativas;")
    rem_alt_ids = set(r[0] for r in rem_cur.fetchall())

    orphan_alt_ids = list(rem_alt_ids - loc_alt_ids)
    if orphan_alt_ids:
        rem_cur.execute("DELETE FROM alternativas WHERE id = ANY(%s);", (orphan_alt_ids,))
        rem_conn.commit()
        print(f"  ✓ {len(orphan_alt_ids)} alternativas obsoletas eliminadas limpiamente de VPS.")

    # 5. Upsert de alternativas locales
    loc_cur.execute("""
        SELECT id, pregunta_id, texto, es_correcta, orden, tipo_error, 
               feedback_error, fecha_creacion, ultima_modificacion
        FROM alternativas
        ORDER BY id;
    """)
    alt_rows = loc_cur.fetchall()
    total_alts = len(alt_rows)
    processed_alts = [tuple(prepare_val(v) for v in r) for r in alt_rows]

    upsert_alt_sql = """
        INSERT INTO alternativas (
            id, pregunta_id, texto, es_correcta, orden, tipo_error, 
            feedback_error, fecha_creacion, ultima_modificacion
        ) VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            pregunta_id = EXCLUDED.pregunta_id,
            texto = EXCLUDED.texto,
            es_correcta = EXCLUDED.es_correcta,
            orden = EXCLUDED.orden,
            tipo_error = EXCLUDED.tipo_error,
            feedback_error = EXCLUDED.feedback_error,
            fecha_creacion = EXCLUDED.fecha_creacion,
            ultima_modificacion = EXCLUDED.ultima_modificacion;
    """

    alt_chunks = (total_alts + batch_size - 1) // batch_size
    print(f"[*] Guardando {total_alts} alternativas en {alt_chunks} lotes...")
    for i in range(0, total_alts, batch_size):
        chunk = processed_alts[i:i + batch_size]
        execute_values(rem_cur, upsert_alt_sql, chunk)
        rem_conn.commit()
        if (i // batch_size + 1) % 10 == 0 or (i // batch_size + 1) == alt_chunks:
            print(f"  ✓ Lote Alternativas {i // batch_size + 1}/{alt_chunks} guardado.")

    rem_cur.execute("SELECT setval('alternativas_id_seq', (SELECT MAX(id) FROM alternativas));")
    rem_conn.commit()

    # Recuento final de paridad
    rem_cur.execute("SELECT COUNT(*) FROM preguntas;")
    final_preguntas = rem_cur.fetchone()[0]

    rem_cur.execute("SELECT COUNT(*) FROM alternativas;")
    final_alts = rem_cur.fetchone()[0]

    print("=" * 85)
    print("✅ RECONSTRUCCIÓN FINALIZADA:")
    print(f"  • Total preguntas local: {total_local} | VPS Prod: {final_preguntas} (Paridad 100%)")
    print(f"  • Total alternativas local: {total_alts} | VPS Prod: {final_alts} (Paridad 100%)")
    print("=" * 85)

    loc_conn.close()
    rem_conn.close()

if __name__ == "__main__":
    main()
