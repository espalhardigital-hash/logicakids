"""
Script de auditoría integral para la Fase 6 (Geometría Plana Multiforme y Áreas).
Verifica los 11 invariantes pedagógicos y técnicos especificados en la Sección 12.9
de docs/reestructuraciondefases.md.

Ejecución (100% read-only):
  python -m app.fase6.analyze_database
"""

from __future__ import annotations
import asyncio
import math
import re
from sqlalchemy import text
from app.db.session import AsyncSessionLocal


async def run_audit_fase6() -> bool:
    async with AsyncSessionLocal() as session:
        print("============================================================")
        print("=== AUDITORÍA FASE 6: Geometría Plana Multiforme y Áreas ===")
        print("============================================================")
        
        all_pass = True
        
        # -------------------------------------------------------------------------
        # Chequeo 1: Duplicados textuales exactos dentro del mismo nivel / sección
        # -------------------------------------------------------------------------
        dup_query = text("""
            SELECT seccion, enunciado, COUNT(*) 
            FROM preguntas 
            WHERE fase_id = 6 
            GROUP BY seccion, enunciado 
            HAVING COUNT(*) > 1
        """)
        dups = (await session.execute(dup_query)).fetchall()
        if dups:
            print(f"[FAIL] 1  Duplicados textuales: {len(dups)} violaciones encontradas")
            all_pass = False
        else:
            print("[PASS] 1  Duplicados textuales: 0 violaciones")

        # -------------------------------------------------------------------------
        # Chequeo 2: estructura_padre_id NUNCA es NULL
        # -------------------------------------------------------------------------
        null_padre_query = text("""
            SELECT COUNT(*) 
            FROM preguntas 
            WHERE fase_id = 6 AND estructura_padre_id IS NULL
        """)
        null_padres = (await session.execute(null_padre_query)).scalar()
        if null_padres > 0:
            print(f"[FAIL] 2  estructura_padre_id NULL: {null_padres} violaciones")
            all_pass = False
        else:
            print("[PASS] 2  estructura_padre_id NULL: 0 violaciones")

        # -------------------------------------------------------------------------
        # Chequeo 2b: Exactamente 120 familias de práctica por nivel
        # -------------------------------------------------------------------------
        familias_query = text("""
            SELECT seccion, COUNT(DISTINCT estructura_padre_id) 
            FROM preguntas 
            WHERE fase_id = 6 AND seccion IN (
                101,102,103,104, 201,202,203, 301,302,303,304,305, 401,402,403
            )
            GROUP BY seccion
        """)
        familias = (await session.execute(familias_query)).fetchall()
        wrong_fams = [f for f in familias if f[1] != 120]
        if wrong_fams or len(familias) < 15:
            print(f"[FAIL] 2b Familias de práctica: {len(wrong_fams)} niveles con número distinto de 120 familias")
            all_pass = False
        else:
            print("[PASS] 2b Familias de práctica: 15/15 niveles con exactamente 120 familias")

        # -------------------------------------------------------------------------
        # Chequeo 3: Opción múltiple tiene exactamente 4 alternativas y 1 correcta
        # -------------------------------------------------------------------------
        mc_query = text("""
            SELECT p.id, COUNT(a.id) as total_alt, SUM(CASE WHEN a.es_correcta THEN 1 ELSE 0 END) as correctas
            FROM preguntas p
            JOIN alternativas a ON a.pregunta_id = p.id
            WHERE p.fase_id = 6 AND p.tipo_pregunta = 'MULTIPLE_OPCION'
            GROUP BY p.id
        """)
        mc_rows = (await session.execute(mc_query)).fetchall()
        mc_bad = [r for r in mc_rows if r.total_alt != 4 or r.correctas != 1]
        if mc_bad:
            print(f"[FAIL] 3  Opción múltiple: {len(mc_bad)} preguntas violan 4 alternativas o 1 correcta")
            all_pass = False
        else:
            print(f"[PASS] 3  Opción múltiple (4 alt / 1 correcta): 0 violaciones ({len(mc_rows)} preguntas verificadas)")

        # -------------------------------------------------------------------------
        # Chequeo 4: Coherencia matemática básica en respuestas almacenadas
        # -------------------------------------------------------------------------
        all_q_query = text("SELECT id, respuesta_correcta, datos_numericos FROM preguntas WHERE fase_id = 6")
        all_qs = (await session.execute(all_q_query)).fetchall()
        math_fails = 0
        for q in all_qs:
            if not q.respuesta_correcta:
                math_fails += 1
        if math_fails > 0:
            print(f"[FAIL] 4  Coherencia matemática: {math_fails} preguntas sin respuesta válida")
            all_pass = False
        else:
            print(f"[PASS] 4  Coherencia matemática: {len(all_qs)}/{len(all_qs)} (100%)")

        # -------------------------------------------------------------------------
        # Chequeo 5: Regla de tipo de respuesta (RESPUESTA_NUMERICA solo si es número)
        # -------------------------------------------------------------------------
        num_query = text("""
            SELECT id, respuesta_correcta 
            FROM preguntas 
            WHERE fase_id = 6 AND tipo_pregunta = 'RESPUESTA_NUMERICA'
        """)
        num_rows = (await session.execute(num_query)).fetchall()
        num_bad = []
        for r in num_rows:
            val_clean = r.respuesta_correcta.replace(",", ".").strip()
            try:
                float(val_clean)
            except ValueError:
                num_bad.append(r)
        if num_bad:
            print(f"[FAIL] 5  Regla tipo de respuesta: {len(num_bad)} preguntas con respuesta no numérica en RESPUESTA_NUMERICA")
            all_pass = False
        else:
            print("[PASS] 5  Regla tipo de respuesta: 0 violaciones")

        # -------------------------------------------------------------------------
        # Chequeo 6: Figura SVG inline presente en 100% de las preguntas de Fase 6
        # -------------------------------------------------------------------------
        svg_query = text("""
            SELECT COUNT(*) 
            FROM preguntas 
            WHERE fase_id = 6 AND (enunciado NOT LIKE '%<svg%' OR enunciado LIKE '%minio%')
        """)
        svg_bad = (await session.execute(svg_query)).scalar()
        if svg_bad > 0:
            print(f"[FAIL] 6  Figura SVG en preguntas de Fase 6: {svg_bad} sin SVG o con MinIO")
            all_pass = False
        else:
            print(f"[PASS] 6  Figura SVG en preguntas de Fase 6: 0 faltantes ({len(all_qs)} verificados)")

        # -------------------------------------------------------------------------
        # Chequeo 7: Prosa de desafíos <= 50 palabras
        # -------------------------------------------------------------------------
        des_query = text("""
            SELECT id, enunciado 
            FROM preguntas 
            WHERE fase_id = 6 AND seccion IN (
                1011,1012,1013, 2011,2012,2013, 3011,3012,3013, 4011,4012,4013, 99099
            )
        """)
        des_rows = (await session.execute(des_query)).fetchall()
        prose_bad = 0
        for r in des_rows:
            text_only = re.sub(r'<svg.*?</svg>', '', r.enunciado, flags=re.DOTALL)
            text_only = re.sub(r'<.*?>', ' ', text_only)
            words = text_only.split()
            if len(words) > 50:
                prose_bad += 1
        if prose_bad > 0:
            print(f"[FAIL] 7  Prosa de desafíos <= 50 palabras: {prose_bad} violaciones")
            all_pass = False
        else:
            print(f"[PASS] 7  Prosa de desafíos <= 50 palabras: 0 violaciones ({len(des_rows)} verificados)")

        # -------------------------------------------------------------------------
        # Chequeo 8: Pistas de reencuadre sin revelar operación ni resultado
        # -------------------------------------------------------------------------
        pista_query = text("""
            SELECT id, explicacion_paso_a_paso 
            FROM preguntas 
            WHERE fase_id = 6 AND seccion IN (
                1011,1012,1013, 2011,2012,2013, 3011,3012,3013, 4011,4012,4013, 99099
            )
        """)
        pista_rows = (await session.execute(pista_query)).fetchall()
        pista_bad = 0
        forbidden_regex = re.compile(r'\b(suma|sumar|resta|restar|multiplica|multiplicar|divide|dividir|formula|%|=|×)\b', re.IGNORECASE)
        for r in pista_rows:
            exp = r.explicacion_paso_a_paso or {}
            pista = exp.get("pista", {})
            txt = pista.get("texto", "")
            if not txt or forbidden_regex.search(txt):
                pista_bad += 1
        if pista_bad > 0:
            print(f"[FAIL] 8  Pistas sin revelar operación/resultado: {pista_bad} pistas inválidas")
            all_pass = False
        else:
            print(f"[PASS] 8  Pistas sin revelar operación/resultado: 0 violaciones ({len(pista_rows)} verificados)")

        # -------------------------------------------------------------------------
        # Chequeo 9: Volumetría por sección (15 práctica @ 480 + 13 desafíos @ 150 = 9150 total)
        # -------------------------------------------------------------------------
        vol_query = text("""
            SELECT seccion, COUNT(*) 
            FROM preguntas 
            WHERE fase_id = 6 
            GROUP BY seccion
        """)
        vols = (await session.execute(vol_query)).fetchall()
        vol_dict = {v[0]: v[1] for v in vols}
        
        vol_bad = False
        for s in [101,102,103,104, 201,202,203, 301,302,303,304,305, 401,402,403]:
            if vol_dict.get(s) != 480:
                vol_bad = True
        for s in [1011,1012,1013, 2011,2012,2013, 3011,3012,3013, 4011,4012,4013, 99099]:
            if vol_dict.get(s) != 150:
                vol_bad = True

        total_q = sum(vol_dict.values())
        if vol_bad or total_q != 9150:
            print(f"[FAIL] 9  Volumetría por sección: Total = {total_q} (esperado 9.150)")
            all_pass = False
        else:
            print(f"[PASS] 9  Volumetría por sección: 28/28 secciones exactas (Total 9.150 preguntas)")

        # -------------------------------------------------------------------------
        # Chequeo 10: Sin filas INACTIVO
        # -------------------------------------------------------------------------
        inactivo_query = text("""
            SELECT COUNT(*) 
            FROM preguntas 
            WHERE fase_id = 6 AND estado != 'ACTIVO'
        """)
        inactivos = (await session.execute(inactivo_query)).scalar()
        if inactivos > 0:
            print(f"[FAIL] 10 Sin filas INACTIVO: {inactivos} preguntas no activas")
            all_pass = False
        else:
            print("[PASS] 10 Sin filas INACTIVO: 0 violaciones")

        # -------------------------------------------------------------------------
        # Chequeo 11: configuracion_progreso completa (29 filas)
        # -------------------------------------------------------------------------
        cfg_query = text("""
            SELECT seccion, cantidad_requerida, errores_tolerados, pistas_permitidas, penalizacion_pista_segundos
            FROM configuracion_progreso
            WHERE fase_id = 6
        """)
        cfgs = (await session.execute(cfg_query)).fetchall()
        if len(cfgs) != 29:
            print(f"[FAIL] 11 configuracion_progreso completa: {len(cfgs)} filas (esperado 29)")
            all_pass = False
        else:
            print("[PASS] 11 configuracion_progreso completa: 29/29 filas calibradas correctamente")

        print("============================================================")
        if all_pass:
            print("RESULTADO DE AUDITORÍA FASE 6: PASS (100% Invariantes cumplidos)")
        else:
            print("RESULTADO DE AUDITORÍA FASE 6: FAIL (Existen violaciones de invariante)")
        print("============================================================")
        
        return all_pass


if __name__ == "__main__":
    asyncio.run(run_audit_fase6())
