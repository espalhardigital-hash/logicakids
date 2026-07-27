"""
Script de Auditoría Profunda Multicriterio de las 9,600 Preguntas de la Fase 5 (Local DB)
Basado en RULES AGENTES/deep_analise_pro.md §8 (Bug Hunting) y §15 (Data Discipline)
"""

import sys
import os
import json
import re
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def main():
    print("=" * 85)
    print("🔬 AUDITORÍA PROFUNDA MULTICRITERIO: FASE 5 (9,600 PREGUNTAS)")
    print("=" * 85)

    loc_env = load_env_file("Datos_localhost/.env.local")
    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    loc_conn = psycopg2.connect(loc_url)
    cur = loc_conn.cursor()

    cur.execute("""
        SELECT p.id, p.seccion, p.sub_nivel, p.operacion, p.tipo_pregunta, 
               p.enunciado, p.respuesta_correcta, p.datos_numericos
        FROM preguntas p
        WHERE p.fase_id = 5
        ORDER BY p.seccion, p.sub_nivel, p.id;
    """)
    questions = cur.fetchall()
    total_q = len(questions)
    print(f"[*] Total de preguntas en Fase 5: {total_q}")

    bad_svg_tags = []
    svg_overflow = []
    missing_values = []
    broken_urls = []
    corrupt_encoding = []
    invalid_mult_choice = []
    invalid_numeric_ans = []

    svg_tag_regex = re.compile(r'<svg([^>]*)>', re.IGNORECASE)

    for q in questions:
        q_id, seccion, sub_nivel, operacion, tipo_p, text, resp_corr, datos_num = q

        # A. Inspección de SVG
        svg_matches = svg_tag_regex.findall(text)
        for attr_str in svg_matches:
            # Detectar si tiene width y height fijos que puedan causar distorsión de viewBox
            if 'width=' in attr_str and 'height=' in attr_str:
                if 'height="auto"' not in attr_str and "height='auto'" not in attr_str and 'max-width' not in attr_str:
                    bad_svg_tags.append((q_id, seccion, sub_nivel, attr_str[:120]))

        # B. Valores Faltantes / Placeholders
        if re.search(r'undefined|NaN|null|\[object Object\]|\{\s*val\s*\}|\?\?|__', text, re.IGNORECASE):
            missing_values.append((q_id, seccion, sub_nivel, "Placeholder o valor faltante"))

        # C. URLs locales en imágenes
        if 'http://localhost' in text or 'http://127.0.0.1' in text:
            broken_urls.append((q_id, seccion, sub_nivel, "URL de imagen local"))

        # D. Codificación corrupta
        if re.search(r'\b\?[a-z]|\?[A-Z]', text):
            corrupt_encoding.append((q_id, seccion, sub_nivel, "Carácter corrupto con ?"))

        # E. Validación según Tipo de Pregunta
        if tipo_p == 'MULTIPLE_OPCION':
            cur.execute("SELECT id, texto, es_correcta FROM alternativas WHERE pregunta_id = %s ORDER BY orden;", (q_id,))
            alts = cur.fetchall()
            correct_count = sum(1 for a in alts if a[2] is True)
            if len(alts) != 4 or correct_count != 1:
                invalid_mult_choice.append((q_id, seccion, sub_nivel, f"Alternativas={len(alts)}, Correctas={correct_count}"))
        
        elif tipo_p == 'RESPUESTA_NUMERICA':
            if not resp_corr or not resp_corr.strip():
                invalid_numeric_ans.append((q_id, seccion, sub_nivel, "Respuesta correcta vacía/nula"))

    print("\n--- RESULTADOS DE LA AUDITORÍA COMPLETA ---")
    print(f"  1. SVGs con atributos width/height sin max-width/auto: {len(bad_svg_tags)} {'✅ (0 OK)' if len(bad_svg_tags)==0 else '❌'}")
    print(f"  2. Preguntas con placeholders vacíos (NaN, null, etc): {len(missing_values)} {'✅ (0 OK)' if len(missing_values)==0 else '❌'}")
    print(f"  3. Preguntas con URLs locales (http://localhost): {len(broken_urls)} {'✅ (0 OK)' if len(broken_urls)==0 else '❌'}")
    print(f"  4. Preguntas con caracteres corruptos (?): {len(corrupt_encoding)} {'✅ (0 OK)' if len(corrupt_encoding)==0 else '❌'}")
    print(f"  5. Preguntas Opción Múltiple con número de opciones != 4 o != 1 correcta: {len(invalid_mult_choice)} {'✅ (0 OK)' if len(invalid_mult_choice)==0 else '❌'}")
    print(f"  6. Preguntas Respuesta Numérica con respuesta vacía/nula: {len(invalid_numeric_ans)} {'✅ (0 OK)' if len(invalid_numeric_ans)==0 else '❌'}")

    if bad_svg_tags:
        print("\n--- EJEMPLOS DE SVGS CON ATRIBUTOS FIXES ---")
        for item in bad_svg_tags[:5]:
            print(f"  ID {item[0]} | Mód {item[1]} Niv {item[2]}: {item[3]}")

    loc_conn.close()

if __name__ == "__main__":
    main()
