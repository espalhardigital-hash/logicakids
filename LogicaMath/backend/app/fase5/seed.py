"""
Seeder autónomo y determinista para la Fase 5: Fracciones, Porcentajes y Proporciones.
Cumple estrictamente con docs/reestructuracionGeneralFases.md y deep_analise_pro §25.4.
"""

import asyncio
import json
import os
import random
import sys
from datetime import datetime
from typing import Dict, Any, List

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.sql_models import (
    Fase, Pregunta, Alternativa, ConfiguracionProgreso,
    StatusEnum, OperacionEnum, TipoPreguntaEnum, TipoErrorEnum,
    Intento, PoolAsignadoAlumno
)
from app.fase2.models import NivelTeoria, IntentoPregunta
from app.fase5.theory_examples import obtener_ejemplos_expandidos_fase5
from app.fase5.compositor_fase5 import CompositorFase5

FASE5_ID = 5
_COMPOSITOR = CompositorFase5()


def _is_numeric_answer(resp_str: str) -> bool:
    clean = resp_str.lstrip('-').replace('.', '', 1).replace(',', '', 1).strip()
    return clean.isdigit()


async def upsert_fila_fase5(session: AsyncSession):
    res = await session.execute(select(Fase).where(Fase.id == FASE5_ID))
    fase = res.scalar_one_or_none()
    if not fase:
        fase = Fase(
            id=FASE5_ID,
            nombre="Fracciones, Porcentajes y Proporciones",
            descripcion="Representación, operaciones de fracciones, porcentajes y regla de tres",
            orden=5,
            estado=StatusEnum.ACTIVO
        )
        session.add(fase)
    else:
        fase.nombre = "Fracciones, Porcentajes y Proporciones"
        fase.descripcion = "Representación, operaciones de fracciones, porcentajes y regla de tres"
        fase.orden = 5
        fase.estado = StatusEnum.ACTIVO
    await session.flush()


async def clear_fase5_data(session: AsyncSession):
    print("Purging existing Fase 5 data for clean seeding...")

    result = await session.execute(select(Pregunta.id).where(Pregunta.fase_id == FASE5_ID))
    pregunta_ids_list = result.scalars().all()

    if pregunta_ids_list:
        await session.execute(delete(IntentoPregunta).where(IntentoPregunta.pregunta_id.in_(pregunta_ids_list)))
        await session.execute(delete(Intento).where(Intento.pregunta_id.in_(pregunta_ids_list)))
        await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.pregunta_id.in_(pregunta_ids_list)))

    await session.execute(delete(Intento).where(Intento.fase_id == FASE5_ID))
    await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE5_ID))

    if pregunta_ids_list:
        await session.execute(delete(Alternativa).where(Alternativa.pregunta_id.in_(pregunta_ids_list)))

    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE5_ID))
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE5_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE5_ID))
    await session.flush()


async def seed_teoria_fase5(session: AsyncSession):
    print("Sembrando NivelTeoria para Fase 5...")
    modulos_info = [
        (1, "La Fracción Visual", "Lectura, equivalencias y partes de un todo"),
        (2, "Fracción de Cantidad", "Cálculo de fracciones sobre grupos y totalidades"),
        (3, "Porcentajes Rápidos y Promedios", "Cálculo de porcentajes, descuentos y promedios"),
        (4, "Razón y Mezclas", "Proporcionalidad directa, razones y porcentajes en mezclas"),
    ]

    for mod_id, mod_nombre, mod_desc in modulos_info:
        for niv_id in (1, 2, 3):
            ejemplos = obtener_ejemplos_expandidos_fase5(mod_id, niv_id)
            teoria = NivelTeoria(
                fase_id=FASE5_ID,
                modulo_id=mod_id,
                nivel_id=niv_id,
                titulo=f"{mod_nombre} - Nivel {niv_id}",
                texto_descubrimiento=f"Descubrimiento pedagógico de {mod_nombre}, Nivel {niv_id}",
                diccionario={"concepto": "Fracciones y Razones"},
                advertencia="Recuerda simplificar y verificar las unidades",
                ejemplos=ejemplos,
                interactivos=[{"tipo": "simulador", "modulo": mod_id, "nivel": niv_id}]
            )
            session.add(teoria)
    await session.flush()


