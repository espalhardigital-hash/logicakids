"""
Script para Inspeccionar y Reparar SVGs en Preguntas de la Base de Datos
"""

import sys
import os
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def main():
    print("=" * 85)
    print("🔬 INSPECCIONANDO Y CORRIGIENDO ETIQUETAS SVG EN PREGUNTAS")
    print("=" * 85)

    loc_env = load_env_file("Datos_localhost/.env.local")
    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    loc_conn = psycopg2.connect(loc_url)
    cur = loc_conn.cursor()

    cur.execute("SELECT COUNT(*) FROM preguntas WHERE enunciado LIKE '%<svg%';")
    total_svg = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM preguntas WHERE enunciado LIKE '%width=''320'' height=''320'' viewBox=''0 68 200 64''%';")
    total_distorted = cur.fetchone()[0]

    print(f"[*] Total preguntas con SVG: {total_svg}")
    print(f"[*] Total preguntas con SVG distorsionado (320x320 con viewBox 200x64): {total_distorted}")

    # Mostrar ejemplos antes de la corrección
    cur.execute("SELECT id, fase_id, seccion, enunciado FROM preguntas WHERE enunciado LIKE '%width=''320'' height=''320'' viewBox=''0 68 200 64''%' LIMIT 3;")
    rows = cur.fetchall()
    print("\n--- EJEMPLOS ANTES DE CORREGIR ---")
    for r in rows:
        print(f"\nID: {r[0]} | Fase: {r[1]} | Sección: {r[2]}")
        print(f"Enunciado:\n{r[3][:250]}...")

    loc_conn.close()

if __name__ == "__main__":
    main()
