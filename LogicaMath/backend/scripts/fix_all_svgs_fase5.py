"""
Script para Corregir y Limpiar Masivamente Todas las Etiquetas SVG de la Fase 5 (Local DB)
Transforma atributos width/height fijos (320x320) a dimensiones responsivas y proporcionales (height: auto, max-width: 320px).
"""

import sys
import os
import re
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def clean_svg_tag(match):
    full_tag = match.group(0)

    # Extraer viewBox si existe
    vb_match = re.search(r'viewBox=["\']([^"\']+)["\']', full_tag)
    viewbox_attr = f'viewBox="{vb_match.group(1)}"' if vb_match else ''

    # Extraer border/background style si existe
    style_match = re.search(r'style=["\']([^"\']+)["\']', full_tag)
    custom_style = ""
    if style_match:
        existing_style = style_match.group(1)
        # Remover width y height del style existente si los hay
        existing_style = re.sub(r'width:[^;]+;?', '', existing_style)
        existing_style = re.sub(r'height:[^;]+;?', '', existing_style)
        custom_style = existing_style.strip()

    if not custom_style:
        custom_style = "margin:10px auto; display:block; background:#111827; border:2px solid #8B5CF6; border-radius:14px;"
    else:
        if "margin" not in custom_style:
            custom_style += " margin:10px auto;"
        if "display" not in custom_style:
            custom_style += " display:block;"

    # Asegurar width 100%, max-width 320px, height auto
    final_style = f"width:100%; max-width:320px; height:auto; {custom_style}".strip()

    return f'<svg {viewbox_attr} style="{final_style}">'

def main():
    print("=" * 85)
    print("🚀 CORRIGIENDO MASIVAMENTE LAS 3,520 ETIQUETAS SVG EN LA FASE 5 (LOCAL DB)")
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
    svg_pattern = re.compile(r'<svg\s+[^>]*>', re.IGNORECASE)

    for q_id, text in rows:
        if 'width=' in text and 'height=' in text and 'height:auto' not in text and 'height: auto' not in text:
            new_text = svg_pattern.sub(clean_svg_tag, text)
            if new_text != text:
                cur.execute("UPDATE preguntas SET enunciado = %s WHERE id = %s;", (new_text, q_id))
                updated_count += 1

    loc_conn.commit()
    print(f"  ✓ {updated_count} preguntas de la Fase 5 actualizadas con SVGs responsivos y proporcionales.")

    loc_conn.close()

if __name__ == "__main__":
    main()