async def seed_configuraciones_fase5(session: AsyncSession):
    print("Sembrando ConfiguracionProgreso para Fase 5...")
    orden = 1

    # 1. Configuración global / práctica libre
    cfg_global = ConfiguracionProgreso(
        fase_id=FASE5_ID,
        seccion=0,
        operacion=OperacionEnum.MIXTA,
        porcentaje_aprobacion=100.0,
        cantidad_requerida=15,
        errores_tolerados=2,
        orden_desbloqueo=orden,
        tipo_feedback="detallado",
        usa_cronometro=False,
        tiempo_default_segundos=0,
        pistas_permitidas=0,
        penalizacion_pista_segundos=0
    )
    session.add(cfg_global)
    orden += 1

    # 2. Bloques de práctica (12 bloques)
    for mod_id in (1, 2, 3, 4):
        for niv_id in (1, 2, 3):
            sec = mod_id * 100 + niv_id
            cfg = ConfiguracionProgreso(
                fase_id=FASE5_ID,
                seccion=sec,
                operacion=OperacionEnum.MIXTA,
                porcentaje_aprobacion=100.0,
                cantidad_requerida=10,
                errores_tolerados=2,
                orden_desbloqueo=orden,
                tipo_feedback="detallado",
                usa_cronometro=False,
                tiempo_default_segundos=0,
                pistas_permitidas=0,
                penalizacion_pista_segundos=0
            )
            session.add(cfg)
            orden += 1

    # 3. Bloques de desafíos (12 bloques)
    time_map = {11: 25, 12: 40, 13: 50}
    for mod_id in (1, 2, 3, 4):
        for niv_id in (11, 12, 13):
            sec = mod_id * 1000 + niv_id
            cfg = ConfiguracionProgreso(
                fase_id=FASE5_ID,
                seccion=sec,
                operacion=OperacionEnum.MIXTA,
                porcentaje_aprobacion=100.0,
                cantidad_requerida=15,
                errores_tolerados=2,
                orden_desbloqueo=orden,
                tipo_feedback="simple",
                usa_cronometro=True,
                tiempo_default_segundos=time_map[niv_id],
                pistas_permitidas=1,
                penalizacion_pista_segundos=5
            )
            session.add(cfg)
            orden += 1

    # 4. Desafío mixto final (1 bloque)
    cfg_mixto = ConfiguracionProgreso(
        fase_id=FASE5_ID,
        seccion=99099,
        operacion=OperacionEnum.MIXTA,
        porcentaje_aprobacion=100.0,
        cantidad_requerida=20,
        errores_tolerados=2,
        orden_desbloqueo=orden,
        tipo_feedback="simple",
        usa_cronometro=True,
        tiempo_default_segundos=60,
        pistas_permitidas=2,
        penalizacion_pista_segundos=5
    )
    session.add(cfg_mixto)
    await session.flush()


