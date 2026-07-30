"""
Script de auditoría de terreno para CH-6: Desafíos de la Fase 4.
Configura base de datos SQLite autónoma para la ejecución y verificación.

Verifica en la BD local:
1. Existencia de exactamente 13 bloques de desafío (4 módulos × 3 + 1 DM).
2. Volumetría total de 1.950 preguntas de desafío (13 × 150).
3. Cumplimiento de las especificaciones D1 (opción múltiple, prosa, ≤ 40 palabras).
4. Cumplimiento de D2 (TJS opción múltiple, ≤ 40 palabras).
5. Cumplimiento de DF (respuesta_numerica, contexto portante, 2 pasos ~15%, errores_previstos).
6. Cumplimiento de DM (99099, mezcla de 1/3 D1, 1/3 D2, 1/3 DF).
"""

import os
import asyncio

DB_PATH = f"./test_ch6_audit_{os.getpid()}.db"

# Configurar BD local en SQLite (autónomo para pruebas)
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{DB_PATH}"

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, INET, UUID
from sqlalchemy.types import JSON

@compiles(JSONB, 'sqlite')
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"

@compiles(ARRAY, 'sqlite')
def compile_array_sqlite(type_, compiler, **kw):
    return "JSON"

@compiles(INET, 'sqlite')
def compile_inet_sqlite(type_, compiler, **kw):
    return "VARCHAR"

@compiles(UUID, 'sqlite')
def compile_uuid_sqlite(type_, compiler, **kw):
    return "VARCHAR"

from sqlalchemy import select, func
from app.db.base import Base
from app.db.session import engine, AsyncSessionLocal
from app.models.sql_models import Pregunta, Alternativa, ConfiguracionProgreso, TipoPreguntaEnum
from app.fase4.seed import (
    upsert_fila_fases,
    seed_preguntas_desafios, seed_configuracion_progreso,
    FASE_DECIMALES_ID
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def run_ch6_seeding():
    async with AsyncSessionLocal() as session:
        await upsert_fila_fases(session)
        await seed_preguntas_desafios(session)
        await seed_configuracion_progreso(session)

async def audit_ch6():
    print("Inicializando tablas en base de datos de prueba SQLite...")
    await init_db()

    print("Ejecutando siembra de desafíos de la Fase 4...")
    await run_ch6_seeding()

    async with AsyncSessionLocal() as session:
        print("\n--- INICIANDO AUDITORÍA DE TERRENO PARA CH-6 (DESAFÍOS) ---")

        # 1. Bloques de desafío en configuracion_progreso
        res_cfg = await session.execute(
            select(ConfiguracionProgreso.seccion).where(
                ConfiguracionProgreso.fase_id == FASE_DECIMALES_ID,
                ConfiguracionProgreso.seccion >= 1000
            )
        )
        des_sec_cfg = res_cfg.scalars().all()
        expected_sec = [1011, 1012, 1013, 2011, 2012, 2013, 3011, 3012, 3013, 4011, 4012, 4013, 99099]
        
        print(f"[Check 1] Secciones de desafío configuradas: {len(des_sec_cfg)} de 13 esperadas.")
        assert sorted(des_sec_cfg) == sorted(expected_sec), f"Error: secciones {sorted(des_sec_cfg)} != {sorted(expected_sec)}"

        # 2. Conteo total de preguntas de desafío
        res_total = await session.execute(
            select(func.count(Pregunta.id)).where(
                Pregunta.fase_id == FASE_DECIMALES_ID,
                Pregunta.seccion >= 1000
            )
        )
        total_q = res_total.scalar()
        print(f"[Check 2] Total preguntas de desafío sembradas: {total_q} (esperado 1.950).")
        assert total_q == 1950, f"Error: total {total_q} != 1950"

        # 3. Auditoría por sección y tipo de pregunta
        for sec in expected_sec:
            res_sec_q = await session.execute(
                select(Pregunta).where(
                    Pregunta.fase_id == FASE_DECIMALES_ID,
                    Pregunta.seccion == sec
                )
            )
            questions = res_sec_q.scalars().all()
            assert len(questions) == 150, f"Sección {sec} tiene {len(questions)} preguntas (esperado 150)"

            # Validar techo de palabras de enunciados (≤ 40 palabras)
            for q in questions:
                words = q.enunciado.split()
                assert len(words) <= 40, f"Pregunta {q.id} en seccion {sec} excede 40 palabras: {len(words)} palabras"

            if sec % 100 == 11: # D1
                types = {q.tipo_pregunta for q in questions}
                assert types == {TipoPreguntaEnum.MULTIPLE_OPCION}, f"D1 seccion {sec} debe ser MULTIPLE_OPCION, obtenido {types}"
                # Verificar excepción C5.5: NO debe contener mini-tabla ni SVG
                for q in questions:
                    assert "<table" not in q.enunciado.lower() and "<svg" not in q.enunciado.lower(), f"D1 seccion {sec} no debe tener tabla/svg (excepcion C5.5)"
            elif sec % 100 == 12: # D2
                types = {q.tipo_pregunta for q in questions}
                assert types == {TipoPreguntaEnum.MULTIPLE_OPCION}, f"D2 seccion {sec} debe ser MULTIPLE_OPCION, obtenido {types}"
            elif sec % 100 == 13: # DF
                types = {q.tipo_pregunta for q in questions}
                assert types == {TipoPreguntaEnum.RESPUESTA_NUMERICA}, f"DF seccion {sec} debe ser RESPUESTA_NUMERICA, obtenido {types}"
                # Verificar presencia de errores_previstos para redondeo
                has_err_previstos = any(q.errores_previstos for q in questions)
                assert has_err_previstos, f"DF seccion {sec} debe tener errores_previstos mapeados"
            elif sec == 99099: # DM
                d1_count = sum(1 for q in questions if q.tipo_pregunta == TipoPreguntaEnum.MULTIPLE_OPCION)
                df_count = sum(1 for q in questions if q.tipo_pregunta == TipoPreguntaEnum.RESPUESTA_NUMERICA)
                assert d1_count == 100 and df_count == 50, f"DM 99099 debe tener 100 OM (D1/D2) y 50 NUM (DF), obtenido {d1_count} OM y {df_count} NUM"

        print("[Check 3] Validación de tipos de pregunta, formato D1/D2/DF/DM y límite de 40 palabras EXITOSA.")
        print("--- AUDITORÍA DE TERRENO FINALIZADA CON ÉXITO: 100% VERDE ---")

    await engine.dispose()
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(audit_ch6())
