"""
Pruebas de Contrato y Simulador de Endpoints — LogicaKids Pro
============================================================
Simula el flujo de respuesta de alumnos en los routers de Fases 1 a 8
verificando la estructura del JSON y que no existan retornos nulos (NoneType).
"""

import pytest
from sqlalchemy import select, and_

from app.models.sql_models import Alumno, Pregunta

# Importar routers y schemas de respuesta de las fases activas 1 a 8
from app.fase1.router import router as fase1_router
from app.fase2.router import responder_fase2
from app.fase2.schemas import Fase2ResponderPregunta
from app.fase3.router import responder_fase3
from app.fase3.schemas import Fase3ResponderPregunta
from app.fase4.router import responder_fase4
from app.fase4.schemas import Fase4ResponderPregunta
from app.fase5.router import responder_fase5
from app.fase5.schemas import Fase5ResponderPregunta
from app.fase6.router import responder_fase6
from app.fase6.schemas import Fase6ResponderPregunta
from app.fase7.router import responder_fase7
from app.fase7.schemas import Fase7ResponderPregunta
from app.fase8.router import responder_fase8
from app.fase8.schemas import Fase8ResponderPregunta


@pytest.mark.asyncio
@pytest.mark.parametrize("fase_id,responder_fn,schema_cls", [
    (2, responder_fase2, Fase2ResponderPregunta),
    (3, responder_fase3, Fase3ResponderPregunta),
    (4, responder_fase4, Fase4ResponderPregunta),
    (5, responder_fase5, Fase5ResponderPregunta),
    (6, responder_fase6, Fase6ResponderPregunta),
    (7, responder_fase7, Fase7ResponderPregunta),
    (8, responder_fase8, Fase8ResponderPregunta),
])
async def test_fases_responder_contract(db_session, fase_id, responder_fn, schema_cls):
    """Simula responder en cada Fase (2-8) verificando que devuelva un objeto válido y no None/500."""
    result = await db_session.execute(select(Alumno).limit(1))
    alumno = result.scalar_one_or_none()
    if not alumno:
        pytest.skip("No hay alumnos en la BD para probar los endpoints responder_fase")

    res_p = await db_session.execute(
        select(Pregunta).where(Pregunta.fase_id == fase_id).limit(1)
    )
    pregunta = res_p.scalar_one_or_none()
    if not pregunta:
        pytest.skip(f"No hay preguntas de Fase {fase_id} en la BD")

    payload = schema_cls(
        pregunta_id=pregunta.id,
        respuesta_dada=pregunta.respuesta_correcta or "1",
        tiempo_segundos=5
    )

    respuesta = await responder_fn(
        payload=payload,
        db=db_session,
        current_user={"alumno_id": alumno.id, "id": alumno.user_id, "role": "USER", "alumno_obj": alumno}
    )

    assert respuesta is not None, f"responder_fase{fase_id} devolvió None (error de indentación o rama inalcanzable)"
    assert hasattr(respuesta, 'es_correcta'), f"La respuesta de Fase {fase_id} no contiene 'es_correcta'"
