"""Exercise the complete Phase 4 API progression on an isolated test database."""

import argparse
import asyncio
import json
import uuid
from dataclasses import asdict, dataclass

import httpx
from sqlalchemy import delete, func, select
from sqlalchemy.engine import make_url
from sqlalchemy.orm import selectinload

from app.db.session import AsyncSessionLocal, DATABASE_URL
from app.fase2.models import IntentoPaso, IntentoPregunta
from app.fase4.topology import (
    CHALLENGE_LEVEL_IDS,
    MIXED_BLOCK,
    MIXED_SECTION,
    MODULE_IDS,
    PRACTICE_LEVEL_IDS,
    get_block,
)
from app.models.sql_models import (
    Alumno,
    Fase,
    Intento,
    PoolAsignadoAlumno,
    Pregunta,
    ProgresoMaestria,
    User,
)


@dataclass
class JourneyEvidence:
    database: str
    api_base_url: str
    blocks_completed: int = 0
    requests_answered: int = 0
    unauthorized_status: int | None = None
    locked_status: int | None = None
    cross_section_status: int | None = None
    concurrent_statuses: tuple[int, int] | None = None
    concurrent_credited_answers: int | None = None
    mixed_state_before: str | None = None
    mixed_state_after: str | None = None
    graduated_phase_order: int | None = None
    repeated_graduation_phase_order: int | None = None
    synthetic_user_removed: bool = False


def _assert_test_database() -> str:
    database = make_url(DATABASE_URL).database or ""
    if "fase4_test" not in database.lower():
        raise RuntimeError(
            "Refusing to run: DATABASE_URL must target an isolated fase4_test database."
        )
    return database


def _require_status(response: httpx.Response, expected: int, context: str) -> None:
    if response.status_code != expected:
        raise RuntimeError(
            f"{context}: expected HTTP {expected}, got {response.status_code}: "
            f"{response.text[:500]}"
        )


async def _set_student_phase4(user_id: str) -> int:
    async with AsyncSessionLocal() as session:
        student = (
            await session.execute(select(Alumno).where(Alumno.user_id == user_id))
        ).scalar_one()
        phase4 = (
            await session.execute(select(Fase).where(Fase.orden == 4))
        ).scalar_one()
        student.fase_actual_id = phase4.id
        await session.commit()
        return student.id


async def _answer_payload(question_data: dict, module_id: int, level_id: int) -> dict:
    question_id = question_data["id"]
    async with AsyncSessionLocal() as session:
        question = (
            await session.execute(
                select(Pregunta)
                .options(selectinload(Pregunta.alternativas))
                .where(Pregunta.id == question_id)
            )
        ).scalar_one()

        payload = {
            "modulo_id": module_id,
            "nivel_id": level_id,
            "pregunta_id": question_id,
            "tiempo_respuesta_segundos": 1,
        }
        if question.alternativas:
            correct = next(
                (alternative for alternative in question.alternativas if alternative.es_correcta),
                None,
            )
            if correct is None:
                raise RuntimeError(f"Question {question_id} has no correct alternative.")
            payload["alternativa_id"] = correct.id
        else:
            payload["respuesta_dada"] = question.respuesta_correcta
        return payload


async def _credited_answers(student_id: int, section: int) -> int:
    async with AsyncSessionLocal() as session:
        value = await session.scalar(
            select(ProgresoMaestria.aciertos_acumulados).where(
                ProgresoMaestria.alumno_id == student_id,
                ProgresoMaestria.fase_id == 4,
                ProgresoMaestria.seccion == section,
            )
        )
        return int(value or 0)


async def _progress_exists(student_id: int, section: int) -> bool:
    async with AsyncSessionLocal() as session:
        count = await session.scalar(
            select(func.count(ProgresoMaestria.id)).where(
                ProgresoMaestria.alumno_id == student_id,
                ProgresoMaestria.fase_id == 4,
                ProgresoMaestria.seccion == section,
            )
        )
        return bool(count)


async def _student_phase_order(student_id: int) -> int:
    async with AsyncSessionLocal() as session:
        return (
            await session.execute(
                select(Fase.orden)
                .join(Alumno, Alumno.fase_actual_id == Fase.id)
                .where(Alumno.id == student_id)
            )
        ).scalar_one()


