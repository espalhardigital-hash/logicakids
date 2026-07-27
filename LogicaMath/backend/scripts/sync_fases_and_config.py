"""
Script de Sincronización de Fases y Configuración de Progreso (Local -> VPS Prod)
Sincroniza la tabla 'fases' (12 fases) y 'configuracion_progreso' (208 configuraciones).
"""

import sys
import os
import psycopg2
from psycopg2.extras import execute_values

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def main():
    print("=" * 80)
    print("🚀 SINCRONIZANDO TABLAS FASES Y CONFIGURACIÓN DE PROGRESO (LOCAL -> VPS PROD)")
    print("=" * 80)

    loc_env = load_env_file("Datos_localhost/.env.local")
    rem_env = load_env_file("Datos_Producion/.env")

    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    rem_url = rewrite_db_url(rem_env["DATABASE_URL"], "localhost", 5435)

    loc_conn = psycopg2.connect(loc_url)
    rem_conn = psycopg2.connect(rem_url)

    loc_cur = loc_conn.cursor()
    rem_cur = rem_conn.cursor()

    # 1. Sincronizar FASES
    loc_cur.execute("""
        SELECT id, nombre, descripcion, orden, estado, fecha_creacion, ultima_modificacion 
        FROM fases 
        ORDER BY id;
    """)
    fases_rows = loc_cur.fetchall()
    print(f"[*] Fases locales encontradas: {len(fases_rows)}")

    upsert_fases_sql = """
        INSERT INTO fases (id, nombre, descripcion, orden, estado, fecha_creacion, ultima_modificacion)
        VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            nombre = EXCLUDED.nombre,
            descripcion = EXCLUDED.descripcion,
            orden = EXCLUDED.orden,
            estado = EXCLUDED.estado,
            fecha_creacion = EXCLUDED.fecha_creacion,
            ultima_modificacion = EXCLUDED.ultima_modificacion;
    """
    execute_values(rem_cur, upsert_fases_sql, fases_rows)
    rem_conn.commit()
    print(f"  ✓ {len(fases_rows)} Fases sincronizadas/upsertadas exitosamente en VPS Prod.")

    # 2. Sincronizar CONFIGURACION_PROGRESO
    loc_cur.execute("""
        SELECT id, fase_id, seccion, operacion, cantidad_requerida, porcentaje_aprobacion, 
               orden_desbloqueo, tipo_feedback, usa_cronometro, tiempo_default_segundos, 
               activo, fecha_creacion, ultima_modificacion, errores_tolerados, 
               pistas_permitidas, penalizacion_pista_segundos
        FROM configuracion_progreso
        ORDER BY id;
    """)
    config_rows = loc_cur.fetchall()
    print(f"[*] Configuraciones de progreso locales encontradas: {len(config_rows)}")

    # Truncar tabla configuracion_progreso en VPS Prod para paridad exacta 100% de 208 filas
    rem_cur.execute("TRUNCATE TABLE configuracion_progreso RESTART IDENTITY CASCADE;")

    insert_config_sql = """
        INSERT INTO configuracion_progreso (
            id, fase_id, seccion, operacion, cantidad_requerida, porcentaje_aprobacion, 
            orden_desbloqueo, tipo_feedback, usa_cronometro, tiempo_default_segundos, 
            activo, fecha_creacion, ultima_modificacion, errores_tolerados, 
            pistas_permitidas, penalizacion_pista_segundos
        ) VALUES %s;
    """
    execute_values(rem_cur, insert_config_sql, config_rows)
    rem_conn.commit()
    print(f"  ✓ {len(config_rows)} Configuraciones de progreso sincronizadas exitosamente en VPS Prod.")

    # Ajustar secuencias
    rem_cur.execute("SELECT setval('fases_id_seq', (SELECT MAX(id) FROM fases));")
    rem_cur.execute("SELECT setval('configuracion_progreso_id_seq', (SELECT MAX(id) FROM configuracion_progreso));")
    rem_conn.commit()

    print("=" * 80)
    print("✅ SINCRONIZACIÓN DE FASES Y CONFIGURACIÓN COMPLETADA")
    print("=" * 80)

    loc_conn.close()
    rem_conn.close()

if __name__ == "__main__":
    main()
