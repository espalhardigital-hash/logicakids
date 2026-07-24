"""
Seeder autónomo y determinista para la Fase 5: Operatoria Decimal y Conversiones.
Cumple estrictamente con las Secciones 5, 6 y 12 de docs/reestructuraciondefases.md.

Volumetría:
  - 15 niveles en niveles_teoria_pool (NivelTeoria).
  - 7.200 preguntas de práctica (15 niveles × 120 familias × 4 variantes: 1 original + 3 espejo).
  - 2.400 preguntas de desafíos (16 bloques × 150 preguntas; 15 de módulo + 1 mixto 99099).
  - 32 filas en configuracion_progreso con errores_tolerados, pistas_permitidas y penalizacion_pista_segundos.

Reglas duras:
  - Cero apariciones de la palabra "perímetro" en Fase 5.
  - Cero MinIO / PNG (todo SVG inline vía app.utils.svg_figuras).
  - estructura_padre_id NUNCA NULL (f5_mX_lY_fam_ZZZ en práctica, f5_dSEC_qZZZ en desafíos).
  - Enunciados TJS ≤ 50 palabras de prosa, datos en mini-tabla/SVG, 1 pregunta al final.
  - Pistas en explicacion_paso_a_paso.pista (reencuadre sin nombrar operación ni resultado).
"""

import asyncio
import json
import os
import random
import re
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
from app.fase2.models import NivelTeoria, IntentoPregunta, IntentoPaso
from app.fase5.theory_data import FASE5_TEORIA_DATA
from app.utils.svg_figuras import (
    fig_rectangulo, fig_cuadrado, fig_triangulo, fig_L, fig_T,
    escalera_unidades, recta_numerica_decimal, tabla_datos, comparador_opciones,
    color_modulo
)

FASE5_ID = 5

CATALOGO_PATH = os.path.join(os.path.dirname(__file__), "data", "catalogo_fase5.json")

def _load_catalogo() -> Dict[str, Any]:
    with open(CATALOGO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

CATALOGO_DATA = _load_catalogo()

def _fmt_dec(val: float) -> str:
    """Formatea float a string con coma decimal (ej. 4.65 -> '4,65', 4.0 -> '4,00' si es dinero)."""
    if float(val).is_integer():
        return f"{int(val)}"
    return f"{round(val, 4)}".replace('.', ',')

def _fmt_money(val: float) -> str:
    """Formatea monto monetario con 2 decimales y coma (ej. 4.5 -> '4,50')."""
    return f"{val:.2f}".replace('.', ',')

def _is_numeric_answer(resp_str: str) -> bool:
    clean = resp_str.lstrip('-').replace('.', '', 1).replace(',', '', 1).strip()
    return clean.isdigit()

NOMBRES_POOL = ["Leo", "Emma", "Thiago", "Mía", "Hugo", "Alba", "Nina", "Bruno", "Salma", "Iker", "Zoe", "Dante", "Lía", "Owen", "Sofía"]

# ── 0. UPSERT FILA DE FASE 5 ──────────────────────────────────────────────────

async def upsert_fila_fases(session: AsyncSession):
    res = await session.execute(select(Fase).where(Fase.id == FASE5_ID))
    fase = res.scalar_one_or_none()
    if not fase:
        fase = Fase(
            id=FASE5_ID,
            nombre="Operatoria Decimal y Conversiones",
            descripcion="Suma, resta, multiplicación, división con decimales y conversiones de longitud, volumen y superficie",
            orden=5,
            estado=StatusEnum.ACTIVO
        )
        session.add(fase)
    else:
        fase.nombre = "Operatoria Decimal y Conversiones"
        fase.descripcion = "Suma, resta, multiplicación, división con decimales y conversiones de longitud, volumen y superficie"
        fase.orden = 5
        fase.estado = StatusEnum.ACTIVO
    await session.commit()
    print("Fase 5 en tabla `fases` asegurada.")

# ── 1. LIMPIEZA / PURGA IDEMPOTENTE ──────────────────────────────────────────

async def clear_fase5_data(session: AsyncSession):
    print("Purga de datos preexistentes de Fase 5 en cascada...")
    res = await session.execute(select(Pregunta.id).where(Pregunta.fase_id == FASE5_ID))
    p_ids = res.scalars().all()

    if p_ids:
        for chunk in [p_ids[i:i+1000] for i in range(0, len(p_ids), 1000)]:
            await session.execute(delete(Alternativa).where(Alternativa.pregunta_id.in_(chunk)))
            res_iq = await session.execute(select(IntentoPregunta.id).where(IntentoPregunta.pregunta_id.in_(chunk)))
            iq_ids = res_iq.scalars().all()
            if iq_ids:
                await session.execute(delete(IntentoPaso).where(IntentoPaso.intento_pregunta_id.in_(iq_ids)))
                await session.execute(delete(IntentoPregunta).where(IntentoPregunta.id.in_(iq_ids)))
            await session.execute(delete(Intento).where(Intento.pregunta_id.in_(chunk)))
            await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.pregunta_id.in_(chunk)))

    await session.execute(delete(Intento).where(Intento.fase_id == FASE5_ID))
    await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE5_ID))
    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE5_ID))
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE5_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE5_ID))
    await session.commit()
    print("Purga de Fase 5 completada.")

