"""
Script de Auditoría Profunda de Base de Datos (Local vs VPS Prod)
Basado en las reglas de RULES AGENTES/deep_analise_pro.md §12 y §15
"""

import sys
import os
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def main():
    print("=" * 85)
    print("🔬 AUDITORÍA PROFUNDA DE BASE DE DATOS: LOCAL (5433) vs VPS PROD (5435)")
    print("=" * 85)

    loc_env = load_env_file("Datos_localhost/.env.local")
    rem_env = load_env_file("Datos_Producion/.env")

    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    rem_url = rewrite_db_url(rem_env["DATABASE_URL"], "localhost", 5435)

    loc_conn = psycopg2.connect(loc_url)
    rem_conn = psycopg2.connect(rem_url)

    cur_l = loc_conn.cursor()
    cur_r = rem_conn.cursor()

    # 1. Conteo de Tablas Principales
    tables = [
        'fases', 'preguntas', 'alternativas', 'alumnos', 'users', 
        'progreso_maestria', 'configuracion_progreso', 'pool_asignado_alumno', 
        'intentos', 'alembic_version'
    ]

    print("\n--- 1. CONTEO DE REGISTROS POR TABLA ---")
    header = f"{'Tabla':<25} | {'Local (5433)':<15} | {'VPS Prod (5435)':<15} | {'Estado':<20}"
    print(header)
    print("-" * len(header))

    for t in tables:
        cur_l.execute(f"SELECT COUNT(*) FROM {t};")
        c_l = cur_l.fetchone()[0]
        cur_r.execute(f"SELECT COUNT(*) FROM {t};")
        c_r = cur_r.fetchone()[0]

        if c_l == c_r:
            st = "✅ PARIDAD 100%"
        elif t in ['alumnos', 'users', 'intentos', 'progreso_maestria', 'pool_asignado_alumno']:
            st = "🟢 PROD PRESERVADO"
        else:
            st = f"⚠️ DIFERENCIA ({c_l - c_r})"

        print(f"{t:<25} | {c_l:<15} | {c_r:<15} | {st:<20}")

    # 2. Desglose de Preguntas por Fase ID
    print("\n--- 2. DESGLOSE DE PREGUNTAS POR FASE_ID ---")
    header_f = f"{'fase_id':<10} | {'Nombre Fase':<35} | {'Local':<12} | {'VPS Prod':<12} | {'Paridad':<12}"
    print(header_f)
    print("-" * len(header_f))

    # Nombres de fases
    cur_l.execute("SELECT id, nombre FROM fases ORDER BY id;")
    fase_names = dict(cur_l.fetchall())

    cur_l.execute("SELECT fase_id, COUNT(*) FROM preguntas GROUP BY fase_id ORDER BY fase_id;")
    loc_fases = dict(cur_l.fetchall())

    cur_r.execute("SELECT fase_id, COUNT(*) FROM preguntas GROUP BY fase_id ORDER BY fase_id;")
    rem_fases = dict(cur_r.fetchall())

    all_fases = sorted(set(list(loc_fases.keys()) + list(rem_fases.keys())))
    for f in all_fases:
        name = fase_names.get(f, f"Fase {f}")
        fl = loc_fases.get(f, 0)
        fr = rem_fases.get(f, 0)
        st_f = "✅ 100%" if fl == fr else f"❌ ({fl - fr})"
        print(f"{f:<10} | {name:<35} | {fl:<12} | {fr:<12} | {st_f:<12}")

    # 3. Verificación de URLs de MinIO en Enunciados
    print("\n--- 3. VERIFICACIÓN DE DOMINIOS DE IMÁGENES MINIO EN PREGUNTAS ---")
    cur_l.execute("SELECT COUNT(*) FROM preguntas WHERE enunciado LIKE '%http://localhost:9100/logicakids%';")
    loc_local_urls = cur_l.fetchone()[0]

    cur_r.execute("SELECT COUNT(*) FROM preguntas WHERE enunciado LIKE '%https://files.espalhar.shop/logicakids-producion%';")
    rem_prod_urls = cur_r.fetchone()[0]

    cur_r.execute("SELECT COUNT(*) FROM preguntas WHERE enunciado LIKE '%http://localhost%';")
    rem_dev_urls = cur_r.fetchone()[0]

    print(f"  • Local: Preguntas con URL local (http://localhost:9100): {loc_local_urls}")
    print(f"  • VPS Prod: Preguntas con URL de CDN Producción (https://files.espalhar.shop): {rem_prod_urls}")
    print(f"  • VPS Prod: Preguntas con URL dev errónea (localhost): {rem_dev_urls} {'✅ (0 OK)' if rem_dev_urls == 0 else '❌ ALERTA'}")

    # 4. Verificación de Revisión Alembic
    print("\n--- 4. ESTADO DE MIGRACIONES ALEMBIC ---")
    cur_l.execute("SELECT version_num FROM alembic_version;")
    loc_alembic = cur_l.fetchone()[0]

    cur_r.execute("SELECT version_num FROM alembic_version;")
    rem_alembic = cur_r.fetchone()[0]

    print(f"  • Local Alembic Head: {loc_alembic}")
    print(f"  • VPS Prod Alembic Head: {rem_alembic}")
    print(f"  • Paridad Alembic: {'✅ Sincronizado' if loc_alembic == rem_alembic else '❌ Desalineado'}")

    # 5. Verificación de Esquema (Columna override_motivo)
    print("\n--- 5. VERIFICACIÓN DE COLUMNA OVERRIDE_MOTIVO EN PROGRESO_MAESTRIA ---")
    cur_l.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'progreso_maestria' AND column_name = 'override_motivo';
    """)
    loc_col = cur_l.fetchone()

    cur_r.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'progreso_maestria' AND column_name = 'override_motivo';
    """)
    rem_col = cur_r.fetchone()

    print(f"  • Local: {loc_col}")
    print(f"  • VPS Prod: {rem_col}")
    print(f"  • Paridad Columna: {'✅ Presente en ambos' if loc_col and rem_col else '❌ Faltante'}")

    print("=" * 85)
    print("✅ FIN DE LA AUDITORÍA PROFUNDA")
    print("=" * 85)

    loc_conn.close()
    rem_conn.close()

if __name__ == "__main__":
    main()
