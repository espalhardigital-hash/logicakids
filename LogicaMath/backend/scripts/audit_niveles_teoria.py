"""
Script de Inspección de niveles_teoria_pool por fase_id (Local vs VPS Prod)
"""

import sys
import os
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def main():
    print("=" * 85)
    print("🔬 INSPECCIÓN DE niveles_teoria_pool POR FASE_ID")
    print("=" * 85)

    loc_env = load_env_file("Datos_localhost/.env.local")
    rem_env = load_env_file("Datos_Producion/.env")

    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    rem_url = rewrite_db_url(rem_env["DATABASE_URL"], "localhost", 5435)

    loc_conn = psycopg2.connect(loc_url)
    rem_conn = psycopg2.connect(rem_url)

    cur_l = loc_conn.cursor()
    cur_r = rem_conn.cursor()

    print("\n--- RECUENTO DE TEORÍA POR FASE EN LOCAL ---")
    cur_l.execute("SELECT fase_id, COUNT(*), MIN(titulo) FROM niveles_teoria_pool GROUP BY fase_id ORDER BY fase_id;")
    for r in cur_l.fetchall():
        print(f"  Fase {r[0]:<2}: {r[1]:<3} niveles | Ejemplo: '{r[2]}'")

    print("\n--- RECUENTO DE TEORÍA POR FASE EN VPS PROD ---")
    cur_r.execute("SELECT fase_id, COUNT(*), MIN(titulo) FROM niveles_teoria_pool GROUP BY fase_id ORDER BY fase_id;")
    for r in cur_r.fetchall():
        print(f"  Fase {r[0]:<2}: {r[1]:<3} niveles | Ejemplo: '{r[2]}'")

    print("\n--- DETALLE DE TEORÍA FASE 5 Y FASE 6 EN LOCAL ---")
    cur_l.execute("SELECT fase_id, modulo_id, nivel_id, titulo FROM niveles_teoria_pool WHERE fase_id IN (5, 6) ORDER BY fase_id, modulo_id, nivel_id;")
    for r in cur_l.fetchall():
        print(f"  Local - Fase {r[0]} Mód {r[1]} Niv {r[2]}: {r[3]}")

    print("\n--- DETALLE DE TEORÍA FASE 5 Y FASE 6 EN VPS PROD ---")
    cur_r.execute("SELECT fase_id, modulo_id, nivel_id, titulo FROM niveles_teoria_pool WHERE fase_id IN (5, 6) ORDER BY fase_id, modulo_id, nivel_id;")
    for r in cur_r.fetchall():
        print(f"  VPS Prod - Fase {r[0]} Mód {r[1]} Niv {r[2]}: {r[3]}")

    loc_conn.close()
    rem_conn.close()

if __name__ == "__main__":
    main()
