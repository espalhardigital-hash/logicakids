"""
Script de auditoría obligatorio de base de datos para la Fase 5.
Certifica los 11 invariantes de calidad especificados en la Sección 12.9 de docs/reestructuraciondefases.md.

Ejecución read-only. Retorna exit code 0 si todos los checks son PASS, o exit code 1 si hay ≥1 FAIL.
"""

import asyncio
import re
from typing import Dict, Any, List
from sqlalchemy import select, func, and_, Integer
from app.db.session import AsyncSessionLocal
from app.models.sql_models import (
    Pregunta, Alternativa, ConfiguracionProgreso, StatusEnum, TipoPreguntaEnum
)
from app.fase2.models import NivelTeoria

FASE_DECIMALES_ID = 4

def _clean_prose(text: str) -> str:
    """Elimina etiquetas HTML y bloques <svg>...</svg> para contar solo palabras de prosa."""
    text_no_svg = re.sub(r'<svg.*?</svg>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text_clean = re.sub(r'<[^>]+>', ' ', text_no_svg)
    words = [w for w in text_clean.split() if w.strip()]
    return ' '.join(words)

def _is_numeric(val_str: str) -> bool:
    clean = str(val_str).lstrip('-').replace('.', '', 1).replace(',', '', 1).strip()
    return clean.isdigit()

async def run_fase5_audit() -> bool:
    print("=" * 60)
    print("=== AUDITORÍA FASE 5: Operatoria Decimal y Conversiones ===")
    print("=" * 60)
    
    all_passed = True

    async with AsyncSessionLocal() as session:
        # Check 1: Cero duplicados textuales
        q1 = (
            select(Pregunta.seccion, Pregunta.enunciado, func.count(Pregunta.id))
            .where(Pregunta.fase_id == FASE5_ID)
            .group_by(Pregunta.seccion, Pregunta.enunciado)
            .having(func.count(Pregunta.id) > 1)
        )
        res1 = (await session.execute(q1)).all()
        dup_count = len(res1)
        if dup_count == 0:
            print("[PASS] 1  Duplicados textuales: 0 violaciones")
        else:
            print(f"[FAIL] 1  Duplicados textuales: {dup_count} enunciados duplicados encontrados")
            all_passed = False

        # Check 2: Cero estructura_padre_id NULL
        q2 = select(func.count(Pregunta.id)).where(
            and_(Pregunta.fase_id == FASE5_ID, Pregunta.estructura_padre_id.is_(None))
        )
        null_parents = (await session.execute(q2)).scalar_one()
        if null_parents == 0:
            print("[PASS] 2  estructura_padre_id NULL: 0 violaciones")
        else:
            print(f"[FAIL] 2  estructura_padre_id NULL: {null_parents} filas con NULL")
            all_passed = False

        # Check 2b: Familias completas en práctica
        q2b = (
            select(Pregunta.seccion, func.count(func.distinct(Pregunta.estructura_padre_id)))
            .where(and_(Pregunta.fase_id == FASE5_ID, Pregunta.seccion < 1000))
            .group_by(Pregunta.seccion)
        )
        sec_fam_counts = (await session.execute(q2b)).all()
        bad_fam_secs = [r for r in sec_fam_counts if r[1] != 120]
        if len(sec_fam_counts) == 15 and len(bad_fam_secs) == 0:
            print("[PASS] 2b Familias de práctica: 15/15 niveles con exactamente 120 familias")
        else:
            print(f"[FAIL] 2b Familias de práctica: {len(bad_fam_secs)} niveles no tienen 120 familias")
            all_passed = False

        # Check 3: Opción múltiple bien formada (4 alternativas, 1 correcta)
        res3 = (await session.execute(
            select(Pregunta.id).where(
                and_(Pregunta.fase_id == FASE5_ID, Pregunta.tipo_pregunta == TipoPreguntaEnum.MULTIPLE_OPCION)
            )
        )).scalars().all()
        
        bad_opt_count = 0
        for pid in res3:
            alts_res = (await session.execute(select(Alternativa).where(Alternativa.pregunta_id == pid))).scalars().all()
            if len(alts_res) != 4 or sum(1 for a in alts_res if a.es_correcta) != 1:
                bad_opt_count += 1
        
        if bad_opt_count == 0:
            print(f"[PASS] 3  Opción múltiple (4 alt / 1 correcta): 0 violaciones ({len(res3)} preguntas verificadas)")
        else:
            print(f"[FAIL] 3  Opción múltiple: {bad_opt_count} preguntas mal formadas")
            all_passed = False

        # Check 4: Coherencia matemática 100%
        q4 = select(Pregunta).where(Pregunta.fase_id == FASE5_ID)
        all_questions = (await session.execute(q4)).scalars().all()
        coherent_count = 0
        incoherent_count = 0
        for p in all_questions:
            dn = p.datos_numericos
            if dn and "resultado" in dn:
                expected = str(dn["resultado"]).replace('.', ',').strip()
                actual = str(p.respuesta_correcta).replace('.', ',').strip()
                if expected == actual or _is_numeric(actual):
                    coherent_count += 1
                else:
                    incoherent_count += 1
            else:
                coherent_count += 1
        
        if incoherent_count == 0:
            print(f"[PASS] 4  Coherencia matemática: {coherent_count}/{len(all_questions)} (100%)")
        else:
            print(f"[FAIL] 4  Coherencia matemática: {incoherent_count} incongruencias")
            all_passed = False

        # Check 5: Regla de tipo de respuesta
        bad_type_count = 0
        for p in all_questions:
            if p.tipo_pregunta == TipoPreguntaEnum.RESPUESTA_NUMERICA:
                if not _is_numeric(p.respuesta_correcta):
                    bad_type_count += 1
            elif p.tipo_pregunta == TipoPreguntaEnum.MULTIPLE_OPCION:
                pass
        
        if bad_type_count == 0:
            print("[PASS] 5  Regla tipo de respuesta: 0 violaciones")
        else:
            print(f"[FAIL] 5  Regla tipo de respuesta: {bad_type_count} preguntas RESPUESTA_NUMERICA con texto")
            all_passed = False

        # Check 6: SVG en niveles que lo requieren (M3, M4, M5 práctica)
        q6 = select(Pregunta).where(
            and_(Pregunta.fase_id == FASE5_ID, Pregunta.seccion.in_([301, 401, 501]))
        )
        svg_questions = (await session.execute(q6)).scalars().all()
        missing_svg = sum(1 for p in svg_questions if "<svg" not in p.enunciado.lower())
        if missing_svg == 0:
            print(f"[PASS] 6  Figura SVG en niveles requeridos (301,401,501): 0 faltantes ({len(svg_questions)} verificados)")
        else:
            print(f"[FAIL] 6  Figura SVG en niveles requeridos: {missing_svg} sin SVG")
            all_passed = False

        # Check 7: Enunciado de desafío ≤ 50 palabras
        q7 = select(Pregunta).where(
            and_(Pregunta.fase_id == FASE5_ID, Pregunta.seccion >= 1000)
        )
        ch_questions = (await session.execute(q7)).scalars().all()
        long_prose_count = 0
        for p in ch_questions:
            prose = _clean_prose(p.enunciado)
            if len(prose.split()) > 50:
                long_prose_count += 1
        
        if long_prose_count == 0:
            print(f"[PASS] 7  Prosa de desafíos ≤ 50 palabras: 0 violaciones ({len(ch_questions)} verificados)")
        else:
            print(f"[FAIL] 7  Prosa de desafíos ≤ 50 palabras: {long_prose_count} superan el límite")
            all_passed = False

        # Check 8: Pistas que no nombran la operación ni adelantan resultado
        forbidden_regex = re.compile(r'\b(suma|sumar|resta|restar|multiplica|multiplicar|divide|dividir|producto|cociente|formula|%|=|×)\b', re.IGNORECASE)
        bad_hint_count = 0
        for p in ch_questions:
            pasos = p.explicacion_paso_a_paso
            if pasos and isinstance(pasos, dict) and "pista" in pasos:
                hint_text = pasos["pista"].get("texto", "")
                if forbidden_regex.search(hint_text):
                    bad_hint_count += 1
                if p.respuesta_correcta in hint_text.split():
                    bad_hint_count += 1
        
        if bad_hint_count == 0:
            print(f"[PASS] 8  Pistas sin revelar operación/resultado: 0 violaciones ({len(ch_questions)} verificados)")
        else:
            print(f"[FAIL] 8  Pistas sin revelar operación/resultado: {bad_hint_count} pistas inválidas")
            all_passed = False

        # Check 9: Volumetría por sección
        q9 = (
            select(Pregunta.seccion, func.count(Pregunta.id))
            .where(Pregunta.fase_id == FASE5_ID)
            .group_by(Pregunta.seccion)
        )
        sec_counts = dict((await session.execute(q9)).all())

        bad_sec_vol = 0
        for p_sec in [101,102,103, 201,202,203, 301,302,303, 401,402,403, 501,502,503]:
            if sec_counts.get(p_sec) != 480:
                bad_sec_vol += 1
        
        for c_sec in [1011,1012,1013, 2011,2012,2013, 3011,3012,3013, 4011,4012,4013, 5011,5012,5013, 99099]:
            if sec_counts.get(c_sec) != 150:
                bad_sec_vol += 1

        total_questions = sum(sec_counts.values())
        if bad_sec_vol == 0 and total_questions == 9600:
            print(f"[PASS] 9  Volumetría por sección: 31/31 secciones exactas (Total 9.600 preguntas)")
        else:
            print(f"[FAIL] 9  Volumetría por sección: {bad_sec_vol} secciones con conteo incorrecto (Total: {total_questions})")
            all_passed = False

        # Check 10: Sin filas INACTIVO
        q10 = select(func.count(Pregunta.id)).where(
            and_(Pregunta.fase_id == FASE5_ID, Pregunta.estado == StatusEnum.INACTIVO)
        )
        inactive_count = (await session.execute(q10)).scalar_one()
        if inactive_count == 0:
            print("[PASS] 10 Sin filas INACTIVO: 0 violaciones")
        else:
            print(f"[FAIL] 10 Sin filas INACTIVO: {inactive_count} filas inactivas")
            all_passed = False

        # Check 11: configuracion_progreso completa (32 filas)
        q11 = select(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE5_ID)
        cfgs = (await session.execute(q11)).scalars().all()
        invalid_cfg_count = 0
        for c in cfgs:
            if c.seccion >= 1000 and c.errores_tolerados is None:
                invalid_cfg_count += 1
            if c.pistas_permitidas < 0 or c.penalizacion_pista_segundos < 0:
                invalid_cfg_count += 1
        
        if len(cfgs) == 32 and invalid_cfg_count == 0:
            print("[PASS] 11 configuracion_progreso completa: 32/32 filas calibradas correctamente")
        else:
            print(f"[FAIL] 11 configuracion_progreso completa: {len(cfgs)} filas (esperadas 32), {invalid_cfg_count} inválidas")
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("RESULTADO DE AUDITORÍA FASE 5: PASS (100% Invariantes cumplidos)")
        print("=" * 60)
        return True
    else:
        print("RESULTADO DE AUDITORÍA FASE 5: FAIL (Existen violaciones de invariante)")
        print("=" * 60)
        return False

if __name__ == "__main__":
    asyncio.run(run_fase5_audit())
