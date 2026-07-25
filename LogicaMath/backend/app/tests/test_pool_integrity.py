"""
Pruebas de Integridad de Pool de Preguntas — LogicaKids Pro
==========================================================
Verifica los invariantes pedagógicos y de datos en la BD:
 1. 0 preguntas MULTIPLE_OPCION con 0 alternativas (LEFT JOIN).
 2. 0 preguntas RESPUESTA_NUMERICA con respuesta no numérica.
 3. Cardinalidad de familias (estructura_padre_id no NULL en secciones de práctica).
 4. Mapeo correcto de imágenes (menciona figura -> datos_numericos tiene url).
"""

import pytest
import re
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.models.sql_models import Pregunta, Alternativa


@pytest.mark.asyncio
async def test_no_empty_multiple_choice_options(db_session):
    """Garantiza que ninguna pregunta de OPCION MULTIPLE tenga 0 alternativas."""
    query = (
        select(Pregunta.id, Pregunta.fase_id, Pregunta.seccion)
        .outerjoin(Alternativa, Alternativa.pregunta_id == Pregunta.id)
        .where(
            and_(
                Pregunta.fase_id.in_([1, 2, 3, 4, 5, 6, 7, 8]),
                Pregunta.tipo_pregunta == 'MULTIPLE_OPCION'
            )
        )
        .group_by(Pregunta.id, Pregunta.fase_id, Pregunta.seccion)
        .having(func.count(Alternativa.id) == 0)
    )
    result = await db_session.execute(query)
    huérfanas = result.all()
    assert len(huérfanas) == 0, f"Preguntas MULTIPLE_OPCION sin alternativas encontradas: {huérfanas}"


@pytest.mark.asyncio
async def test_numeric_answers_are_parseable(db_session):
    """Garantiza que las preguntas de RESPUESTA NUMERICA tengan valores numéricos parseables."""
    query = select(Pregunta).where(
        and_(
            Pregunta.fase_id.in_([1, 2, 3, 4, 5, 6, 7, 8]),
            Pregunta.tipo_pregunta == 'RESPUESTA_NUMERICA'
        )
    )
    result = await db_session.execute(query)
    preguntas = result.scalars().all()
    
    numeric_pattern = re.compile(r'^-?[0-9]+([.,][0-9]+)?$')
    invalid_answers = []
    
    for p in preguntas:
        ans = (p.respuesta_correcta or '').strip()
        if not numeric_pattern.match(ans):
            invalid_answers.append((p.id, p.fase_id, p.seccion, ans))
            
    assert len(invalid_answers) == 0, f"Respuestas de texto en tipo RESPUESTA_NUMERICA: {invalid_answers}"


@pytest.mark.asyncio
async def test_estructura_padre_id_cardinality(db_session):
    """Verifica que las secciones de práctica tengan estructura_padre_id poblado (no 100% NULL)."""
    for fase_id in range(1, 9):
        query = select(
            func.count(Pregunta.id).label("total"),
            func.count(Pregunta.estructura_padre_id).label("con_padre"),
            func.count(func.distinct(Pregunta.estructura_padre_id)).label("distintos_padres")
        ).where(
            and_(
                Pregunta.fase_id == fase_id,
                Pregunta.seccion < 1000  # Práctica libre
            )
        )
        result = await db_session.execute(query)
        row = result.first()
        if row and row.total > 0:
            assert row.con_padre > 0, f"Fase {fase_id} tiene estructura_padre_id 100% NULL ({row.con_padre}/{row.total})"