async def _cleanup_user(user_id: str | None) -> bool:
    if not user_id:
        return True
    async with AsyncSessionLocal() as session:
        student_id = await session.scalar(
            select(Alumno.id).where(Alumno.user_id == user_id)
        )
        if student_id is not None:
            attempt_question_ids = select(IntentoPregunta.id).where(
                IntentoPregunta.alumno_id == student_id
            )
            await session.execute(
                delete(IntentoPaso).where(
                    IntentoPaso.intento_pregunta_id.in_(attempt_question_ids)
                )
            )
            await session.execute(
                delete(IntentoPregunta).where(IntentoPregunta.alumno_id == student_id)
            )
            await session.execute(
                delete(Intento).where(Intento.alumno_id == student_id)
            )
            await session.execute(
                delete(PoolAsignadoAlumno).where(
                    PoolAsignadoAlumno.alumno_id == student_id
                )
            )
            await session.execute(
                delete(ProgresoMaestria).where(
                    ProgresoMaestria.alumno_id == student_id
                )
            )
            await session.execute(delete(Alumno).where(Alumno.id == student_id))
        await session.execute(delete(User).where(User.id == user_id))
        await session.commit()
        remains = await session.scalar(
            select(func.count(User.id)).where(User.id == user_id)
        )
        return remains == 0


async def _complete_block(
    client: httpx.AsyncClient,
    headers: dict[str, str],
    module_id: int,
    level_id: int,
    evidence: JourneyEvidence,
) -> dict:
    max_answers = 30
    for _ in range(max_answers):
        question_response = await client.get(
            f"/fase4/modulo/{module_id}/nivel/{level_id}/pregunta",
            headers=headers,
        )
        _require_status(
            question_response,
            200,
            f"load block {module_id}/{level_id}",
        )
        payload = await _answer_payload(
            question_response.json(), module_id, level_id
        )
        answer_response = await client.post(
            "/fase4/responder", json=payload, headers=headers
        )
        _require_status(
            answer_response,
            200,
            f"answer block {module_id}/{level_id}",
        )
        answer = answer_response.json()
        evidence.requests_answered += 1
        if not answer["es_correcta"]:
            raise RuntimeError(
                f"Oracle answer was rejected for block {module_id}/{level_id}."
            )
        if answer["bloque_completado"]:
            evidence.blocks_completed += 1
            return answer
    raise RuntimeError(
        f"Block {module_id}/{level_id} did not complete after {max_answers} answers."
    )


