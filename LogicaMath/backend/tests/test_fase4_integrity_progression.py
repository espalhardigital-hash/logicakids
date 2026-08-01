from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.fase4 import router as fase4_router
from app.fase4.schemas import Fase4ResponderPregunta, Fase4CerrarRescate
from app.fase4.topology import (
    MIXED_SECTION,
    PLAYABLE_BLOCKS,
    PREREQUISITE_BLOCKS,
    all_prerequisites_approved,
    configured_error_tolerance,
    get_block,
    has_reached_error_limit,
    is_block_unlocked,
    phase_is_complete,
)


def approved_progress():
    return SimpleNamespace(estado="aprobado")


def test_phase4_has_24_prerequisites_and_one_mixed_block():
    assert len(PREREQUISITE_BLOCKS) == 24
    assert len(PLAYABLE_BLOCKS) == 25
    assert get_block(99, 99).section == MIXED_SECTION


def test_mixed_unlocks_with_exactly_24_canonical_prerequisites():
    progress = {block.section: approved_progress() for block in PREREQUISITE_BLOCKS}

    assert all_prerequisites_approved(progress)
    assert is_block_unlocked(progress, 99, 99)


def test_phantom_progress_does_not_unlock_or_complete_phase():
    progress = {123456: approved_progress(), 0: approved_progress()}

    assert not is_block_unlocked(progress, 99, 99)
    assert not phase_is_complete(progress)


def test_only_approved_mixed_block_completes_phase():
    progress = {block.section: approved_progress() for block in PREREQUISITE_BLOCKS}
    assert not phase_is_complete(progress)

    progress[MIXED_SECTION] = approved_progress()
    assert phase_is_complete(progress)


@pytest.mark.parametrize("module_id,level_id", [(0, 1), (1, 4), (99, 13), (4, 99)])
def test_response_schema_rejects_noncanonical_blocks(module_id, level_id):
    with pytest.raises(ValidationError):
        Fase4ResponderPregunta(
            modulo_id=module_id,
            nivel_id=level_id,
            pregunta_id=1,
            respuesta_dada="1",
        )


def test_response_schema_rejects_multiple_answer_modes():
    with pytest.raises(ValidationError):
        Fase4ResponderPregunta(
            modulo_id=1,
            nivel_id=1,
            pregunta_id=1,
            respuesta_dada="1",
            alternativa_id=2,
        )


def test_rescue_schema_rejects_cross_topology_pair():
    with pytest.raises(ValidationError):
        Fase4CerrarRescate(modulo_id=1, nivel_id=99, pregunta_id=1)


def test_configured_error_tolerance_wins_over_percentage_math():
    assert configured_error_tolerance(1, 11, 2) == 2
    assert configured_error_tolerance(1, 13, 1) == 1
    assert configured_error_tolerance(99, 99, 3) == 3


def test_early_exit_first_error_limit_and_new_attempt():
    tolerance = configured_error_tolerance(1, 11, 2)
    assert not has_reached_error_limit(1, tolerance)
    assert has_reached_error_limit(2, tolerance)
    # The explicit/early-exit reset clears the previous session.
    assert not has_reached_error_limit(0, tolerance)


@pytest.mark.asyncio
async def test_resolver_rejects_question_from_another_section():
    question = SimpleNamespace(seccion=102)
    result = SimpleNamespace(scalar_one_or_none=lambda: question)
    db = SimpleNamespace(execute=AsyncMock(return_value=result))

    with pytest.raises(HTTPException) as exc_info:
        await fase4_router._resolve_question_for_block(db, 7, 1, 1)

    assert exc_info.value.status_code == 409


