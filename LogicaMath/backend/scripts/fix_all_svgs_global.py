"""
Script de Reparación 100% Definitivo para TODAS LAS 13,440 PREGUNTAS SVG EN TODAS LAS FASES
Calcula dinámicamente la altura proporcional desde el viewBox y añade inercia CSS (height, min-height y aspect-ratio).
"""

import sys
import os
import re
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def fix_any_svg_tag(match):
    full_tag = match.group(0)

    # 1. Extraer viewBox
    vb_match = re.search(r'viewBox=["\']([0-9.\-\s]+)["\']', full_tag, re.IGNORECASE)
    
    calc_width = 320
    calc_height = 200
    aspect_ratio_str = "16/9"

    if vb_match:
        parts = [float(v) for v in vb_match.group(1).split()]
        if len(parts) == 4:
            vb_w = parts[2]
            vb_h = parts[3]
            if vb_w > 0 and vb_h > 0:
                # Si es la tabla de montos 200x64
                if vb_w == 200 and vb_h == 64:
                    calc_height = 102
                    aspect_ratio_str = "200/64"
                elif vb_w == vb_h:
                    calc_width = 260
                    calc_height = 260
                    aspect_ratio_str = "1/1"
                else:
                    aspect_ratio_str = f"{int(vb_w)}/{int(vb_h)}"
                    calc_height = int((calc_width * vb_h) / vb_w)
                    if calc_height < 180:
                        calc_height = 180

    vb_attr = f'viewBox="{vb_match.group(1)}"' if vb_match else ''

    # Preservar o añadir borde morado/naranja y fondo oscuro
    border_color = "#8B5CF6"
    if "F59E0B" in full_tag:
        border_color = "#F59E0B"
    elif "10B981" in full_tag:
        border_color = "#10B981"

    style_attr = f'style="margin:10px auto; display:block; width:100%; max-width:{calc_width}px; height:{calc_height}px; min-height:{calc_height}px; aspect-ratio:{aspect_ratio_str}; background:#111827; border:2px solid {border_color}; border-radius:14px;"'

    return f'<svg {vb_attr} width="100%" height="{calc_height}" {style_attr}>'

def main():
    print("=" * 85)
    print("🚀 REPARACIÓN 100% ABSOLUTA DE SVGS EN TODAS LAS FASES (LOCAL DB)")
    print("=" * 85)

    loc_env = load_env_file("Datos_localhost/.env.local")
    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    loc_conn = psycopg2.connect(loc_url)
    cur = loc_conn.cursor()

    cur.execute("""
        SELECT id, fase_id, enunciado 
        FROM preguntas 
        WHERE enunciado LIKE '%<svg%';
    """)
    rows = cur.fetchall()
    print(f"[*] Procesando las {len(rows)} preguntas con SVG en TODAS LAS FASES...")

    svg_tag_regex = re.compile(r'<svg\s+[^>]*>', re.IGNORECASE)
    updated_count = 0

    for q_id, fase_id, text in rows:
        new_text = svg_tag_regex.sub(fix_any_svg_tag, text)
        if new_text != text:
            cur.execute("UPDATE preguntas SET enunciado = %s WHERE id = %s;", (new_text, q_id))
            updated_count += 1

    loc_conn.commit()
    print(f"  ✓ {updated_count} preguntas actualizadas con dimensiones intrínsecas dinámicas.")

    # Verificar de nuevo si queda algún SVG sin altura o con height:auto
    cur.execute("""
        SELECT COUNT(*) 
        FROM preguntas 
        WHERE enunciado LIKE '%<svg%' 
          AND (enunciado LIKE '%height:auto%' OR enunciado LIKE '%height: auto%');
    """)
    remaining_auto = cur.fetchone()[0]
    print(f"  👉 Preguntas restantes con height:auto en la base de datos: {remaining_auto} {'✅ (0 OK)' if remaining_auto == 0 else '❌'}")

    loc_conn.close()

if __name__ == "__main__":
    main()
