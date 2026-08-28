"""Normalize every implemented practice level to the shared 10-correct goal."""

import asyncio
import json

from sqlalchemy import and_, case, func, or_, select, text, update

from app.core.progression import PRACTICE_REQUIRED_CORRECT_ANSWERS
from app.db.session import AsyncSessionLocal
from app.models.sql_models import (
    ConfiguracionProgreso,
    EstadoProgresoEnum,
    PlatformSettings,
    ProgresoMaestria,
)


IMPLEMENTED_PHASE_IDS = tuple(range(1, 9))


def _practice_scope(model):
    return and_(
        model.fase_id.in_(IMPLEMENTED_PHASE_IDS),
        or_(
            model.seccion == 0,
            model.seccion.between(100, 999),
            and_(model.fase_id == 1, model.seccion == 1),
        ),
    )


async def normalize_practice_progress_goal() -> dict:
    """Apply the practice goal without modifying questions, attempts, or challenges."""
    async with AsyncSessionLocal() as session:
        legacy_state_result = await session.execute(
            text(
                "UPDATE progreso_maestria "
                "SET estado = 'APROBADO' "
                "WHERE lower(estado) = 'aprobado' AND estado <> 'APROBADO'"
            )
        )
        config_before = await session.scalar(
            select(func.count(ConfiguracionProgreso.id)).where(
                _practice_scope(ConfiguracionProgreso),
                ConfiguracionProgreso.cantidad_requerida
                != PRACTICE_REQUIRED_CORRECT_ANSWERS,
            )
        )
        progress_over_goal_before = await session.scalar(
            select(func.count(ProgresoMaestria.id)).where(
                _practice_scope(ProgresoMaestria),
                ProgresoMaestria.aciertos_acumulados
                > PRACTICE_REQUIRED_CORRECT_ANSWERS,
            )
        )

        await session.execute(
            update(ConfiguracionProgreso)
            .where(_practice_scope(ConfiguracionProgreso))
            .values(
                cantidad_requerida=PRACTICE_REQUIRED_CORRECT_ANSWERS,
                porcentaje_aprobacion=100,
                ultima_modificacion=func.now(),
            )
        )

        goal = PRACTICE_REQUIRED_CORRECT_ANSWERS
        await session.execute(
            update(ProgresoMaestria)
            .where(_practice_scope(ProgresoMaestria))
            .values(
                aciertos_acumulados=func.least(
                    ProgresoMaestria.aciertos_acumulados,
                    goal,
                ),
                porcentaje_actual=case(
                    (ProgresoMaestria.estado == EstadoProgresoEnum.APROBADO, 100),
                    else_=func.least(100, ProgresoMaestria.aciertos_acumulados * 10),
                ),
                estado=case(
                    (
                        ProgresoMaestria.aciertos_acumulados >= goal,
                        EstadoProgresoEnum.APROBADO,
                    ),
                    else_=ProgresoMaestria.estado,
                ),
                fecha_aprobacion=case(
                    (
                        and_(
                            ProgresoMaestria.aciertos_acumulados >= goal,
                            ProgresoMaestria.fecha_aprobacion.is_(None),
                        ),
                        func.now(),
                    ),
                    else_=ProgresoMaestria.fecha_aprobacion,
                ),
            )
        )

        settings = await session.scalar(
            select(PlatformSettings).where(PlatformSettings.key == "pedagogy_config")
        )
        if settings:
            updated_settings = dict(settings.value or {})
            updated_settings["questionsPerPhase"] = goal
            practice_settings = dict(updated_settings.get("practica_libre") or {})
            practice_settings["cantidad_requerida"] = goal
            practice_settings["porcentaje_aprobacion"] = 100
            updated_settings["practica_libre"] = practice_settings
            settings.value = updated_settings

        await session.commit()

        invalid_configs = await session.scalar(
            select(func.count(ConfiguracionProgreso.id)).where(
                _practice_scope(ConfiguracionProgreso),
                or_(
                    ConfiguracionProgreso.cantidad_requerida != goal,
                    ConfiguracionProgreso.porcentaje_aprobacion != 100,
                ),
            )
        )
        progress_over_goal_after = await session.scalar(
            select(func.count(ProgresoMaestria.id)).where(
                _practice_scope(ProgresoMaestria),
                ProgresoMaestria.aciertos_acumulados > goal,
            )
        )

        result = {
            "phase_ids": list(IMPLEMENTED_PHASE_IDS),
            "practice_goal": goal,
            "legacy_progress_states_normalized": legacy_state_result.rowcount or 0,
            "configs_changed": config_before or 0,
            "progress_rows_clamped": progress_over_goal_before or 0,
            "invalid_configs_after": invalid_configs or 0,
            "progress_rows_over_goal_after": progress_over_goal_after or 0,
        }
        if result["invalid_configs_after"] or result["progress_rows_over_goal_after"]:
            raise RuntimeError(f"Practice progression normalization failed: {result}")
        return result


if __name__ == "__main__":
    print(json.dumps(asyncio.run(normalize_practice_progress_goal()), indent=2))