@pytest.mark.asyncio
async def test_resolver_does_not_expose_question_from_another_phase():
    result = SimpleNamespace(scalar_one_or_none=lambda: None)
    db = SimpleNamespace(execute=AsyncMock(return_value=result))

    with pytest.raises(HTTPException) as exc_info:
        await fase4_router._resolve_question_for_block(db, 7, 1, 1)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_direct_access_to_locked_block_is_rejected(monkeypatch):
    monkeypatch.setattr(
        fase4_router,
        "_load_progress_by_section",
        AsyncMock(return_value={}),
    )

    with pytest.raises(HTTPException) as exc_info:
        await fase4_router._authorize_block_access(
            SimpleNamespace(), SimpleNamespace(id=1), 2, 1, {"role": "USER"}
        )

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_invalid_question_identity_cannot_create_phantom_progress(monkeypatch):
    resolver = AsyncMock(
        side_effect=HTTPException(status_code=409, detail="section mismatch")
    )
    create_progress = AsyncMock()
    monkeypatch.setattr(fase4_router, "_resolve_question_for_block", resolver)
    monkeypatch.setattr(fase4_router, "_get_or_create_progreso", create_progress)

    payload = Fase4ResponderPregunta(
        modulo_id=1,
        nivel_id=1,
        pregunta_id=7,
        respuesta_dada="1",
    )
    with pytest.raises(HTTPException):
        await fase4_router.responder_fase4(
            payload,
            db=SimpleNamespace(),
            alumno=SimpleNamespace(id=1),
            current_user={"role": "USER"},
        )

    create_progress.assert_not_awaited()


@pytest.mark.asyncio
async def test_admin_unlock_bypass_does_not_read_or_create_progress(monkeypatch):
    load_progress = AsyncMock()
    monkeypatch.setattr(fase4_router, "_load_progress_by_section", load_progress)

    result = await fase4_router._authorize_block_access(
        SimpleNamespace(), SimpleNamespace(id=1), 4, 13, {"role": "ADMIN"}
    )

    assert result == {}
    load_progress.assert_not_awaited()


def fake_scalar_result(*, one=None, optional=None):
    return SimpleNamespace(
        scalar_one=lambda: one,
        scalar_one_or_none=lambda: optional,
    )


@pytest.mark.asyncio
async def test_graduation_advances_transactionally_to_phase5():
    student = SimpleNamespace(id=1, fase_actual_id=4)
    target = SimpleNamespace(id=5, orden=5, nombre="Fase 5")
    current = SimpleNamespace(id=4, orden=4)
    mixed = SimpleNamespace(estado="aprobado")
    db = SimpleNamespace(
        execute=AsyncMock(side_effect=[
            fake_scalar_result(one=student),
            fake_scalar_result(optional=target),
            fake_scalar_result(optional=current),
            fake_scalar_result(optional=mixed),
        ]),
        commit=AsyncMock(),
    )

    response = await fase4_router.graduate_fase4(db=db, alumno=student)

    assert student.fase_actual_id == 5
    assert response["nueva_fase_id"] == 5
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_graduation_is_idempotent_when_already_in_phase5():
    student = SimpleNamespace(id=1, fase_actual_id=5)
    target = SimpleNamespace(id=5, orden=5, nombre="Fase 5")
    db = SimpleNamespace(
        execute=AsyncMock(side_effect=[
            fake_scalar_result(one=student),
            fake_scalar_result(optional=target),
        ]),
        commit=AsyncMock(),
    )

    response = await fase4_router.graduate_fase4(db=db, alumno=student)

    assert response["nueva_fase_id"] == 5
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_graduation_fails_when_phase5_is_not_configured():
    student = SimpleNamespace(id=1, fase_actual_id=4)
    db = SimpleNamespace(
        execute=AsyncMock(side_effect=[
            fake_scalar_result(one=student),
            fake_scalar_result(optional=None),
        ]),
        commit=AsyncMock(),
    )

    with pytest.raises(HTTPException) as exc_info:
        await fase4_router.graduate_fase4(db=db, alumno=student)

    assert exc_info.value.status_code == 500
    db.commit.assert_not_awaited()