async def seed_preguntas_fase5(session: AsyncSession):
    print("Generando y sembrando preguntas de Fase 5 con CompositorFase5...")

    # 1. Sembrar preguntas de práctica (12 bloques x 60 preguntas = 720)
    for mod_id in (1, 2, 3, 4):
        for niv_id in (1, 2, 3):
            sec = mod_id * 100 + niv_id
            q_count = 0
            for fam_idx in range(12):
                for var_idx in range(5):
                    seed_val = 500000 + sec * 100 + fam_idx * 5 + var_idx
                    preg_data = _COMPOSITOR.componer_pregunta_practica(
                        modulo_id=mod_id,
                        nivel_id=niv_id,
                        fam_idx=fam_idx,
                        var_idx=var_idx,
                        seed_val=seed_val
                    )

                    ans_str = preg_data["respuesta_correcta"]
                    is_num = _is_numeric_answer(ans_str)
                    tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA if is_num else TipoPreguntaEnum.MULTIPLE_OPCION
                    padre_id = f"f5_m{mod_id}_l{niv_id}_fam_{fam_idx:03d}"

                    datos_num = dict(preg_data["datos_numericos"])
                    datos_num["variante"] = var_idx

                    preg = Pregunta(
                        fase_id=FASE5_ID,
                        seccion=sec,
                        operacion=OperacionEnum.MIXTA,
                        tipo_pregunta=tipo_preg,
                        enunciado=preg_data["enunciado"],
                        respuesta_correcta=ans_str,
                        explicacion_paso_a_paso={"pasos": [{"orden": 1, "texto": preg_data["explicacion"]}]},
                        datos_numericos=datos_num,
                        estructura_padre_id=padre_id,
                        estado=StatusEnum.ACTIVO
                    )
                    session.add(preg)
                    await session.flush()

                    # Opciones de respuesta para opción múltiple con metadatos de error pedagógico
                    opciones_meta = preg_data.get("opciones_meta", [])
                    if opciones_meta:
                        for orden_opt, meta in enumerate(opciones_meta):
                            alt = Alternativa(
                                pregunta_id=preg.id,
                                texto=meta["texto"],
                                es_correcta=meta["es_correcta"],
                                tipo_error=meta.get("tipo_error") if not meta["es_correcta"] else None,
                                feedback_error=meta.get("feedback_error") if not meta["es_correcta"] else None,
                                orden=orden_opt
                            )
                            session.add(alt)
                    else:
                        for orden_opt, op_txt in enumerate(preg_data["opciones"]):
                            alt = Alternativa(
                                pregunta_id=preg.id,
                                texto=op_txt,
                                es_correcta=(op_txt == ans_str),
                                orden=orden_opt
                            )
                            session.add(alt)

                    q_count += 1
            print(f"  ✓ Módulo {mod_id} Nivel {niv_id} (sección {sec}): {q_count} preguntas sembradas.")

    # 2. Sembrar preguntas de desafíos (12 bloques x 30 preguntas = 360)
    for mod_id in (1, 2, 3, 4):
        for niv_id in (11, 12, 13):
            sec = mod_id * 1000 + niv_id
            target_niv = (niv_id - 10)  # Maps 11->1, 12->2, 13->3
            q_count = 0
            for fam_idx in range(6):
                for var_idx in range(5):
                    seed_val = 600000 + sec * 100 + fam_idx * 5 + var_idx
                    preg_data = _COMPOSITOR.componer_pregunta_practica(
                        modulo_id=mod_id,
                        nivel_id=target_niv,
                        fam_idx=fam_idx,
                        var_idx=var_idx,
                        seed_val=seed_val
                    )

                    ans_str = preg_data["respuesta_correcta"]
                    padre_id = f"f5_d{sec}_q{q_count:03d}"
                    datos_num = dict(preg_data["datos_numericos"])
                    datos_num["variante"] = var_idx

                    preg = Pregunta(
                        fase_id=FASE5_ID,
                        seccion=sec,
                        operacion=OperacionEnum.MIXTA,
                        tipo_pregunta=TipoPreguntaEnum.MULTIPLE_OPCION,
                        enunciado=f"[Desafío] {preg_data['enunciado']}",
                        respuesta_correcta=ans_str,
                        explicacion_paso_a_paso={"pasos": [{"orden": 1, "texto": preg_data["explicacion"]}]},
                        datos_numericos=datos_num,
                        estructura_padre_id=padre_id,
                        estado=StatusEnum.ACTIVO
                    )
                    session.add(preg)
                    await session.flush()

                    opciones_meta = preg_data.get("opciones_meta", [])
                    if opciones_meta:
                        for orden_opt, meta in enumerate(opciones_meta):
                            alt = Alternativa(
                                pregunta_id=preg.id,
                                texto=meta["texto"],
                                es_correcta=meta["es_correcta"],
                                tipo_error=meta.get("tipo_error") if not meta["es_correcta"] else None,
                                feedback_error=meta.get("feedback_error") if not meta["es_correcta"] else None,
                                orden=orden_opt
                            )
                            session.add(alt)
                    else:
                        for orden_opt, op_txt in enumerate(preg_data["opciones"]):
                            alt = Alternativa(
                                pregunta_id=preg.id,
                                texto=op_txt,
                                es_correcta=(op_txt == ans_str),
                                orden=orden_opt
                            )
                            session.add(alt)

                    q_count += 1
            print(f"  ✓ Desafío {sec}: {q_count} preguntas sembradas.")

    # 3. Sembrar desafío mixto final (60 preguntas)
    sec_mixto = 99099
    q_count = 0
    for mod_id in (1, 2, 3, 4):
        for niv_id in (1, 2, 3):
            for var_idx in range(5):
                seed_val = 700000 + mod_id * 1000 + niv_id * 100 + var_idx
                # fam_idx variaba con mod_id (constante para los 3 niveles y
                # las 5 variantes de un mismo módulo): las 60 preguntas del
                # examen final salían de solo 12 plantillas (1 por módulo x
                # nivel) en vez de las 72 disponibles. Al variar también con
                # niv_id y var_idx se recorren varias plantillas por bloque.
                fam_idx = niv_id * 5 + var_idx
                preg_data = _COMPOSITOR.componer_pregunta_practica(
                    modulo_id=mod_id,
                    nivel_id=niv_id,
                    fam_idx=fam_idx,
                    var_idx=var_idx,
                    seed_val=seed_val
                )

                ans_str = preg_data["respuesta_correcta"]
                padre_id = f"f5_mixto_q{q_count:03d}"
                datos_num = dict(preg_data["datos_numericos"])
                datos_num["variante"] = var_idx

                preg = Pregunta(
                    fase_id=FASE5_ID,
                    seccion=sec_mixto,
                    operacion=OperacionEnum.MIXTA,
                    tipo_pregunta=TipoPreguntaEnum.MULTIPLE_OPCION,
                    enunciado=f"[Desafío Mixto Final] {preg_data['enunciado']}",
                    respuesta_correcta=ans_str,
                    explicacion_paso_a_paso={"pasos": [{"orden": 1, "texto": preg_data["explicacion"]}]},
                    datos_numericos=datos_num,
                    estructura_padre_id=padre_id,
                    estado=StatusEnum.ACTIVO
                )
                session.add(preg)
                await session.flush()

                opciones_meta = preg_data.get("opciones_meta", [])
                if opciones_meta:
                    for orden_opt, meta in enumerate(opciones_meta):
                        alt = Alternativa(
                            pregunta_id=preg.id,
                            texto=meta["texto"],
                            es_correcta=meta["es_correcta"],
                            tipo_error=meta.get("tipo_error") if not meta["es_correcta"] else None,
                            feedback_error=meta.get("feedback_error") if not meta["es_correcta"] else None,
                            orden=orden_opt
                        )
                        session.add(alt)
                else:
                    for orden_opt, op_txt in enumerate(preg_data["opciones"]):
                        alt = Alternativa(
                            pregunta_id=preg.id,
                            texto=op_txt,
                            es_correcta=(op_txt == ans_str),
                            orden=orden_opt
                        )
                        session.add(alt)

                q_count += 1
    print(f"  ✓ Desafío Mixto Final (sección {sec_mixto}): {q_count} preguntas sembradas.")
    await session.flush()


async def run_fase5_seed(session: AsyncSession):
    print("=================================================================")
    print(" INICIANDO SIEMBRA REESTRUCTURADA DE FASE 5 (LogicaKids Pro)")
    print("=================================================================")
    await upsert_fila_fase5(session)
    await clear_fase5_data(session)
    await seed_teoria_fase5(session)
    await seed_configuraciones_fase5(session)
    await seed_preguntas_fase5(session)
    await session.commit()
    print("=================================================================")
    print(" ¡SIEMBRA DE FASE 5 COMPLETADA EXITOSAMENTE!")
    print("=================================================================")


if __name__ == "__main__":
    async def main():
        async with AsyncSessionLocal() as session:
            await run_fase5_seed(session)

    asyncio.run(main())