# ── 2. SIEMBRA DE TEORÍA (NivelTeoria) ───────────────────────────────────────

async def seed_teoria_niveles(session: AsyncSession):
    print("Sembrando los 15 guiones teóricos (niveles_teoria_pool)...")
    for t_data in FASE5_TEORIA_DATA:
        nt = NivelTeoria(
            fase_id=FASE5_ID,
            modulo_id=t_data["modulo_id"],
            nivel_id=t_data["nivel_id"],
            titulo=t_data["titulo"],
            texto_descubrimiento=t_data["texto_descubrimiento"] + "\n\n" + t_data.get("cuerpo_teoria", ""),
            advertencia=t_data["advertencia"],
            diccionario=t_data["diccionario"],
            ejemplos=t_data["ejemplos"],
            interactivos=t_data["interactivos"],
            revisado_admin=True,
            revisado_por="seed_fase5_macro"
        )
        session.add(nt)
    await session.commit()
    print("15 niveles teóricos sembrados con éxito.")

# ── 3. GENERADOR DE PRÁCTICA (7.200 preguntas = 15 niveles x 120 fam x 4) ─────

def _generate_practice_question(modulo_id: int, nivel_id: int, fam_idx: int, var_idx: int, seed_val: int) -> dict:
    rng = random.Random(seed_val)
    sec = modulo_id * 100 + nivel_id
    fam_id = f"f5_m{modulo_id}_l{nivel_id}_fam_{fam_idx:03d}"
    es_espejo = (var_idx > 0)
    personaje = NOMBRES_POOL[(fam_idx + var_idx) % len(NOMBRES_POOL)]

    escenarios_mod = [e for e in CATALOGO_DATA["escenarios"] if e["modulo_id"] == modulo_id]
    confusiones_mod = [c for c in CATALOGO_DATA["confusiones"] if c["modulo_id"] == modulo_id]
    esc = escenarios_mod[fam_idx % len(escenarios_mod)]

    # offset garantizando singularidad numérica para cada variante
    item_offset = (fam_idx * 4 + var_idx) * 0.07

    if modulo_id == 1:
        if nivel_id == 1:
            op_enum = OperacionEnum.SUMA
            a = round(1.20 + item_offset + rng.uniform(0.01, 0.05), 2)
            b = round(0.45 + (fam_idx * 0.03) + rng.uniform(0.01, 0.05), 2)
            ans_num = round(a + b, 2)
            ans_str = _fmt_money(ans_num)
            
            enunciado = (
                f"{personaje} compra dos productos en {esc['nombre'].lower()}: "
                f"uno por R$ {_fmt_money(a)} y otro por R$ {_fmt_money(b)}.<br/>"
                f"¿Cuánto paga en total?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Alineamos las comas verticales: {_fmt_money(a)} + {_fmt_money(b)}."},
                    {"orden": 2, "texto": f"Sumamos columna a columna: {_fmt_money(a)} + {_fmt_money(b)} = R$ {ans_str}."}
                ]
            }
            err_dict = {
                _fmt_money(ans_num + 1.0): "Revisa el acarreo en las décimas.",
                _fmt_money(round(a + b + 0.1, 2)): confusiones_mod[0]["feedback"]
            }

        elif nivel_id == 2:
            op_enum = OperacionEnum.RESTA
            a = round(15.0 + item_offset + rng.uniform(0.1, 0.4), 1)
            b = round(1.25 + (fam_idx * 0.02) + rng.uniform(0.01, 0.05), 2)
            if b >= a:
                b = round(a / 2, 2)
            ans_num = round(a - b, 2)
            ans_str = _fmt_money(ans_num)

            enunciado = (
                f"{personaje} tiene R$ {_fmt_money(a)} y gasta R$ {_fmt_money(b)} en {esc['nombre'].lower()}.<br/>"
                f"¿Cuánto dinero le queda?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Completamos con ceros: {_fmt_money(a)} − {_fmt_money(b)}."},
                    {"orden": 2, "texto": f"Restamos pidiendo prestado si hace falta: {_fmt_money(a)} − {_fmt_money(b)} = R$ {ans_str}."}
                ]
            }
            err_dict = {
                _fmt_money(round(a - b + 0.9, 2)): confusiones_mod[1]["feedback"],
                _fmt_money(round(a - b - 0.1, 2)): confusiones_mod[2]["feedback"]
            }

        else:  # N3
            op_enum = OperacionEnum.MIXTA
            a = round(20.0 + item_offset + rng.uniform(0.1, 0.5), 2)
            b = round(2.15 + (fam_idx * 0.02) + rng.uniform(0.01, 0.04), 2)
            c = round(1.10 + (fam_idx * 0.01) + rng.uniform(0.01, 0.03), 2)
            ans_num = round(a - b - c, 2)
            ans_str = _fmt_money(ans_num)

            tbl = tabla_datos([("Dinero inicial", f"R$ {_fmt_money(a)}"), ("Primer gasto", f"R$ {_fmt_money(b)}"), ("Segundo gasto", f"R$ {_fmt_money(c)}")], color=color_modulo(5,1))
            enunciado = (
                f"{personaje} administra su presupuesto en {esc['nombre'].lower()}:<br/>"
                f"{tbl}<br/>"
                f"¿Cuánto dinero le queda después de ambos gastos?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Sumamos los gastos: {_fmt_money(b)} + {_fmt_money(c)} = R$ {_fmt_money(b+c)}."},
                    {"orden": 2, "texto": f"Restamos del inicial: {_fmt_money(a)} − {_fmt_money(b+c)} = R$ {ans_str}."}
                ]
            }
            err_dict = {
                _fmt_money(round(a - b, 2)): "Olvidaste restar el segundo gasto.",
                _fmt_money(round(a + b + c, 2)): confusiones_mod[7]["feedback"]
            }

    elif modulo_id == 2:
        if nivel_id == 1:
            op_enum = OperacionEnum.MULTIPLICACION
            p_unit = round(0.35 + item_offset * 0.1 + rng.uniform(0.01, 0.04), 2)
            cant = 3 + (fam_idx + var_idx) % 7
            ans_num = round(p_unit * cant, 2)
            ans_str = _fmt_money(ans_num)

            enunciado = (
                f"En {esc['nombre'].lower()}, {personaje} compra {cant} unidades a R$ {_fmt_money(p_unit)} cada una.<br/>"
                f"¿Cuánto paga en total?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Multiplicamos enteros y ubicamos la coma a 2 lugares: R$ {ans_str}."}
                ]
            }
            err_dict = {
                _fmt_money(round(ans_num * 10, 2)): confusiones_mod[0]["feedback"],
                _fmt_money(round(p_unit + cant, 2)): confusiones_mod[3]["feedback"]
            }

        elif nivel_id == 2:
            op_enum = OperacionEnum.DIVISION
            cant = [2, 4, 5, 8, 10][(fam_idx + var_idx) % 5]
            ans_num = round(2.50 + item_offset + rng.uniform(0.01, 0.05), 2)
            total = round(ans_num * cant, 2)
            ans_str = _fmt_money(ans_num)

            enunciado = (
                f"Una cuenta de R$ {_fmt_money(total)} en {esc['nombre'].lower()} se reparte equitativamente entre {cant} personas.<br/>"
                f"¿Cuánto paga cada una?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Dividimos total ÷ personas: {_fmt_money(total)} ÷ {cant} = {ans_str}."}
                ]
            }
            err_dict = {
                _fmt_money(round(total * cant, 2)): confusiones_mod[2]["feedback"],
                _fmt_money(round(total / 10, 2)): confusiones_mod[1]["feedback"]
            }

        else:
            op_enum = OperacionEnum.MIXTA
            cant = [3, 4, 6, 12][(fam_idx + var_idx) % 4]
            unit_price = round(2.20 + item_offset + rng.uniform(0.01, 0.05), 2)
            total = round(unit_price * cant, 2)
            ans_num = unit_price
            ans_str = _fmt_money(ans_num)

            tbl = tabla_datos([("Costo total del paquete", f"R$ {_fmt_money(total)}"), ("Cantidad de unidades", f"{cant}")], color=color_modulo(5,2))
            enunciado = (
                f"{personaje} consulta precios en {esc['nombre'].lower()}:<br/>"
                f"{tbl}<br/>"
                f"¿Cuál es el precio unitario de cada producto?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Dividimos total ÷ unidades: {_fmt_money(total)} ÷ {cant} = {ans_str}."}
                ]
            }
            err_dict = {
                _fmt_money(total): confusiones_mod[9]["feedback"],
                _fmt_money(round(total * cant, 2)): confusiones_mod[2]["feedback"]
            }

    elif modulo_id == 3:
        if nivel_id == 1:
            op_enum = OperacionEnum.MIXTA
            m_val = round(1.10 + item_offset + rng.uniform(0.01, 0.05), 2)
            ans_num = round(m_val * 100, 1)
            ans_str = _fmt_dec(ans_num)

            svg = escalera_unidades("lineal", ["cm","dm","m"], "m", "cm", m_val, color_modulo(5,3))
            enunciado = (
                f"{personaje} mide un tramo en {esc['nombre'].lower()}: {m_val} m.<br/>"
                f"{svg}<br/>"
                f"¿Cuántos centímetros son?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"De m a cm bajamos 2 peldaños (×100): {m_val} × 100 = {ans_str} cm."}
                ]
            }
            err_dict = {
                _fmt_dec(m_val * 10): confusiones_mod[3]["feedback"],
                _fmt_dec(m_val / 100): confusiones_mod[1]["feedback"]
            }

        elif nivel_id == 2:
            op_enum = OperacionEnum.MIXTA
            m_val = round(1.2 + (fam_idx * 0.05), 1)
            cm_val = 15 + var_idx * 10 + fam_idx % 20
            ans_num = round(m_val * 100 + cm_val, 1)
            ans_str = _fmt_dec(ans_num)

            enunciado = (
                f"{personaje} une dos cables en {esc['nombre'].lower()}: uno de {m_val} m y otro de {cm_val} cm.<br/>"
                f"¿Cuántos centímetros de cable tiene en total?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Convertimos {m_val} m a cm ({int(m_val*100)}) y sumamos {cm_val} = {ans_str} cm."}
                ]
            }
            err_dict = {
                _fmt_dec(m_val + cm_val): confusiones_mod[4]["feedback"],
                _fmt_dec(m_val * 100): "Olvidaste sumar el segundo tramo."
            }

        else:
            op_enum = OperacionEnum.MIXTA
            cm_mapa = 2 + (fam_idx + var_idx) % 7
            esc_val = [2, 5, 10, 15][fam_idx % 4]
            ans_num = cm_mapa * esc_val
            ans_str = _fmt_dec(ans_num)

            tbl = tabla_datos([("Medida en mapa", f"{cm_mapa} cm"), ("Escala", f"1 cm = {esc_val} km")], color=color_modulo(5,3))
            enunciado = (
                f"{personaje} estudia un plano en {esc['nombre'].lower()}:<br/>"
                f"{tbl}<br/>"
                f"¿Cuál es la distancia real en kilómetros?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Multiplicamos cm × escala: {cm_mapa} × {esc_val} = {ans_num} km."}
                ]
            }
            err_dict = {
                _fmt_dec(cm_mapa / esc_val): confusiones_mod[6]["feedback"],
                _fmt_dec(cm_mapa + esc_val): "Multiplica la distancia por el factor de escala."
            }

    elif modulo_id == 4:
        if nivel_id == 1:
            op_enum = OperacionEnum.MIXTA
            l_val = round(0.4 + item_offset * 0.1 + rng.uniform(0.01, 0.04), 1)
            ans_num = round(l_val * 1000, 1)
            ans_str = _fmt_dec(ans_num)

            svg = escalera_unidades("cubica", ["mL","L"], "L", "mL", l_val, color_modulo(5,4))
            enunciado = (
                f"{personaje} revisa un envase en {esc['nombre'].lower()} de {l_val} L.<br/>"
                f"{svg}<br/>"
                f"¿Cuántos mililitros contiene?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"1 L = 1000 mL → {l_val} × 1000 = {ans_str} mL."}
                ]
            }
            err_dict = {
                _fmt_dec(l_val * 100): confusiones_mod[0]["feedback"],
                _fmt_dec(l_val / 1000): confusiones_mod[5]["feedback"]
            }

        elif nivel_id == 2:
            op_enum = OperacionEnum.MIXTA
            dm3_val = 4 + fam_idx + var_idx * 2
            ans_num = dm3_val
            ans_str = _fmt_dec(ans_num)

            enunciado = (
                f"Un depósito en {esc['nombre'].lower()} ocupa {dm3_val} dm³ de volumen.<br/>"
                f"¿Cuántos litros de capacidad tiene?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"1 dm³ = 1 L → {dm3_val} dm³ = {ans_str} L."}
                ]
            }
            err_dict = {
                _fmt_dec(dm3_val * 10): confusiones_mod[2]["feedback"],
                _fmt_dec(dm3_val * 1000): "dm³ y L son equivalentes 1:1."
            }

        else:
            op_enum = OperacionEnum.MIXTA
            cap_l = round(1.0 + item_offset * 0.1, 1)
            usado_ml = 100 + var_idx * 50 + fam_idx * 5
            ans_num = round(cap_l * 1000 - usado_ml, 1)
            ans_str = _fmt_dec(ans_num)

            tbl = tabla_datos([("Capacidad total", f"{cap_l} L"), ("Consumo", f"{usado_ml} mL")], color=color_modulo(5,4))
            enunciado = (
                f"{personaje} controla líquidos en {esc['nombre'].lower()}:<br/>"
                f"{tbl}<br/>"
                f"¿Cuántos mililitros de líquido quedan?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"{cap_l} L = {int(cap_l*1000)} mL − {usado_ml} mL = {ans_str} mL."}
                ]
            }
            err_dict = {
                _fmt_dec(cap_l * 1000 + usado_ml): confusiones_mod[6]["feedback"],
                _fmt_dec(cap_l * 1000): "Olvidaste restar el consumo."
            }

    else:
        if nivel_id == 1:
            op_enum = OperacionEnum.MIXTA
            m2_val = round(1.5 + item_offset * 0.1 + rng.uniform(0.01, 0.05), 1)
            ans_num = round(m2_val * 100, 1)
            ans_str = _fmt_dec(ans_num)

            svg = escalera_unidades("cuadrada", ["cm²","dm²","m²"], "m²", "dm²", m2_val, color_modulo(5,5))
            enunciado = (
                f"{personaje} mide una lámina en {esc['nombre'].lower()} de {m2_val} m².<br/>"
                f"{svg}<br/>"
                f"¿Cuántos decímetros cuadrados (dm²) son?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"De m² a dm² multiplicamos por 100: {m2_val} × 100 = {ans_str} dm²."}
                ]
            }
            err_dict = {
                _fmt_dec(m2_val * 10): confusiones_mod[0]["feedback"],
                _fmt_dec(m2_val / 100): confusiones_mod[8]["feedback"]
            }

        elif nivel_id == 2:
            op_enum = OperacionEnum.MIXTA
            pulg_val = 4 + fam_idx % 25 + var_idx * 2
            ans_num = round(pulg_val * 2.54, 2)
            ans_str = _fmt_dec(ans_num)

            enunciado = (
                f"{personaje} mide una pantalla en {esc['nombre'].lower()}: {pulg_val} pulgadas.<br/>"
                f"¿Cuántos centímetros mide la diagonal? (1 pulg = 2,54 cm)"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"{pulg_val} × 2,54 = {ans_str} cm."}
                ]
            }
            err_dict = {
                _fmt_dec(pulg_val * 2.5): confusiones_mod[5]["feedback"],
                _fmt_dec(pulg_val * 2.0): "Usa el factor exacto de 2,54 cm por pulgada."
            }

        else:
            op_enum = OperacionEnum.MIXTA
            ha_val = round(1.2 + item_offset * 0.1, 1)
            lotes = [4, 5, 8, 10, 20][(fam_idx + var_idx) % 5]
            ans_num = round(ha_val * 10000 / lotes, 1)
            ans_str = _fmt_dec(ans_num)

            tbl = tabla_datos([("Superficie del terreno", f"{ha_val} ha"), ("Lotes iguales", f"{lotes}")], color=color_modulo(5,5))
            enunciado = (
                f"{personaje} evalúa una parcela en {esc['nombre'].lower()}:<br/>"
                f"{tbl}<br/>"
                f"¿Cuántos metros cuadrados (m²) le corresponden a cada lote?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"{ha_val} ha = {int(ha_val*10000)} m² ÷ {lotes} = {ans_str} m²."}
                ]
            }
            err_dict = {
                _fmt_dec(ha_val * 10000 * lotes): confusiones_mod[4]["feedback"],
                _fmt_dec(ha_val * 1000 / lotes): confusiones_mod[3]["feedback"]
            }

    tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA if _is_numeric_answer(ans_str) else TipoPreguntaEnum.MULTIPLE_OPCION

    datos_num = {
        "fase5": True,
        "seed": seed_val,
        "escenario": esc["nombre"],
        "personaje": personaje,
        "variante": var_idx,
        "es_espejo": es_espejo,
        "resultado": ans_str
    }

    return {
        "fase_id": FASE5_ID,
        "seccion": sec,
        "estructura_padre_id": fam_id,
        "operacion": op_enum,
        "tipo_pregunta": tipo_preg,
        "enunciado": enunciado,
        "respuesta_correcta": ans_str,
        "datos_numericos": datos_num,
        "explicacion_paso_a_paso": explicacion,
        "errores_previstos": err_dict,
        "requiere_subrayado": False,
        "estado": StatusEnum.ACTIVO,
        "creado_por": None
    }


