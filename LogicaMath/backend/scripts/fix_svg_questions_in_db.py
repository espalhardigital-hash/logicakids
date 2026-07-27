"""
Script para Corregir y Limpiar Etiquetas SVG en la Base de Datos (Local)
Sustituye 'width=320 height=320' por atributos proporcionales y responsivos sin duplicidad.
"""

import sys
import os
import psycopg2
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def fix_db(conn, db_name):
    cur = conn.cursor()
    
    cur.execute("SELECT id, enunciado FROM preguntas WHERE enunciado LIKE '%<svg%';")
    rows = cur.fetchall()
    print(f"[*] {db_name}: Analizando {len(rows)} preguntas con SVG...")

    updated_count = 0
    for q_id, text in rows:
        if "width='320' height='320'" in text or 'width="320" height="320"' in text or "style='margin:10px auto" in text:
            # Reemplazar etiqueta svg completa
            fixed_text = re.sub(
                r"<svg\s+[^>]*viewBox=['\"]0 68 200 64['\"][^>]*>",
                r"<svg viewBox='0 68 200 64' style='margin:10px auto; display:block; width:100%; max-width:320px; height:auto; background:#111827; border:2px solid #8B5CF6; border-radius:14px;'>",
                text
            )
            if fixed_text != text:
                cur.execute("UPDATE preguntas SET enunciado = %s WHERE id = %s;", (fixed_text, q_id))
                updated_count += 1

    conn.commit()
    print(f"  ✓ {db_name}: {updated_count} preguntas actualizadas y limpiadas con éxito.")

def main():
    print("=" * 85)
    print("🚀 LIMPIANDO Y REPARANDO ETIQUETAS SVG EN PREGUNTAS")
    print("=" * 85)

    loc_env = load_env_file("Datos_localhost/.env.local")
    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    loc_conn = psycopg2.connect(loc_url)

    fix_db(loc_conn, "LOCAL DB (5433)")
    loc_conn.close()

if __name__ == "__main__":
    main()
