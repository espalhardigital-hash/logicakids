import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select, update, func, delete
from app.db.session import AsyncSessionLocal
from app.models.sql_models import Pregunta, Alumno, StatusEnum, ConfiguracionProgreso
from app.models.progreso import ProgresoMaestria, PoolAsignadoAlumno, Intento
from app.fase2.models import NivelTeoria
from app.fase4.seed import (
    FASE4_ID,
    seed_teoria_niveles,
    seed_configuracion_progreso,
    seed_preguntas_practica,
    seed_preguntas_desafios,
)

from sqlalchemy import select, update, func, delete, text

async def step2_inactivate_old_questions(session):
    print("--- PASO 2: Inactivando preguntas viejas de Fase 4 (Aditivo) ---")
    result = await session.execute(
        text("SELECT count(*) FROM preguntas WHERE fase_id = 4 AND (estado = 'ACTIVO' OR estado = 'activo')")
    )
    before_count = result.scalar_one()
    
    await session.execute(
        text("UPDATE preguntas SET estado = 'INACTIVO' WHERE fase_id = 4 AND (estado = 'ACTIVO' OR estado = 'activo')")
    )
    await session.commit()

    result_after = await session.execute(
        text("SELECT count(*) FROM preguntas WHERE fase_id = 4 AND (estado = 'ACTIVO' OR estado = 'activo')")
    )
    after_count = result_after.scalar_one()

    result_inact = await session.execute(
        text("SELECT count(*) FROM preguntas WHERE fase_id = 4 AND (estado = 'INACTIVO' OR estado = 'inactivo')")
    )
    inact_count = result_inact.scalar_one()

    print(f"Preguntas activas antes de inactivar: {before_count}")
    print(f"Preguntas activas después de inactivar: {after_count}")
    print(f"Preguntas inactivas conservadas (FKs preservadas): {inact_count}")

async def step3_and_4_seed_tjs(session):
    print("--- PASOS 3 Y 4: Sembrando preguntas TJS y actualizando configuracion_progreso ---")
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE4_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE4_ID))
    await session.commit()
    await seed_teoria_niveles(session)
    await seed_configuracion_progreso(session)
    await seed_preguntas_practica(session)
    await seed_preguntas_desafios(session)
    print("Siembra TJS completada exitosamente.")

async def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    
    async with AsyncSessionLocal() as session:
        if mode == "execute_steps_2_3_4":
            await step2_inactivate_old_questions(session)
            await step3_and_4_seed_tjs(session)
        elif mode == "execute_step_5_reset_progress":
            print("--- PASO 5: Ejecutando reinicio de progreso de Fase 4 ---")
            
            # Count before
            res_pm = await session.execute(select(func.count(ProgresoMaestria.id)).where(ProgresoMaestria.fase_id == FASE4_ID))
            count_pm = res_pm.scalar_one()
            
            res_pool = await session.execute(select(func.count(PoolAsignadoAlumno.id)).where(PoolAsignadoAlumno.fase_id == FASE4_ID))
            count_pool = res_pool.scalar_one()

            res_al = await session.execute(select(func.count(Alumno.id)).where(Alumno.fase_actual_id > 4))
            count_al = res_al.scalar_one()

            # Execute deletes & updates
            await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE4_ID))
            await session.execute(delete(ProgresoMaestria).where(ProgresoMaestria.fase_id == FASE4_ID))
            await session.execute(
                update(Alumno).where(Alumno.fase_actual_id > 4).values(fase_actual_id=4)
            )
            await session.commit()

            print(f"RESULTADO PASO 5:")
            print(f"  - Filas borradas en progreso_maestria: {count_pm}")
            print(f"  - Filas borradas en pool_asignado_alumno: {count_pool}")
            print(f"  - Alumnos reajustados a Fase 4: {count_al}")
            print("Reinicio de progreso completado sin tocar intentos.")

if __name__ == "__main__":
    asyncio.run(main())
