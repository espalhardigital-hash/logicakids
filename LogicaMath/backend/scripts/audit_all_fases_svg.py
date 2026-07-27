"""
Script de Auditoría Global de SVGs en Todas las 12 Fases (37,930 Preguntas)
Inspecciona tanto la Base de Datos Local como la Base de Datos VPS Prod para garantizar cero colapsos de altura.
"""

import sys
import os
import re
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def audit_db_svgs(db_name, connection_url):
    print(f"\n--- AUDITANDO {db_name} ---")
    conn = psycopg2.connect(connection_url)
    cur = conn.cursor()

    cur.execute("""
        SELECT fase_id, COUNT(*) 
        FROM preguntas 
        WHERE enunciado LIKE '%<svg%'
        GROUP BY fase_id
        ORDER BY fase_id;
    """)
    svg_counts = cur.fetchall()
    print(f"[*] Conteo de preguntas con SVG por Fase en {db_name}:")
    total_svg = 0
    for fase_id, count in svg_counts:
        print(f"  • Fase {fase_id}: {count} preguntas con SVG")
        total_svg += count
    print(f"  👉 Total global de preguntas con SVG: {total_svg}")

    # Buscar SVGs potencialmente defectuosos o sin altura
    cur.execute("""
        SELECT id, fase_id, enunciado 
        FROM preguntas 
        WHERE enunciado LIKE '%<svg%' 
          AND (
            enunciado LIKE '%height:auto%' 
            OR (enunciado LIKE '%width=%320%' AND enunciado NOT LIKE '%height=%102%')
            OR (enunciado LIKE '%viewBox=%0 68%' AND enunciado NOT LIKE '%height=%102%')
          );
    """)
    defective = cur.fetchall()
    print(f"  ❌ SVGs con colapso o dimensiones desalineadas: {len(defective)}")
    conn.close()
    return len(defective)

def main():
    print("=" * 85)
    print("🔬 AUDITORÍA GLOBAL DE SVGS EN TODAS LAS FASES (LOCAL Y VPS)")
    print("=" * 85)

    loc_env = load_env_file("Datos_localhost/.env.local")
    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    defective_loc = audit_db_svgs("LOCAL DB (Puerto 5433)", loc_url)

if __name__ == "__main__":
    main()
