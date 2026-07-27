"""
Script de Auditoría de las Tablas de Teoría (Local vs VPS Prod)
"""

import sys
import os
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def main():
    print("=" * 85)
    print("🔬 AUDITORÍA DE TABLAS DE TEORÍA: LOCAL vs VPS PROD")
    print("=" * 85)

    loc_env = load_env_file("Datos_localhost/.env.local")
    rem_env = load_env_file("Datos_Producion/.env")

    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    rem_url = rewrite_db_url(rem_env["DATABASE_URL"], "localhost", 5435)

    loc_conn = psycopg2.connect(loc_url)
    rem_conn = psycopg2.connect(rem_url)

    cur_l = loc_conn.cursor()
    cur_r = rem_conn.cursor()

    cur_l.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    loc_tables = set(r[0] for r in cur_l.fetchall())

    cur_r.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    rem_tables = set(r[0] for r in cur_r.fetchall())

    print(f"[*] Tablas en Local: {sorted(list(loc_tables))}")
    print(f"[*] Tablas en VPS Prod: {sorted(list(rem_tables))}")

    # Buscar tablas con 'teoria' o 'nivel' o 'lectura'
    theory_tables = [t for t in loc_tables if 'teor' in t or 'nivel' in t or 'lectur' in t or 'fase' in t]
    print(f"[*] Tablas relacionadas con teoría/niveles en Local: {theory_tables}")

    for t in theory_tables:
        if t in loc_tables and t in rem_tables:
            cur_l.execute(f"SELECT COUNT(*) FROM {t};")
            cl = cur_l.fetchone()[0]
            cur_r.execute(f"SELECT COUNT(*) FROM {t};")
            cr = cur_r.fetchone()[0]
            print(f"  • {t:<30}: Local = {cl:<6} | VPS Prod = {cr:<6}")

    loc_conn.close()
    rem_conn.close()

if __name__ == "__main__":
    main()