async def run_journey(api_base_url: str) -> JourneyEvidence:
    database = _assert_test_database()
    evidence = JourneyEvidence(database=database, api_base_url=api_base_url)
    synthetic_user_id: str | None = None
    unique = uuid.uuid4().hex[:12]
    email = f"codex-fase4-{unique}@example.test"
    password = f"Fase4-{unique}-Safe9!"

    try:
        async with httpx.AsyncClient(base_url=api_base_url, timeout=30.0) as client:
            unauthorized = await client.get("/fase4/dashboard")
            evidence.unauthorized_status = unauthorized.status_code
            if unauthorized.status_code not in (401, 403):
                raise RuntimeError(
                    f"Unauthenticated dashboard returned {unauthorized.status_code}."
                )

            register = await client.post(
                "/auth/register",
                json={"username": f"codex_fase4_{unique}", "email": email, "password": password},
            )
            _require_status(register, 200, "register synthetic user")
            token = register.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            async with AsyncSessionLocal() as session:
                synthetic_user_id = await session.scalar(
                    select(User.id).where(User.email == email)
                )
            if synthetic_user_id is None:
                raise RuntimeError("Registered user was not persisted.")
            student_id = await _set_student_phase4(synthetic_user_id)

            dashboard = await client.get("/fase4/dashboard", headers=headers)
            _require_status(dashboard, 200, "initial dashboard")

            locked = await client.get(
                "/fase4/modulo/1/nivel/2/pregunta", headers=headers
            )
            evidence.locked_status = locked.status_code
            _require_status(locked, 403, "locked M1N2 access")
            if await _progress_exists(student_id, 102):
                raise RuntimeError("Locked access created phantom progress for section 102.")

            first_question = await client.get(
                "/fase4/modulo/1/nivel/1/pregunta", headers=headers
            )
            _require_status(first_question, 200, "load first M1N1 question")
            first_payload = await _answer_payload(first_question.json(), 1, 1)

            mismatch_payload = dict(first_payload, nivel_id=2)
            mismatch = await client.post(
                "/fase4/responder", json=mismatch_payload, headers=headers
            )
            evidence.cross_section_status = mismatch.status_code
            _require_status(mismatch, 409, "cross-section answer")
            if await _progress_exists(student_id, 102):
                raise RuntimeError("Cross-section answer created phantom progress.")

            concurrent = await asyncio.gather(
                client.post("/fase4/responder", json=first_payload, headers=headers),
                client.post("/fase4/responder", json=first_payload, headers=headers),
            )
            evidence.concurrent_statuses = tuple(
                response.status_code for response in concurrent
            )
            for response in concurrent:
                _require_status(response, 200, "concurrent double-submit")
            evidence.concurrent_credited_answers = await _credited_answers(
                student_id, 101
            )
            if evidence.concurrent_credited_answers != 1:
                raise RuntimeError(
                    "Concurrent duplicate answer changed credited mastery more than once."
                )
            evidence.requests_answered += 2

            ordered_blocks = tuple(
                get_block(module_id, level_id)
                for module_id in MODULE_IDS
                for level_id in PRACTICE_LEVEL_IDS + CHALLENGE_LEVEL_IDS
            ) + (MIXED_BLOCK,)
            for block in ordered_blocks:
                result = await _complete_block(
                    client,
                    headers,
                    block.module_id,
                    block.level_id,
                    evidence,
                )
                if block.section == MIXED_SECTION and not result["fase_completada"]:
                    raise RuntimeError("Mixed mastery did not complete Phase 4.")
                if block.section != MIXED_SECTION and result["fase_completada"]:
                    raise RuntimeError("A prerequisite block completed Phase 4 early.")

                if block.section == ordered_blocks[-2].section:
                    before_mixed = await client.get(
                        "/fase4/dashboard", headers=headers
                    )
                    _require_status(before_mixed, 200, "dashboard before mixed")
                    evidence.mixed_state_before = before_mixed.json()[
                        "desafio_mixto_estado"
                    ]
                    if evidence.mixed_state_before != "disponible":
                        raise RuntimeError(
                            "Mixed challenge was not available after 24 prerequisites."
                        )

            final_dashboard = await client.get("/fase4/dashboard", headers=headers)
            _require_status(final_dashboard, 200, "dashboard after mixed")
            evidence.mixed_state_after = final_dashboard.json()[
                "desafio_mixto_estado"
            ]
            if evidence.mixed_state_after != "completado":
                raise RuntimeError("Dashboard did not report completed mixed challenge.")

            graduation = await client.post("/fase4/graduate", headers=headers)
            _require_status(graduation, 200, "Phase 4 graduation")
            evidence.graduated_phase_order = await _student_phase_order(student_id)
            if evidence.graduated_phase_order != 5:
                raise RuntimeError("Graduation did not assign canonical Phase 5.")

            repeated = await client.post("/fase4/graduate", headers=headers)
            _require_status(repeated, 200, "repeated Phase 4 graduation")
            evidence.repeated_graduation_phase_order = await _student_phase_order(
                student_id
            )
            if evidence.repeated_graduation_phase_order != 5:
                raise RuntimeError("Repeated graduation advanced beyond Phase 5.")
    finally:
        evidence.synthetic_user_removed = await _cleanup_user(synthetic_user_id)

    if not evidence.synthetic_user_removed:
        raise RuntimeError("Synthetic user cleanup failed.")
    return evidence


async def main(api_base_url: str, output_path: str | None) -> int:
    evidence = await run_journey(api_base_url.rstrip("/"))
    rendered = json.dumps(asdict(evidence), ensure_ascii=False, indent=2)
    print(rendered)
    if output_path:
        from pathlib import Path

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Evidence written to: {path.resolve()}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base-url", default="http://127.0.0.1:8010")
    parser.add_argument("--output")
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.api_base_url, args.output)))
