import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select, func
from app.db.session import AsyncSessionLocal
from app.models.sql_models import Pregunta, Alumno
from app.models.progreso import ProgresoMaestria, PoolAsignadoAlumno, Intento, ConfiguracionProgreso

async def main():
    async with AsyncSessionLocal() as session:
        # 1. Preguntas fase 4
        res_p_act = await session.execute(
            select(func.count(Pregunta.id)).where(Pregunta.fase_id == 4, func.upper(Pregunta.estado).in_(['ACTIVO', 'ACTIVO']))
        )
        count_p_act = res_p_act.scalar_one()

        res_p_inact = await session.execute(
            select(func.count(Pregunta.id)).where(Pregunta.fase_id == 4, func.upper(Pregunta.estado) == 'INACTIVO')
        )
        count_p_inact = res_p_inact.scalar_one()

        res_p_desafios = await session.execute(
            select(func.count(Pregunta.id)).where(Pregunta.fase_id == 4, Pregunta.seccion >= 1000, func.upper(Pregunta.estado) == 'ACTIVO')
        )
        count_p_desafios = res_p_desafios.scalar_one()

        res_p_practica = await session.execute(
            select(func.count(Pregunta.id)).where(Pregunta.fase_id == 4, Pregunta.seccion < 1000, func.upper(Pregunta.estado) == 'ACTIVO')
        )
        count_p_practica = res_p_practica.scalar_one()

        # 2. Progreso maestria fase 4 (filas a borrar)
        res_pm = await session.execute(
            select(func.count(ProgresoMaestria.id)).where(ProgresoMaestria.fase_id == 4)
        )
        count_pm = res_pm.scalar_one()

        # 3. Pool asignado alumno fase 4 (filas a borrar)
        res_pool = await session.execute(
            select(func.count(PoolAsignadoAlumno.id)).where(PoolAsignadoAlumno.fase_id == 4)
        )
        count_pool = res_pool.scalar_one()

        # 4. Alumnos con fase_actual_id > 4 y fase_actual_id == 4
        res_al_gt4 = await session.execute(
            select(func.count(Alumno.id)).where(Alumno.fase_actual_id > 4)
        )
        count_al_gt4 = res_al_gt4.scalar_one()

        res_al_eq4 = await session.execute(
            select(func.count(Alumno.id)).where(Alumno.fase_actual_id == 4)
        )
        count_al_eq4 = res_al_eq4.scalar_one()

        res_al_total = await session.execute(select(func.count(Alumno.id)))
        count_al_total = res_al_total.scalar_one()

        # 5. Intentos fase 4 (NO SE TOCAN)
        res_int = await session.execute(
            select(func.count(Intento.id)).where(Intento.fase_id == 4)
        )
        count_int = res_int.scalar_one()

        # 6. Configuracion progreso fase 4
        res_cfg = await session.execute(
            select(func.count(ConfiguracionProgreso.id)).where(ConfiguracionProgreso.fase_id == 4)
        )
        count_cfg = res_cfg.scalar_one()

        print("=" * 80)
        print("ESTADO ACTUAL DE LA BASE DE DATOS PARA FASE 4 TJS")
        print("=" * 80)
        print(f"Total preguntas ACTIVAS (TJS Nuevas) en Fase 4: {count_p_act}")
        print(f"  - Preguntas de desafío activas (seccion >= 1000): {count_p_desafios}")
        print(f"  - Preguntas de práctica activas (seccion < 1000): {count_p_practica}")
        print(f"Total preguntas INACTIVAS (Viejas reservadas para FK/historial): {count_p_inact}")
        print("-" * 80)
        print("FILAS A BORRAR EN REINICIO DE PROGRESO (PASO 5):")
        print(f"  - Filas en 'progreso_maestria' (fase_id = 4): {count_pm}")
        print(f"  - Filas en 'pool_asignado_alumno' (fase_id = 4): {count_pool}")
        print("-" * 80)
        print("ALUMNOS AFECTADOS EN REINICIO DE PROGRESO (PASO 5):")
        print(f"  - Alumnos con fase_actual_id > 4 (serán reajustados a 4): {count_al_gt4}")
        print(f"  - Alumnos con fase_actual_id == 4: {count_al_eq4}")
        print(f"  - Total alumnos en el sistema: {count_al_total}")
        print("-" * 80)
        print("HISTORIAL INTENTOS (INTACTO, NUNCA SE TOCA):")
        print(f"  - Total filas en 'intentos' (fase_id = 4): {count_int}")
        print(f"  - Bloques de 'configuracion_progreso' actuales en Fase 4: {count_cfg}")
        print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