async def seed_practica_pool(session: AsyncSession):
    print("Sembrando 7.200 preguntas de práctica (15 niveles × 120 familias × 4)...")
    total_q = 0
    batch_questions = []

    for mod_id in range(1, 6):
        for lvl_id in range(1, 4):
            sec = mod_id * 100 + lvl_id
            for fam_idx in range(120):
                for var_idx in range(4):
                    seed_val = 50000000 + sec * 100000 + fam_idx * 10 + var_idx
                    q_dict = _generate_practice_question(mod_id, lvl_id, fam_idx, var_idx, seed_val)
                    
                    p = Pregunta(**q_dict)
                    batch_questions.append(p)
                    total_q += 1

                    if len(batch_questions) >= 600:
                        session.add_all(batch_questions)
                        await session.commit()
                        batch_questions = []
    
    if batch_questions:
        session.add_all(batch_questions)
        await session.commit()

    print(f"Práctica sembrada: {total_q} preguntas.")

# ── 4. GENERADOR DE DESAFÍOS (2.400 preguntas = 16 bloques x 150) ──────────────

def _generate_challenge_question(sec: int, q_idx: int, seed_val: int) -> dict:
    rng = random.Random(seed_val)
    mod_id = 99 if sec == 99099 else sec // 1000
    des_id = 99 if sec == 99099 else sec % 100
    personaje = NOMBRES_POOL[(q_idx) % len(NOMBRES_POOL)]

    real_mod = rng.randint(1, 5) if mod_id == 99 else mod_id
    escenarios_mod = [e for e in CATALOGO_DATA["escenarios"] if e["modulo_id"] == real_mod]
    confusiones_mod = [c for c in CATALOGO_DATA["confusiones"] if c["modulo_id"] == real_mod]
    esc = escenarios_mod[q_idx % len(escenarios_mod)]

    struct_id = f"f5_d{sec}_q{q_idx:03d}"

    q_offset = q_idx * 0.12

    if des_id == 11 or (des_id == 99 and q_idx % 3 == 0):
        op_enum = OperacionEnum.MIXTA
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        a = round(2.50 + q_offset + rng.uniform(0.01, 0.05), 2)
        b = round(1.10 + q_idx * 0.05 + rng.uniform(0.01, 0.03), 2)
        ans_num = round(a + b, 2)
        ans_str = _fmt_money(ans_num)

        tbl = tabla_datos([("Monto 1", f"R$ {_fmt_money(a)}"), ("Monto 2", f"R$ {_fmt_money(b)}")], color=color_modulo(5, real_mod))
        enunciado = f"{personaje} reúne montos en {esc['nombre'].lower()}.<br/>{tbl}<br/>¿Qué operación calcula el total acumulado?"
        
        correct_alt = f"Sumar R$ {_fmt_money(a)} + R$ {_fmt_money(b)}"
        alts = [
            {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
            {"texto": f"Restar R$ {_fmt_money(a)} − R$ {_fmt_money(b)}", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": confusiones_mod[7]["feedback"]},
            {"texto": f"Multiplicar R$ {_fmt_money(a)} × R$ {_fmt_money(b)}", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "No corresponde multiplicar montos al juntar dinero."},
            {"texto": f"Sumar R$ {_fmt_money(a)} + R$ {_fmt_money(b)} sin alinear la coma", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.VALOR_POSICIONAL, "feedback_error": confusiones_mod[0]["feedback"]}
        ]
        rng.shuffle(alts)
        for i, alt in enumerate(alts):
            alt["orden"] = i + 1

        explicacion = {
            "titulo": "Resolución",
            "pasos": [{"orden": 1, "texto": f"Juntar dos cantidades es sumar: {_fmt_money(a)} + {_fmt_money(b)} = R$ {ans_str}."}],
            "pista": {"texto": "Compara si los montos se unen o se descuentan para elegir el procedimiento adecuado.", "penalizacion_segundos": 5}
        }
        err_dict = {alt["texto"]: alt["feedback_error"] for alt in alts if not alt["es_correcta"]}

    elif des_id == 12 or (des_id == 99 and q_idx % 3 == 1):
        op_enum = OperacionEnum.MIXTA
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        a = round(12.0 + q_offset + rng.uniform(0.1, 0.4), 1)
        b = round(1.50 + q_idx * 0.04 + rng.uniform(0.01, 0.05), 2)
        ans_num = round(a - b, 2)
        ans_str = _fmt_money(ans_num)
        err_val = _fmt_money(round(a - b + 0.9, 2))

        tbl = tabla_datos([("Dinero", f"R$ {_fmt_money(a)}"), ("Gasto", f"R$ {_fmt_money(b)}"), ("Cálculo de Hugo", f"R$ {err_val}")], color=color_modulo(5, real_mod))
        enunciado = f"Hugo calculó su saldo en {esc['nombre'].lower()}.<br/>{tbl}<br/>¿Cuál fue su error?"

        correct_alt = "No completó con cero la cifra decimal antes de restar"
        alts = [
            {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
            {"texto": "Sumó en lugar de restar", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Hugo sí restó, pero no igualó decimales."},
            {"texto": "Multiplicó los números", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "No hubo multiplicación."},
            {"texto": "Los datos no alcanzan para decidir", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.NO_IDENTIFICA_DATOS, "feedback_error": "Los datos son suficientes."}
        ]
        rng.shuffle(alts)
        for i, alt in enumerate(alts):
            alt["orden"] = i + 1

        explicacion = {
            "titulo": "Resolución",
            "pasos": [{"orden": 1, "texto": f"Completar cero: {_fmt_money(a)} − {_fmt_money(b)} = R$ {ans_str}."}],
            "pista": {"texto": "Compara la cantidad de dígitos decimales que usó Hugo con los del enunciado.", "penalizacion_segundos": 5}
        }
        err_dict = {alt["texto"]: alt["feedback_error"] for alt in alts if not alt["es_correcta"]}

    else:
        op_enum = OperacionEnum.MIXTA
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        a = round(10.0 + q_offset + rng.uniform(0.01, 0.05), 2)
        b = round(2.0 + q_idx * 0.03 + rng.uniform(0.01, 0.04), 2)
        c_irrel = round(5.0 + q_idx * 0.05 + rng.uniform(0.01, 0.05), 2)
        ans_num = round(a + b, 2)
        ans_str = _fmt_money(ans_num)

        tbl = tabla_datos([("Producto A", f"R$ {_fmt_money(a)}"), ("Producto B", f"R$ {_fmt_money(b)}"), ("Promoción no comprada", f"R$ {_fmt_money(c_irrel)}")], color=color_modulo(5, real_mod))
        enunciado = f"{personaje} compra en {esc['nombre'].lower()}.<br/>{tbl}<br/>¿Cuánto paga por el Producto A y el Producto B en total?"

        alts = None
        explicacion = {
            "titulo": "Resolución",
            "pasos": [
                {"orden": 1, "texto": f"La promoción no comprada es un dato irrelevante."},
                {"orden": 2, "texto": f"Sumamos A + B: {_fmt_money(a)} + {_fmt_money(b)} = R$ {ans_str}."}
            ],
            "pista": {"texto": "Revisa qué productos se compraron realmente y descarta lo que no se llevó.", "penalizacion_segundos": 5}
        }
        err_dict = {
            _fmt_money(round(a + b + c_irrel, 2)): confusiones_mod[8]["feedback"],
            _fmt_money(round(a - b, 2)): "Para hallar el total comprado se suma, no se resta."
        }

    datos_num = {
        "fase5": True,
        "es_desafio": True,
        "seccion": sec,
        "seed": seed_val,
        "escenario": esc["nombre"],
        "personaje": personaje,
        "resultado": ans_str
    }

    return {
        "q_dict": {
            "fase_id": FASE5_ID,
            "seccion": sec,
            "estructura_padre_id": struct_id,
            "operacion": op_enum,
            "tipo_pregunta": tipo_preg,
            "enunciado": enunciado,
            "respuesta_correcta": ans_str,
            "datos_numericos": datos_num,
            "explicacion_paso_a_paso": explicacion,
            "errores_previstos": err_dict,
            "requiere_subrayado": False,
            "estado": StatusEnum.ACTIVO,
            "creado_por": None
        },
        "alts": alts
    }


async def seed_preguntas_desafios(session: AsyncSession):
    print("Sembrando 2.400 preguntas de desafíos (16 bloques × 150)...")
    desafios_sec = [
        1011, 1012, 1013, 2011, 2012, 2013, 3011, 3012, 3013,
        4011, 4012, 4013, 5011, 5012, 5013, 99099
    ]
    total_q = 0

    for sec in desafios_sec:
        batch_alts = []
        for q_idx in range(150):
            seed_val = 59000000 + sec * 1000 + q_idx
            res_item = _generate_challenge_question(sec, q_idx, seed_val)
            p = Pregunta(**res_item["q_dict"])
            session.add(p)
            await session.flush()

            if res_item["alts"]:
                for alt_dict in res_item["alts"]:
                    alt = Alternativa(
                        pregunta_id=p.id,
                        texto=alt_dict["texto"],
                        es_correcta=alt_dict["es_correcta"],
                        orden=alt_dict["orden"],
                        tipo_error=alt_dict["tipo_error"],
                        feedback_error=alt_dict["feedback_error"]
                    )
                    batch_alts.append(alt)
            total_q += 1

        if batch_alts:
            session.add_all(batch_alts)
        await session.commit()

    print(f"Desafíos sembrados: {total_q} preguntas.")

# ── 5. SIEMBRA DE CONFIGURACIÓN DE PROGRESO (32 filas) ───────────────────────

async def seed_configuracion_progreso(session: AsyncSession):
    print("Sembrando 32 filas en configuracion_progreso...")

    cfg_0 = ConfiguracionProgreso(
        fase_id=FASE5_ID,
        seccion=0,
        operacion=OperacionEnum.MIXTA,
        cantidad_requerida=15,
        porcentaje_aprobacion=90,
        orden_desbloqueo=99,
        tipo_feedback="normal",
        usa_cronometro=True,
        tiempo_default_segundos=60,
        errores_tolerados=3,
        pistas_permitidas=3,
        penalizacion_pista_segundos=5,
        activo=True
    )
    session.add(cfg_0)

    for mod_id in range(1, 6):
        for lvl_id in range(1, 4):
            sec = mod_id * 100 + lvl_id
            cfg_p = ConfiguracionProgreso(
                fase_id=FASE5_ID,
                seccion=sec,
                operacion=OperacionEnum.MIXTA,
                cantidad_requerida=15,
                porcentaje_aprobacion=100,
                orden_desbloqueo=lvl_id,
                tipo_feedback="bucle_espejo",
                usa_cronometro=False,
                tiempo_default_segundos=0,
                errores_tolerados=None,
                pistas_permitidas=0,
                penalizacion_pista_segundos=0,
                activo=True
            )
            session.add(cfg_p)

    desafios_master = [
        (11, 12, 60, 2),
        (12, 12, 90, 2),
        (13, 10, 120, 1),
    ]
    for mod_id in range(1, 6):
        for des_id, cant, seg, err in desafios_master:
            sec = mod_id * 1000 + des_id
            cfg_d = ConfiguracionProgreso(
                fase_id=FASE5_ID,
                seccion=sec,
                operacion=OperacionEnum.MIXTA,
                cantidad_requerida=cant,
                porcentaje_aprobacion=100,
                orden_desbloqueo=10 + (des_id % 10),
                tipo_feedback="normal",
                usa_cronometro=True,
                tiempo_default_segundos=seg,
                errores_tolerados=err,
                pistas_permitidas=3,
                penalizacion_pista_segundos=5,
                activo=True
            )
            session.add(cfg_d)

    cfg_mix = ConfiguracionProgreso(
        fase_id=FASE5_ID,
        seccion=99099,
        operacion=OperacionEnum.MIXTA,
        cantidad_requerida=15,
        porcentaje_aprobacion=100,
        orden_desbloqueo=99,
        tipo_feedback="normal",
        usa_cronometro=True,
        tiempo_default_segundos=90,
        errores_tolerados=3,
        pistas_permitidas=3,
        penalizacion_pista_segundos=5,
        activo=True
    )
    session.add(cfg_mix)
    await session.commit()
    print("32 filas de `configuracion_progreso` sembradas.")

# ── 6. RUNNER PRINCIPAL DE SIEMBRA FASE 5 ────────────────────────────────────

async def run_fase5_seed():
    print("=" * 60)
    print("INICIANDO SIEMBRA COMPLETA DE FASE 5 (Modelo B / TJS)")
    print("=" * 60)
    async with AsyncSessionLocal() as session:
        await upsert_fila_fases(session)
        await clear_fase5_data(session)
        await seed_teoria_niveles(session)
        await seed_practica_pool(session)
        await seed_preguntas_desafios(session)
        await seed_configuracion_progreso(session)
    print("=" * 60)
    print("SIEMBRA DE FASE 5 FINALIZADA CON ÉXITO")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_fase5_seed())
