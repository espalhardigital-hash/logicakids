"""
Script para Reparar Masivamente y de Forma Definitiva las Etiquetas SVG de la Fase 5 (Local DB)
Asegura width="100%", height="102", min-height="102px" y aspect-ratio para evitar colapso a 0px en navegadores.
"""

import sys
import os
import re
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def fix_svg_enunciado(text):
    if not text or '<svg' not in text:
        return text

    # Reparar SVGs de tablas de montos con viewBox 200x64 o 200x86
    fixed = re.sub(
        r'<svg[^>]*viewBox=["\']0 (?:68|57) 200 (?:64|86)["\'][^>]*>',
        r'<svg viewBox="0 68 200 64" width="100%" height="102" style="margin:10px auto; display:block; width:100%; max-width:320px; height:102px; min-height:102px; aspect-ratio:200/64; background:#111827; border:2px solid #8B5CF6; border-radius:14px;">',
        text,
        flags=re.IGNORECASE
    )

    # Reparar cualquier otro SVG sin height explícito en la base de datos
    fixed = re.sub(
        r'<svg\s+width=["\']320["\']\s+height=["\']320["\'][^>]*>',
        r'<svg width="100%" height="150" style="margin:10px auto; display:block; width:100%; max-width:320px; height:150px; min-height:100px; background:#111827; border:2px solid #8B5CF6; border-radius:14px;">',
        fixed,
        flags=re.IGNORECASE
    )

    return fixed

def main():
    print("=" * 85)
    print("🚀 APLICANDO REPARACIÓN DEFINITIVA DE SVGS EN FASE 5 (LOCAL DB)")
    print("=" * 85)

    loc_env = load_env_file("Datos_localhost/.env.local")
    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    loc_conn = psycopg2.connect(loc_url)
    cur = loc_conn.cursor()

    cur.execute("""
        SELECT id, enunciado 
        FROM preguntas 
        WHERE fase_id = 5 AND enunciado LIKE '%<svg%';
    """)
    rows = cur.fetchall()
    print(f"[*] Analizando {len(rows)} preguntas con SVG en Fase 5...")

    updated_count = 0
    for q_id, text in rows:
        fixed_text = fix_svg_enunciado(text)
        if fixed_text != text:
            cur.execute("UPDATE preguntas SET enunciado = %s WHERE id = %s;", (fixed_text, q_id))
            updated_count += 1

    loc_conn.commit()
    print(f"  ✓ {updated_count} preguntas de la Fase 5 actualizadas con dimensiones e inercia CSS (height: 102px, min-height: 102px).")

    loc_conn.close()

if __name__ == "__main__":
    main()
