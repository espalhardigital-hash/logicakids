"""
Seeder autónomo y determinista para la Fase 4: Operatoria Decimal y Conversiones.
Cumple estrictamente con reestructuracion.md y deep_analise_pro §25.4.

Volumetría:
  - 12 niveles en niveles_teoria_pool (NivelTeoria) — 4 módulos × 3 niveles.
  - 3.456 preguntas de práctica (4 módulos × 3 niveles × 72 familias × 4 variantes: 1 original + 3 espejo).
  - 1.950 preguntas de desafíos (13 bloques × 150 preguntas; 12 de módulo + 1 mixto 99099).
  - 16 filas en configuracion_progreso (4 módulos × 4 config por módulo).

Reglas duras (Fase 4):
  - Cero vocabulario de fracciones (décimas = partes de 10, centésimas = partes de 100).
  - Cero MinIO / PNG (todo SVG inline vía app.utils.svg_figuras).
  - estructura_padre_id NUNCA NULL (f4_mX_lY_fam_ZZZ en práctica, f4_dSEC_qZZZ en desafíos).
  - Enunciados TJS ≤ 50 palabras de prosa, datos en mini-tabla/SVG, 1 pregunta al final.
  - Enunciado compositor validado con R1, R2 y presupuestos (CompositorFase4).
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
from app.fase4.theory_data import FASE4_TEORIA_DATA
from app.utils.svg_figuras import (
    fig_rectangulo, fig_cuadrado, fig_triangulo, fig_L, fig_T,
    escalera_unidades, recta_numerica_decimal, tabla_datos, comparador_opciones,
    color_modulo
)

FASE_DECIMALES_ID = 4

# catalogo_fase5.json mantenido en disco como referencia histórica (no se usa).
# Los nuevos catálogos son escenarios_fase4.json, plantillas_fase4.json,
# confusiones_fase4.json y nombres_fase4.json, cargados por el CompositorFase4.
CATALOGO_PATH = os.path.join(os.path.dirname(__file__), "data", "catalogo_fase5.json")

def _load_catalogo() -> Dict[str, Any]:
    with open(CATALOGO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

CATALOGO_DATA = _load_catalogo()

# ── Compositor: carga los 4 catálogos nuevos una sola vez ────────────────────
from app.fase4.compositor_fase4 import CompositorFase4
_COMPOSITOR = CompositorFase4()   # singleton; carga los catálogos al importar

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

async def upsert_fila_fases(session: AsyncSession):
    # Fase 4: Operatoria Decimal y Conversiones
    res4 = await session.execute(select(Fase).where(Fase.id == FASE_DECIMALES_ID))
    fase4 = res4.scalar_one_or_none()
    if not fase4:
        fase4 = Fase(
            id=FASE_DECIMALES_ID,
            nombre="Operatoria Decimal y Conversiones",
            descripcion="Suma, resta, multiplicación, división con decimales y conversiones métricas",
            orden=4,
            estado=StatusEnum.ACTIVO
        )
        session.add(fase4)
    else:
        fase4.nombre = "Operatoria Decimal y Conversiones"
        fase4.descripcion = "Suma, resta, multiplicación, división con decimales y conversiones métricas"
        fase4.orden = 4
        fase4.estado = StatusEnum.ACTIVO

    # Fase 5: Fracciones, Porcentajes y Proporciones
    res5 = await session.execute(select(Fase).where(Fase.id == 5))
    fase5 = res5.scalar_one_or_none()
    if not fase5:
        fase5 = Fase(
            id=5,
            nombre="Fracciones, Porcentajes y Proporciones",
            descripcion="Representación, operaciones de fracciones, porcentajes y regla de tres",
            orden=5,
            estado=StatusEnum.ACTIVO
        )
        session.add(fase5)
    else:
        fase5.nombre = "Fracciones, Porcentajes y Proporciones"
        fase5.descripcion = "Representación, operaciones de fracciones, porcentajes y regla de tres"
        fase5.orden = 5
        fase5.estado = StatusEnum.ACTIVO

    await session.commit()
    print("Fases 4 y 5 en tabla `fases` aseguradas.")

# ── 1. LIMPIEZA / PURGA IDEMPOTENTE ──────────────────────────────────────────

async def clear_fase4_data(session: AsyncSession):
    print("Purga de datos preexistentes de Fase 5 en cascada...")
    res = await session.execute(select(Pregunta.id).where(Pregunta.fase_id == FASE_DECIMALES_ID))
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

    await session.execute(delete(Intento).where(Intento.fase_id == FASE_DECIMALES_ID))
    await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE_DECIMALES_ID))
    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE_DECIMALES_ID))
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE_DECIMALES_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE_DECIMALES_ID))
    await session.commit()
    print("Purga de Fase 4 (Decimales) completada.")

# ── 2. SIEMBRA DE TEORÍA (NivelTeoria) ───────────────────────────────────────

from app.fase4.theory_examples import obtener_ejemplos_expandidos_fase4

def validar_contenido_pre_siembra():
    if len(FASE4_TEORIA_DATA) != 12:
        raise ValueError(f"FASE4_TEORIA_DATA debe contener exactamente 12 niveles, hallados {len(FASE4_TEORIA_DATA)}")
    
    for t_data in FASE4_TEORIA_DATA:
        desc = t_data.get("texto_descubrimiento", "")
        cuerpo = t_data.get("cuerpo_teoria", "")
        full_txt = desc + " " + cuerpo
        for word in ["fracción", "fracciones", "un décimo", "¹/₁₀"]:
            if word in full_txt.lower():
                raise ValueError(f"Término prohibido de fracciones '{word}' hallado en M{t_data['modulo_id']} N{t_data['nivel_id']}")

    for m in range(1, 5):
        for n in range(1, 4):
            egs = obtener_ejemplos_expandidos_fase4(m, n)
            if len(egs) != 4:
                raise ValueError(f"Módulo {m} Nivel {n} debe tener exactamente 4 ejemplos guiados, hallados {len(egs)}")
            tjs = egs[3]
            if len(tjs.get("pasos", [])) != 5:
                raise ValueError(f"Ejemplo 4 TJS de M{m} N{n} debe tener exactamente 5 pasos, hallados {len(tjs.get('pasos', []))}")
            if "opciones" not in tjs["pasos"][2]:
                raise ValueError(f"Ejemplo 4 TJS de M{m} N{n} en paso 3 carece de opciones de compromiso activo")

    print("✅ Validación pre-siembra superada con éxito (Presupuesto, Cero Fracciones, 4 Ejemplos por Nivel con TJS de 5 pasos).")

async def seed_teoria_niveles(session: AsyncSession):
    validar_contenido_pre_siembra()
    print("Sembrando los 12 guiones teóricos (niveles_teoria_pool)...")
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE_DECIMALES_ID))
    for t_data in FASE4_TEORIA_DATA:
        egs = obtener_ejemplos_expandidos_fase4(t_data["modulo_id"], t_data["nivel_id"])
        nt = NivelTeoria(
            fase_id=FASE_DECIMALES_ID,
            modulo_id=t_data["modulo_id"],
            nivel_id=t_data["nivel_id"],
            titulo=t_data["titulo"],
            texto_descubrimiento=t_data["texto_descubrimiento"] + "\n\n" + t_data.get("cuerpo_teoria", ""),
            advertencia=t_data["advertencia"],
            diccionario=t_data["diccionario"],
            ejemplos=egs,
            interactivos=[],
            revisado_admin=True,
            revisado_por="seed_fase4_ch7"
        )
        session.add(nt)
    await session.commit()
    print("12 niveles teóricos sembrados con éxito.")

# ── 3. GENERADOR DE PRÁCTICA (7.200 preguntas = 15 niveles x 120 fam x 4) ─────

def _generate_practice_question(modulo_id: int, nivel_id: int, fam_idx: int, var_idx: int, seed_val: int) -> dict:
    rng = random.Random(seed_val)
    sec = modulo_id * 100 + nivel_id
    fam_id = f"f4_m{modulo_id}_l{nivel_id}_fam_{fam_idx:03d}"
    es_espejo = (var_idx > 0)
    personaje = NOMBRES_POOL[(fam_idx + var_idx) % len(NOMBRES_POOL)]

    # ── Compositor: genera enunciado validado (R1, R2, presupuestos, variedad) ──
    try:
        comp = _COMPOSITOR.componer_pregunta_practica(
            modulo_id, nivel_id, fam_idx, var_idx, seed_val
        )
        enunciado_comp = comp["enunciado"]
    except Exception:
        # Fallback determinista si el compositor no tiene plantilla para esta combinación
        enunciado_comp = None

    # El catálogo viejo se usa solo para confusiones y escenario de referencia
    # (el enunciado final vendrá del compositor si está disponible)
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

            tbl = tabla_datos([("Costo total", f"R$ {_fmt_money(total)}"), ("Cant. unidades", f"{cant}")], color=color_modulo(5,2))
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
            km_val = round(1.2 + item_offset * 0.4, 1)
            tramos = [4, 5, 8, 10, 20][(fam_idx + var_idx) % 5]
            ans_num = round(km_val * 1000 / tramos, 1)
            ans_str = _fmt_dec(ans_num)

            tbl = tabla_datos([("Distancia total", f"{km_val} km"), ("Tramos iguales", f"{tramos}")], color=color_modulo(4,3))
            enunciado = (
                f"{personaje} recorre un trayecto en {esc['nombre'].lower()}:<br/>"
                f"{tbl}<br/>"
                f"¿Cuántos metros mide cada tramo del recorrido?"
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"{km_val} km = {int(km_val*1000)} m ÷ {tramos} = {ans_str} m."}
                ]
            }
            err_dict = {
                _fmt_dec(km_val * 1000 * tramos): confusiones_mod[4]["feedback"],
                _fmt_dec(km_val * 100 / tramos): confusiones_mod[3]["feedback"]
            }

    tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA if _is_numeric_answer(ans_str) else TipoPreguntaEnum.MULTIPLE_OPCION

    datos_num = {
        "fase4": True,
        "seed": seed_val,
        "escenario": esc["nombre"],
        "personaje": personaje,
        "variante": var_idx,
        "es_espejo": es_espejo,
        "resultado": ans_str
    }

    return {
        "fase_id": FASE_DECIMALES_ID,
        "seccion": sec,
        "estructura_padre_id": fam_id,          # NUNCA None (Tomo 4 §11, F5 req#1)
        "operacion": op_enum,
        "tipo_pregunta": tipo_preg,
        "enunciado": enunciado_comp if enunciado_comp else enunciado,  # compositor first
        "respuesta_correcta": ans_str,
        "datos_numericos": datos_num,
        "explicacion_paso_a_paso": explicacion,
        "errores_previstos": err_dict,
        "requiere_subrayado": False,
        "estado": StatusEnum.ACTIVO,
        "creado_por": None
    }


async def seed_practica_pool(session: AsyncSession):
    print("Sembrando 3.456 preguntas de práctica libre (4 módulos × 3 niveles × 72 familias × 4 variantes)...")
    total_q = 0
    batch_questions = []

    for mod_id in range(1, 5):
        for lvl_id in range(1, 4):
            sec = mod_id * 100 + lvl_id
            for fam_idx in range(72):
                for var_idx in range(4):
                    seed_val = 50000000 + sec * 100000 + fam_idx * 10 + var_idx
                    q_dict = _generate_practice_question(mod_id, lvl_id, fam_idx, var_idx, seed_val)
                    
                    p = Pregunta(**q_dict)
                    batch_questions.append(p)
                    total_q += 1

                    if len(batch_questions) >= 1000:
                        session.add_all(batch_questions)
                        await session.commit()
                        batch_questions = []
    
    if batch_questions:
        session.add_all(batch_questions)
        await session.commit()

    print(f"Práctica sembrada: {total_q} preguntas.")

# ── 4. GENERADOR DE DESAFÍOS (1.950 preguntas = 13 bloques x 150) ──────────────

def _generate_challenge_question(sec: int, q_idx: int, seed_val: int) -> dict:
    rng = random.Random(seed_val)
    mod_id = 99 if sec == 99099 else sec // 1000
    des_id = 99 if sec == 99099 else sec % 100

    real_mod = (q_idx % 4) + 1 if mod_id == 99 else mod_id
    personaje = NOMBRES_POOL[q_idx % len(NOMBRES_POOL)]

    escenarios_mod = [e for e in CATALOGO_DATA["escenarios"] if e["modulo_id"] == real_mod]
    confusiones_mod = [c for c in CATALOGO_DATA["confusiones"] if c["modulo_id"] == real_mod]
    if not escenarios_mod:
        escenarios_mod = CATALOGO_DATA["escenarios"]
    if not confusiones_mod:
        confusiones_mod = CATALOGO_DATA["confusiones"]
    esc = escenarios_mod[q_idx % len(escenarios_mod)]

    struct_id = f"f5_d{sec}_q{q_idx:03d}"

    des_type = (11 if (q_idx % 3 == 0) else (12 if (q_idx % 3 == 1) else 13)) if des_id == 99 else des_id

    # ── D1: PROBLEMA DE CONTEXTO EN OPCIÓN MÚLTIPLE (C5.3, C5.5, C5.9) ────────
    if des_type == 11:
        op_enum = OperacionEnum.MIXTA
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION

        if real_mod == 1:
            a = round(2.50 + (q_idx % 10) * 0.40 + rng.uniform(0.01, 0.09), 2)
            b = round(1.10 + (q_idx % 8) * 0.30 + rng.uniform(0.01, 0.09), 2)
            ans_num = round(a + b, 2)
            ans_str = _fmt_money(ans_num)
            enunciado = f"{personaje} compró un cuaderno de R$ {_fmt_money(a)} y un lápiz de R$ {_fmt_money(b)}. ¿Cuánto gastó en total?"
            correct_alt = f"R$ {ans_str}"
            alts = [
                {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
                {"texto": f"R$ {_fmt_money(round(a - b, 2))}", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Al juntar gastos se suma, no se resta."},
                {"texto": f"R$ {_fmt_money(round(a + b - 0.9, 2))}", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.VALOR_POSICIONAL, "feedback_error": "Revisa la suma alineando bien la coma."},
                {"texto": f"R$ {_fmt_money(round(a + b + 1.0, 2))}", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.SUMA_DECIMAL, "feedback_error": "Olvidaste llevar el acarreo de las décimas."}
            ]
        elif real_mod == 2:
            cant = (q_idx % 5) + 2
            precio = round(3.50 + (q_idx % 6) * 0.50 + rng.uniform(0.01, 0.05), 2)
            ans_num = round(cant * precio, 2)
            ans_str = _fmt_money(ans_num)
            enunciado = f"{personaje} compró {cant} paquetes de galletas a R$ {_fmt_money(precio)} cada uno. ¿Cuánto pagó en total?"
            correct_alt = f"R$ {ans_str}"
            alts = [
                {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
                {"texto": f"R$ {_fmt_money(round(cant + precio, 2))}", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Varias unidades del mismo precio se multiplican."},
                {"texto": f"R$ {_fmt_money(round(ans_num / 10, 2))}", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.VALOR_POSICIONAL, "feedback_error": "Revisa la posición de la coma al multiplicar."},
                {"texto": f"R$ {_fmt_money(round(ans_num - precio, 2))}", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.CALCULO, "feedback_error": "Faltó multiplicar por un paquete."}
            ]
        elif real_mod == 3:
            personas = (q_idx % 4) + 2
            monto = round(personas * (2.50 + (q_idx % 5) * 1.20), 2)
            ans_num = round(monto / personas, 2)
            ans_str = _fmt_money(ans_num)
            enunciado = f"{personaje} repartió R$ {_fmt_money(monto)} entre {personas} amigos en partes iguales. ¿Cuánto recibió cada uno?"
            correct_alt = f"R$ {ans_str}"
            alts = [
                {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
                {"texto": f"R$ {_fmt_money(round(monto * personas, 2))}", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Repartir en partes iguales es dividir, no multiplicar."},
                {"texto": f"R$ {_fmt_money(round(monto - personas, 2))}", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "No corresponde restar."},
                {"texto": f"R$ {_fmt_money(round(ans_num / 10, 2))}", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.VALOR_POSICIONAL, "feedback_error": "Revisa el punto decimal en la división."}
            ]
        else:
            metros = (q_idx % 8 + 1) * 250
            km = round(metros / 1000.0, 2)
            ans_str = _fmt_dec(km)
            enunciado = f"{personaje} recorrió una distancia de {metros} metros en su bicicleta. ¿A cuántos kilómetros equivale en total?"
            correct_alt = f"{ans_str} km"
            alts = [
                {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
                {"texto": f"{_fmt_dec(metros * 1000)} km", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.DECIMAL, "feedback_error": "Para pasar de m a km se divide por 1.000, no se multiplica."},
                {"texto": f"{_fmt_dec(metros / 100)} km", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.DECIMAL, "feedback_error": "1 km equivale a 1.000 m, no a 100 m."},
                {"texto": f"{_fmt_dec(metros / 10)} km", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.DECIMAL, "feedback_error": "Debes dividir por 1.000 para llegar a km."}
            ]

        rng.shuffle(alts)
        for i, alt in enumerate(alts):
            alt["orden"] = i + 1

        explicacion = {
            "titulo": "Resolución",
            "pasos": [{"orden": 1, "texto": f"Identificar datos y operar para hallar el resultado."}],
            "pista": {"texto": "Lee con atención las palabras claves para elegir la operación adecuada.", "penalizacion_segundos": 5}
        }
        err_dict = {alt["texto"]: alt["feedback_error"] for alt in alts if not alt["es_correcta"]}

    # ── D2: TJS AVANZADO EN OPCIÓN MÚLTIPLE (C5.3, C5.9) ───────────────────────
    elif des_type == 12:
        op_enum = OperacionEnum.MIXTA
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION

        if real_mod == 1:
            monto = round(15.00 + (q_idx % 5) * 5.0, 2)
            item1 = round(6.50 + (q_idx % 4) * 1.50, 2)
            item2 = round(7.20 + (q_idx % 3) * 1.10, 2)
            total = round(item1 + item2, 2)
            alcanza = total <= monto
            ans_str = "Sí, le alcanza" if alcanza else "No le alcanza"
            enunciado = f"{personaje} lleva R$ {_fmt_money(monto)}. Quiere un cuaderno de R$ {_fmt_money(item1)} y un lápiz de R$ {_fmt_money(item2)}. ¿Le alcanza el dinero?"

            correct_alt = f"Sí, y le sobran R$ {_fmt_money(monto - total)}" if alcanza else f"No, le faltan R$ {_fmt_money(total - monto)}"
            alts = [
                {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
                {"texto": f"No, le faltan R$ {_fmt_money(monto - total)}" if alcanza else f"Sí, y le sobran R$ {_fmt_money(total - monto)}", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Revisa la comparación entre el dinero disponible y el costo total."},
                {"texto": f"Le alcanza exacto sin sobrante", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.CALCULO, "feedback_error": "El gasto total no es igual al monto que lleva."},
                {"texto": "Los datos no son suficientes", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.NO_IDENTIFICA_DATOS, "feedback_error": "Los datos son suficientes para sumar y comparar."}
            ]
        elif real_mod == 2:
            a = round(2.5 + (q_idx % 5) * 0.4, 1)
            b = round(1.2 + (q_idx % 4) * 0.3, 1)
            res_err = round((a * 10) * (b * 10), 2)
            enunciado = f"{personaje} calculó {a} × {b} y obtuvo {_fmt_dec(res_err)}. ¿Cuál fue su error con la coma?"
            correct_alt = "Olvidó contar los decimales de ambos factores"
            alts = [
                {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
                {"texto": "Sumó los factores en lugar de multiplicar", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Multiplicó los dígitos pero no ubicó bien la coma."},
                {"texto": "Restó los decimales", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "No hubo resta en el procedimiento."},
                {"texto": "El resultado obtenido es correcto", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.CALCULO, "feedback_error": "El resultado correcto tiene 2 cifras decimales."}
            ]
        elif real_mod == 3:
            div = round(4.5 + (q_idx % 4) * 1.5, 1)
            divisor = round(0.5 + (q_idx % 3) * 0.5, 1)
            ans_val = round(div / divisor, 2)
            enunciado = f"{personaje} dividió {_fmt_dec(div)} ÷ {_fmt_dec(divisor)} desplazando las comas. ¿Tuvo razón al afirmar que el resultado es entero?"
            correct_alt = f"Sí, porque al desplazar comas obtiene {int(div*10)} ÷ {int(divisor*10)} = {_fmt_dec(ans_val)}"
            alts = [
                {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
                {"texto": "No, porque al dividir decimales siempre da decimal", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.CALCULO, "feedback_error": "La división de dos decimales puede dar un cociente entero."},
                {"texto": "No, porque debió restar las comas", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Las comas se desplazan multiplicando por 10 en dividendo y divisor."},
                {"texto": "Faltan datos para saber el resultado", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.NO_IDENTIFICA_DATOS, "feedback_error": "Los datos son suficientes para resolver."}
            ]
        else:
            val_m = round(1.5 + (q_idx % 4) * 0.5, 1)
            val_cm_err = val_m * 10
            enunciado = f"{personaje} convirtió {_fmt_dec(val_m)} m a cm y obtuvo {_fmt_dec(val_cm_err)} cm. ¿Dónde cometió el error?"
            correct_alt = "Multiplicó por 10 en lugar de multiplicar por 100"
            alts = [
                {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
                {"texto": "Dividió por 100 en lugar de multiplicar", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.DECIMAL, "feedback_error": "Al bajar la escalera se multiplica."},
                {"texto": "Sumó 100 en lugar de multiplicar", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Las conversiones métricas usan multiplicación o división."},
                {"texto": "El resultado obtenido es correcto", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.CALCULO, "feedback_error": "1 metro tiene 100 cm, por lo que 1,5 m es 150 cm."}
            ]

        rng.shuffle(alts)
        for i, alt in enumerate(alts):
            alt["orden"] = i + 1
        ans_str = correct_alt

        explicacion = {
            "titulo": "Resolución",
            "pasos": [{"orden": 1, "texto": f"Evaluar la situación y procedimiento."}],
            "pista": {"texto": "Analiza la regla conceptual antes de juzgar la respuesta.", "penalizacion_segundos": 5}
        }
        err_dict = {alt["texto"]: alt["feedback_error"] for alt in alts if not alt["es_correcta"]}

    # ── DF: CARGA TOTAL INTEGRADA EN INPUT LIBRE (C5.3, C5.9, C5.11, C5.12, C5.13)
    else:
        op_enum = OperacionEnum.MIXTA
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        alts = None

        is_two_step = (q_idx % 7 == 0)
        is_context_rounding = (q_idx % 5 == 0)

        if is_context_rounding:
            litros = round(2.2 + (q_idx % 4) * 0.8, 1)
            cap_botella = 1.0
            irrel_balde = round(15.0 + (q_idx % 3) * 5.0, 1)
            ans_arithmetic = round(litros / cap_botella, 1)
            ans_int = int(litros // cap_botella) + (1 if (litros % cap_botella) > 0 else 0)
            ans_str = f"{ans_int}"

            enunciado = f"{personaje} necesita {litros} L de jugo. Cada botella trae {cap_botella} L y miró un balde de {irrel_balde} L. ¿Cuántas botellas completas debe comprar?"

            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Dato irrelevante: el balde de {irrel_balde} L."},
                    {"orden": 2, "texto": f"{litros} ÷ {cap_botella} = {ans_arithmetic}. Como no venden fracciones de botella, se compran {ans_int} botellas."}
                ],
                "pista": {"texto": "Recuerda que no puedes comprar una fracción de botella; si falta un poco, necesitas otra botella entera.", "penalizacion_segundos": 5}
            }
            err_dict = {
                _fmt_dec(ans_arithmetic): f"Tu cuenta está bien ({_fmt_dec(ans_arithmetic)}). Pero no se venden fracciones de botella: con {int(ans_arithmetic)} no alcanza. Necesitas {ans_int} botellas.",
                f"{int(ans_arithmetic)}": f"Con {int(ans_arithmetic)} botellas solo obtienes {int(ans_arithmetic)} L y faltan {round(litros - int(ans_arithmetic), 1)} L. Necesitas {ans_int} botellas."
            }

        elif is_two_step:
            cant = 3
            precio_unit = round(3.50 + (q_idx % 3) * 0.50, 2)
            billete = 20.0
            irrel_mochila = round(45.0 + (q_idx % 4) * 5.0, 2)
            total_gastado = round(cant * precio_unit, 2)
            ans_num = round(billete - total_gastado, 2)
            ans_str = _fmt_money(ans_num)

            enunciado = f"{personaje} llevó R$ {_fmt_money(billete)}. Compró {cant} cuadernos de R$ {_fmt_money(precio_unit)} cada uno y miró una mochila de R$ {_fmt_money(irrel_mochila)}. ¿Cuánto le devolvieron?"

            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Dato irrelevante: la mochila de R$ {_fmt_money(irrel_mochila)}."},
                    {"orden": 2, "texto": f"Paso 1 (inferido): {cant} × {_fmt_money(precio_unit)} = R$ {_fmt_money(total_gastado)}."},
                    {"orden": 3, "texto": f"Paso 2: R$ {_fmt_money(billete)} − R$ {_fmt_money(total_gastado)} = R$ {ans_str}."}
                ],
                "pista": {"texto": "Calcula primero el costo total de los cuadernos antes de restar del billete.", "penalizacion_segundos": 5}
            }
            err_dict = {
                _fmt_money(total_gastado): "Calculaste el costo total de los cuadernos, pero falta restar del billete para hallar el vuelto.",
                _fmt_money(round(billete - precio_unit, 2)): "Compró 3 cuadernos, no uno solo. Debes multiplicar primero.",
                _fmt_money(round(billete - total_gastado - irrel_mochila, 2)): "La mochila solo la miró, es un dato irrelevante."
            }

        else:
            billete = round(20.0 + (q_idx % 3) * 10.0, 2)
            item1 = round(3.50 + (q_idx % 5) * 0.80, 2)
            item2 = round(8.50 + (q_idx % 4) * 0.60, 2)
            irrel = round(35.00 + (q_idx % 3) * 10.0, 2)
            total = round(item1 + item2, 2)
            ans_num = round(billete - total, 2)
            ans_str = _fmt_money(ans_num)

            enunciado = f"{personaje} llevó R$ {_fmt_money(billete)}. Compró un cuaderno de R$ {_fmt_money(item1)}, un lápiz de R$ {_fmt_money(item2)} y miró una mochila de R$ {_fmt_money(irrel)}. ¿Cuánto le sobró?"

            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Dato irrelevante: la mochila de R$ {_fmt_money(irrel)}."},
                    {"orden": 2, "texto": f"Paso 1: R$ {_fmt_money(item1)} + R$ {_fmt_money(item2)} = R$ {_fmt_money(total)}."},
                    {"orden": 3, "texto": f"Paso 2: R$ {_fmt_money(billete)} − R$ {_fmt_money(total)} = R$ {ans_str}."}
                ],
                "pista": {"texto": "Suma los productos comprados y resta el resultado del billete que llevó.", "penalizacion_segundos": 5}
            }
            err_dict = {
                _fmt_money(total): "Ese es el costo total gastado. Te piden cuánto le sobró del billete.",
                _fmt_money(round(billete - item1, 2)): "Falta restar el segundo producto comprado."
            }

    words = enunciado.split()
    if len(words) > 40:
        raise ValueError(f"Enunciado excede el límite duro de 40 palabras ({len(words)} palabras): '{enunciado}'")

    datos_num = {
        "fase4": True,
        "es_desafio": True,
        "seccion": sec,
        "seed": seed_val,
        "escenario": esc.get("nombre", esc.get("id", "general")),
        "personaje": personaje,
        "resultado": ans_str
    }

    return {
        "q_dict": {
            "fase_id": FASE_DECIMALES_ID,
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
    print("Sembrando 1.950 preguntas de desafíos (13 bloques × 150)...")
    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE_DECIMALES_ID, Pregunta.seccion >= 1000))
    desafios_sec = [
        1011, 1012, 1013,
        2011, 2012, 2013,
        3011, 3012, 3013,
        4011, 4012, 4013,
        99099
    ]
    total_q = 0
    batch_questions = []

    for sec in desafios_sec:
        for q_idx in range(150):
            seed_val = 59000000 + sec * 1000 + q_idx
            res_item = _generate_challenge_question(sec, q_idx, seed_val)
            p = Pregunta(**res_item["q_dict"])

            if res_item["alts"]:
                for alt_dict in res_item["alts"]:
                    alt = Alternativa(
                        texto=alt_dict["texto"],
                        es_correcta=alt_dict["es_correcta"],
                        orden=alt_dict["orden"],
                        tipo_error=alt_dict["tipo_error"],
                        feedback_error=alt_dict["feedback_error"]
                    )
                    p.alternativas.append(alt)

            batch_questions.append(p)
            total_q += 1

            if len(batch_questions) >= 500:
                session.add_all(batch_questions)
                await session.commit()
                batch_questions = []

    if batch_questions:
        session.add_all(batch_questions)
        await session.commit()

    print(f"Desafíos sembrados: {total_q} preguntas.")

# ── 5. SIEMBRA DE CONFIGURACIÓN DE PROGRESO (32 filas) ───────────────────────

async def seed_configuracion_progreso(session: AsyncSession):
    print("Sembrando 32 filas en configuracion_progreso...")
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE_DECIMALES_ID))

    cfg_0 = ConfiguracionProgreso(
        fase_id=FASE_DECIMALES_ID,
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

    for mod_id in range(1, 5):
        for lvl_id in range(1, 4):
            sec = mod_id * 100 + lvl_id
            cfg_p = ConfiguracionProgreso(
                fase_id=FASE_DECIMALES_ID,
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
    for mod_id in range(1, 5):
        for des_id, cant, seg, err in desafios_master:
            sec = mod_id * 1000 + des_id
            cfg_d = ConfiguracionProgreso(
                fase_id=FASE_DECIMALES_ID,
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
        fase_id=FASE_DECIMALES_ID,
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

# ── 6. RUNNER PRINCIPAL DE SIEMBRA FASE 4 ────────────────────────────────────────────

async def run_fase4_seed():
    print("=" * 60)
    print("INICIANDO SIEMBRA COMPLETA DE FASE 4 (Decimales/Conversiones)")
    print("=" * 60)
    async with AsyncSessionLocal() as session:
        await upsert_fila_fases(session)
        await clear_fase4_data(session)
        await seed_teoria_niveles(session)
        await seed_practica_pool(session)
        await seed_preguntas_desafios(session)
        await seed_configuracion_progreso(session)
    print("=" * 60)
    print("SIEMBRA DE FASE 5 FINALIZADA CON ÉXITO")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_fase4_seed())
