"""
Seeder autónomo y determinista para la Fase 4: Operatoria Decimal y Conversiones.
Cumple estrictamente con docs/reestructuraciondefases.md y deep_analise_pro §25.4.

Volumetría:
  - 12 niveles en niveles_teoria_pool (NivelTeoria) — 4 módulos × 3 niveles.
  - 3.456 preguntas de práctica (4 módulos × 3 niveles × 72 familias × 4 variantes: 1 original + 3 espejo).
  - 1.950 preguntas de desafíos (13 bloques × 150 preguntas; 12 de módulo + 1 mixto 99099).
  - 26 filas en configuracion_progreso: 1 práctica libre, 12 niveles, 12 desafíos y 1 mixta.

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

# catalogo_fase5.json ya no se lee. Cargarlo al importar ataba este módulo a un
# archivo histórico que el barrido de banco de preguntas va a eliminar. Los
# catálogos vigentes son escenarios_fase4.json, plantillas_fase4.json,
# confusiones_fase4.json y nombres_fase4.json, todos vía CompositorFase4.

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
    print("Purga de datos preexistentes de Fase 4 en cascada...")
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

# ── 3. GENERADOR DE PRÁCTICA (3.456 preguntas = 4 módulos x 3 niveles x 72 fam x 4) ─────

_OP_ENUM_POR_NOMBRE = {
    "sumar": OperacionEnum.SUMA,
    "restar": OperacionEnum.RESTA,
    "multiplicar": OperacionEnum.MULTIPLICACION,
    "dividir": OperacionEnum.DIVISION,
}

_VERBO_OPERACION = {
    "sumar": "Sumamos", "restar": "Restamos",
    "multiplicar": "Multiplicamos", "dividir": "Dividimos",
}


def _fmt_num(v: float) -> str:
    return f"{v:.2f}".replace('.', ',')


def _explicacion_desde_compositor(comp: dict) -> dict:
    """Explicación derivada de la MISMA fórmula y valores que produjeron la respuesta.

    Evita el desfase de construirla con números distintos a los del enunciado.
    """
    vals = comp["valores"]
    formula = comp["formula"]
    legible = formula
    for nombre in ("total", "n_cant", "a", "b", "c"):   # 'total' antes que 'a' para no romper
        legible = legible.replace(nombre, _fmt_num(vals[nombre]) if nombre != "n_cant" else str(vals[nombre]))
    verbo = _VERBO_OPERACION.get(comp["operacion_correcta"], "Operamos")
    return {
        "titulo": "Resolución",
        "pasos": [
            {"orden": 1, "texto": "Alineamos las comas y comprobamos que ambos números tengan la misma cantidad de cifras decimales."},
            {"orden": 2, "texto": f"{verbo} según el planteamiento: {legible}."},
            {"orden": 3, "texto": f"Resultado: {comp['respuesta_correcta']}."},
        ],
    }


def _construir_errores_previstos(pares: list, fallback: str) -> dict:
    """Contrato canónico de `errores_previstos`, consumido por router.py.

    router.py busca `errores_previstos["respuestas_erroneas"]` (lista de
    {valor, tipo_error, feedback}) y usa `errores_previstos["calculo"]` como
    mensaje de respaldo. Guardar aquí cualquier otra forma (ej. un dict plano
    {texto: feedback}) deja el feedback cognitivo calculado pero nunca leído:
    `.get("respuestas_erroneas", [])` siempre devuelve una lista vacía.
    """
    return {
        "respuestas_erroneas": [
            {"valor": valor, "tipo_error": tipo.value, "feedback": feedback}
            for valor, tipo, feedback in pares
        ],
        "calculo": fallback,
    }


def _errores_desde_compositor(comp: dict, confusiones_mod: list) -> dict:
    """Errores previstos anclados al resultado real, con confusiones nombradas (C5.6)."""
    res = comp["resultado_num"]
    pares = []
    # Desplazamiento de coma: el error estructural de toda la fase.
    for desviado in (round(res * 10, 2), round(res / 10, 2)):
        if desviado > 0 and abs(desviado - res) > 0.005:
            pares.append((_fmt_num(desviado), TipoErrorEnum.VALOR_POSICIONAL,
                          "Revisa la posición de la coma decimal en el resultado."))
    # Confusión nombrada del catálogo (no texto genérico).
    if confusiones_mod:
        conf = confusiones_mod[0]
        etiqueta = conf.get("explicacion") or "Revisa el procedimiento paso a paso."
        codigo = (conf.get("codigo") or "").lower()
        tipo = TipoErrorEnum.VALOR_POSICIONAL if ("coma" in codigo or "alinear" in codigo) else TipoErrorEnum.CALCULO
        candidato = round(res + 0.1, 2)
        if abs(candidato - res) > 0.005:
            pares.append((_fmt_num(candidato), tipo, etiqueta))
    return _construir_errores_previstos(pares, "Revisa tus cálculos e inténtalo de nuevo.")


def _con_unidad(valor: str, unidad: str) -> str:
    """'R$ 12,50' para dinero; '12,50 m' para magnitudes físicas."""
    return f"{unidad} {valor}" if unidad in ("R$", "$", "€") else f"{valor} {unidad}"


# Operación que un alumno aplica cuando confunde el sentido del problema.
def _svg_altura(svg: str, altura_px: int) -> str:
    svg = re.sub(r"height='\d+'", f"height='{altura_px}'", svg, count=1)
    return svg.replace(
        "style='",
        f"style='max-height:{altura_px}px; ",
        1,
    )


def _enunciado_con_svg(enunciado: str, figura_svg: str | None, altura_px: int) -> str:
    if not figura_svg:
        return enunciado
    return f"{enunciado}<br/>{_svg_altura(figura_svg, altura_px)}"


_OP_INVERSA = {"sumar": "restar", "restar": "sumar",
               "multiplicar": "dividir", "dividir": "multiplicar"}

_FEEDBACK_INVERSA = {
    "sumar": "Al juntar cantidades se suma, no se resta.",
    "restar": "Cuando algo se quita o se gasta se resta, no se suma.",
    "multiplicar": "Varias cantidades iguales se multiplican, no se dividen.",
    "dividir": "Repartir en partes iguales es dividir, no multiplicar.",
}


def _factor_conversion(formula: str) -> float | None:
    """Factor de la escalera métrica presente en la fórmula (10, 100 o 1000)."""
    for f in (1000.0, 100.0, 10.0):
        if f"{f:g}" in formula:
            return f
    return None


def _alternativas_desde_compositor(comp: dict, rng: random.Random) -> list:
    """4 alternativas ancladas al resultado real y a errores con significado (C5.6).

    Los distractores no son ruido aleatorio: cada uno encarna un error que un
    alumno comete de verdad (operación invertida, coma desplazada, un operando
    olvidado). Sin esto la opción múltiple se resuelve por descarte visual.
    """
    res = comp["resultado_num"]
    unidad = comp["unidad"]
    vals = comp["valores"]
    op = comp["operacion_correcta"]

    correcto = _con_unidad(comp["respuesta_correcta"], unidad)
    candidatos = []

    # 1) Operación invertida respecto a la que pide el enunciado.
    a, b = vals["a"], vals["b"]
    factor = _factor_conversion(comp["formula"])
    if factor:
        # En una conversión el error real es recorrer la escalera métrica al
        # revés, no "repartir en vez de multiplicar": el feedback genérico de
        # operación mentiría sobre lo que el alumno hizo.
        invertido = a * factor if f"/{factor:g}" in comp["formula"] else a / factor
        candidatos.append((round(invertido, 2), TipoErrorEnum.DECIMAL,
                           f"Recorriste la escalera métrica al revés: aquí hay que "
                           f"{'dividir' if f'/{factor:g}' in comp['formula'] else 'multiplicar'} por {factor:g}."))
    else:
        inversos = {"sumar": a - b, "restar": a + b,
                    "multiplicar": (a / b if b else 0), "dividir": a * b}
        candidatos.append((round(inversos.get(op, res + 1), 2),
                           TipoErrorEnum.OPERACION_INCORRECTA,
                           _FEEDBACK_INVERSA.get(op, "Revisa qué operación pide el enunciado.")))

    # 2) Coma desplazada un lugar: el error estructural de toda la fase.
    candidatos.append((round(res * 10, 2), TipoErrorEnum.VALOR_POSICIONAL,
                       "Revisa la posición de la coma decimal en el resultado."))
    candidatos.append((round(res / 10, 2), TipoErrorEnum.VALOR_POSICIONAL,
                       "Corriste la coma un lugar de más al escribir el resultado."))

    # 3) Un operando olvidado.
    candidatos.append((round(res - b, 2), TipoErrorEnum.CALCULO,
                       "Quedó un dato del enunciado sin usar en la cuenta."))

    alts = [{"texto": correcto, "es_correcta": True, "orden": 1,
             "tipo_error": None, "feedback_error": None}]
    usados = {comp["respuesta_correcta"]}
    for valor, tipo_err, fb in candidatos:
        if len(alts) == 4:
            break
        if valor <= 0 or abs(valor - res) < 0.005:
            continue
        # Un distractor 100 veces mayor que la respuesta se descarta de un
        # vistazo y no mide nada. Debe ser plausible para ser útil.
        if valor > res * 100 or valor < res / 100:
            continue
        txt = _fmt_num(valor)
        if txt in usados:
            continue
        usados.add(txt)
        alts.append({"texto": _con_unidad(txt, unidad), "es_correcta": False,
                     "orden": len(alts) + 1, "tipo_error": tipo_err, "feedback_error": fb})

    # Relleno determinista si algún candidato quedó descartado por colisión.
    paso = 0.15
    while len(alts) < 4:
        paso += 0.15
        txt = _fmt_num(round(res + paso, 2))
        if txt in usados:
            continue
        usados.add(txt)
        alts.append({"texto": _con_unidad(txt, unidad), "es_correcta": False,
                     "orden": len(alts) + 1, "tipo_error": TipoErrorEnum.CALCULO,
                     "feedback_error": "Repite la cuenta comprobando cada cifra decimal."})

    rng.shuffle(alts)
    for i, alt in enumerate(alts):
        alt["orden"] = i + 1
    return alts


def _generate_practice_question(modulo_id: int, nivel_id: int, fam_idx: int, var_idx: int, seed_val: int) -> dict:
    rng = random.Random(seed_val)
    sec = modulo_id * 100 + nivel_id
    fam_id = f"f4_m{modulo_id}_l{nivel_id}_fam_{fam_idx:03d}"
    es_espejo = (var_idx > 0)
    personaje = NOMBRES_POOL[(fam_idx + var_idx) % len(NOMBRES_POOL)]

    # ── Compositor: ÚNICA fuente del enunciado, la respuesta y la explicación ──
    # No hay generador de reserva a propósito. El fallback heredado de la fase
    # anterior componía volumen (L, dm³) para el módulo 4 y superficie para un
    # módulo 5 que ya no existe, ambos fuera de la Fase 4 tras C6.5; además leía
    # esc["nombre"] y confusiones_mod[6], ausentes en los catálogos nuevos. Si el
    # compositor no puede componer, la siembra debe fallar y no colar una
    # pregunta de otra magnitud.
    comp = _COMPOSITOR.componer_pregunta_practica(
        modulo_id, nivel_id, fam_idx, var_idx, seed_val
    )
    confusiones_mod = [c for c in _COMPOSITOR.confusiones if c["modulo_id"] == modulo_id]

    enunciado_final = _enunciado_con_svg(comp["enunciado"], comp.get("figura_svg"), 200)
    ans_str = comp["respuesta_correcta"]
    op_enum = _OP_ENUM_POR_NOMBRE.get(comp["operacion_correcta"], OperacionEnum.MIXTA)
    explicacion = _explicacion_desde_compositor(comp)
    err_dict = _errores_desde_compositor(comp, confusiones_mod)
    tipo_preg = (TipoPreguntaEnum.RESPUESTA_NUMERICA if _is_numeric_answer(ans_str)
                 else TipoPreguntaEnum.MULTIPLE_OPCION)

    datos_num = {
        **comp["valores"],
        "fase4": True,
        "seed": seed_val,
        "plantilla_id": comp["plantilla_id"],
        "escenario_id": comp["escenario_id"],
        "personaje": comp["personaje"],
        "formula": comp["formula"],
        "unidad": comp["unidad"],
        "variante": var_idx,
        "es_espejo": es_espejo,
        "resultado": ans_str,
    }

    return {
        "fase_id": FASE_DECIMALES_ID,
        "seccion": sec,
        "estructura_padre_id": fam_id,          # NUNCA None (Tomo 4 §11, F5 req#1)
        "operacion": op_enum,
        "tipo_pregunta": tipo_preg,
        "enunciado": enunciado_final,
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

    # Catálogos de la Fase 4 (escenarios_fase4.json / confusiones_fase4.json),
    # no el CATALOGO_DATA heredado de la fase anterior.
    escenarios_mod = [e for e in _COMPOSITOR.escenarios if e["modulo_id"] == real_mod]
    confusiones_mod = [c for c in _COMPOSITOR.confusiones if c["modulo_id"] == real_mod]
    if not escenarios_mod:
        escenarios_mod = _COMPOSITOR.escenarios
    if not confusiones_mod:
        confusiones_mod = _COMPOSITOR.confusiones
    esc = escenarios_mod[q_idx % len(escenarios_mod)]

    struct_id = f"f4_d{sec}_q{q_idx:03d}"

    des_type = (11 if (q_idx % 3 == 0) else (12 if (q_idx % 3 == 1) else 13)) if des_id == 99 else des_id
    comp_d1 = None          # solo D1 usa el compositor; D2/DF tienen otra estructura

    # ── D1: PROBLEMA DE CONTEXTO EN OPCIÓN MÚLTIPLE (C5.3, C5.5, C5.9) ────────
    if des_type == 11:
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION

        # El desafío D1 recorre los TRES niveles del módulo, no un enunciado fijo:
        # 18 plantillas por módulo frente a 1. Sin esto el alumno memoriza
        # "cuaderno + lápiz = sumar" y el bloque deja de medir razonamiento (C7.1).
        nivel_d1 = ((q_idx // 3) % 3) + 1
        comp = comp_d1 = _COMPOSITOR.componer_pregunta_practica(
            real_mod, nivel_d1, q_idx % 12, q_idx % 4, seed_val
        )
        enunciado = _enunciado_con_svg(comp["enunciado"], comp.get("figura_svg"), 140)
        ans_str = comp["respuesta_correcta"]
        esc = next((e for e in _COMPOSITOR.escenarios
                    if e["id"] == comp["escenario_id"]), esc)
        op_enum = _OP_ENUM_POR_NOMBRE.get(comp["operacion_correcta"], OperacionEnum.MIXTA)
        alts = _alternativas_desde_compositor(comp, rng)
        explicacion = _explicacion_desde_compositor(comp)
        explicacion["pista"] = {
            "texto": "Lee las palabras clave del enunciado para decidir qué operación pide.",
            "penalizacion_segundos": 5,
        }
        err_dict = _construir_errores_previstos(
            [(a["texto"], a["tipo_error"], a["feedback_error"]) for a in alts if not a["es_correcta"]],
            "Revisa qué operación pide el enunciado y vuelve a calcular.")
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
            enunciado = f"{personaje} calculó {_fmt_dec(a)} × {_fmt_dec(b)} y obtuvo {_fmt_dec(res_err)}. ¿Cuál fue su error con la coma?"
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
            # El cociente NO siempre es entero (ej. 4,5 ÷ 1,0 = 4,5): la
            # afirmación "Sí" no puede darse por correcta sin comprobarlo.
            es_entero = abs(ans_val - round(ans_val)) < 1e-9
            enunciado = f"{personaje} dividió {_fmt_dec(div)} ÷ {_fmt_dec(divisor)} desplazando las comas. ¿Tuvo razón al afirmar que el resultado es entero?"
            desplazado = f"{int(div * 10)} ÷ {int(divisor * 10)} = {_fmt_dec(ans_val)}"
            if es_entero:
                correct_alt = f"Sí, porque al desplazar comas obtiene {desplazado}, un número entero"
                alts = [
                    {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
                    {"texto": "No, porque al dividir decimales siempre da decimal", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.CALCULO, "feedback_error": "La división de dos decimales puede dar un cociente entero, como en este caso."},
                    {"texto": "No, porque debió restar las comas", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Las comas se desplazan multiplicando por 10 en dividendo y divisor."},
                    {"texto": "Faltan datos para saber el resultado", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.NO_IDENTIFICA_DATOS, "feedback_error": "Los datos son suficientes para resolver."}
                ]
            else:
                correct_alt = f"No, porque al desplazar comas obtiene {desplazado}, que no es un número entero"
                alts = [
                    {"texto": correct_alt, "es_correcta": True, "orden": 1, "tipo_error": None, "feedback_error": None},
                    {"texto": f"Sí, porque al desplazar comas obtiene {desplazado}", "es_correcta": False, "orden": 2, "tipo_error": TipoErrorEnum.CALCULO, "feedback_error": f"{_fmt_dec(ans_val)} tiene cifras decimales: no es un número entero."},
                    {"texto": "No, porque debió restar las comas", "es_correcta": False, "orden": 3, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Las comas se desplazan multiplicando por 10 en dividendo y divisor."},
                    {"texto": "Faltan datos para saber el resultado", "es_correcta": False, "orden": 4, "tipo_error": TipoErrorEnum.NO_IDENTIFICA_DATOS, "feedback_error": "Los datos son suficientes para resolver."}
                ]
        else:
            val_m = round(1.5 + (q_idx % 4) * 0.5, 1)
            val_cm_err = val_m * 10
            enunciado = _enunciado_con_svg(
                f"{personaje} convirtió {_fmt_dec(val_m)} m a cm y obtuvo {_fmt_dec(val_cm_err)} cm. ¿Dónde cometió el error?",
                tabla_datos(
                    [
                        ("Dato inicial", f"{_fmt_dec(val_m)} m"),
                        ("Resultado dado", f"{_fmt_dec(val_cm_err)} cm"),
                    ],
                    color=color_modulo(4, 4),
                    marco=False,
                ),
                125,
            )
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
        err_dict = _construir_errores_previstos(
            [(a["texto"], a["tipo_error"], a["feedback_error"]) for a in alts if not a["es_correcta"]],
            "Revisa la situación planteada e inténtalo de nuevo.")

    # ── DF: CARGA TOTAL INTEGRADA EN INPUT LIBRE (C5.3, C5.9, C5.11, C5.12, C5.13)
    else:
        op_enum = OperacionEnum.MIXTA
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        alts = None

        is_two_step = (q_idx % 7 == 0)
        is_context_rounding = (q_idx % 5 == 0)

        if real_mod == 4:
            tramo_m = round(1.2 + (q_idx % 5) * 0.3, 1)
            tramo_cm = 35 + (q_idx % 4) * 15
            hora_salida = 8 + (q_idx % 3)
            ans_num = round(tramo_m * 100 + tramo_cm, 2)
            ans_str = _fmt_dec(ans_num)

            enunciado = _enunciado_con_svg(
                f"{personaje} unió dos tramos de una ruta. ¿Cuántos centímetros mide la ruta completa?",
                tabla_datos(
                    [
                        ("Tramo A", f"{_fmt_dec(tramo_m)} m"),
                        ("Tramo B", f"{tramo_cm} cm"),
                        ("Hora de salida", f"{hora_salida}:00"),
                    ],
                    color=color_modulo(4, 4),
                    marco=False,
                ),
                145,
            )
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Dato irrelevante: la hora de salida ({hora_salida}:00) no cambia la longitud."},
                    {"orden": 2, "texto": f"Convertimos el tramo A: {_fmt_dec(tramo_m)} m × 100 = {_fmt_dec(tramo_m * 100)} cm."},
                    {"orden": 3, "texto": f"Sumamos ambos tramos: {_fmt_dec(tramo_m * 100)} + {tramo_cm} = {ans_str} cm."},
                ],
                "pista": {"texto": "Expresa los dos tramos en centímetros antes de sumarlos.", "penalizacion_segundos": 5},
            }
            err_dict = _construir_errores_previstos([
                (_fmt_dec(round(tramo_m * 100, 2)), TipoErrorEnum.PROBLEMA_INCOMPLETO,
                 "Convertiste el primer tramo, pero falta sumar el tramo B."),
                (_fmt_dec(round(tramo_m + tramo_cm, 2)), TipoErrorEnum.VALOR_POSICIONAL,
                 "No puedes sumar metros y centímetros sin unificar las unidades."),
                (_fmt_dec(round(tramo_m * 10 + tramo_cm, 2)), TipoErrorEnum.VALOR_POSICIONAL,
                 "De metros a centímetros se multiplica por 100, no por 10."),
            ], "Revisa la conversión de unidades e inténtalo de nuevo.")

        elif is_context_rounding:
            # C6.5: la Fase 4 trabaja longitud y dinero. El volumen (L) pasó a la
            # fase de geometría 3D, así que el redondeo al alza se plantea con
            # listones, no con botellas.
            largo = round(4.4 + (q_idx % 4) * 1.6, 1)
            cap_liston = 2.0
            irrel_ancho = round(1.2 + (q_idx % 3) * 0.3, 1)
            ans_arithmetic = round(largo / cap_liston, 2)
            ans_int = int(largo // cap_liston) + (1 if (largo % cap_liston) > 0 else 0)
            ans_str = f"{ans_int}"

            enunciado = f"{personaje} debe cubrir {_fmt_dec(largo)} m de zócalo con listones de {_fmt_dec(cap_liston)} m cada uno. El pasillo mide {_fmt_dec(irrel_ancho)} m de ancho. ¿Cuántos listones completos necesita comprar?"

            faltan = round(largo - int(ans_arithmetic) * cap_liston, 2)
            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Dato irrelevante: el ancho del pasillo ({_fmt_dec(irrel_ancho)} m) no interviene en el largo del zócalo."},
                    {"orden": 2, "texto": f"{_fmt_dec(largo)} ÷ {_fmt_dec(cap_liston)} = {_fmt_dec(ans_arithmetic)}. Como no venden listones partidos, se compran {ans_int}."}
                ],
                "pista": {"texto": "No puedes comprar una parte de listón: si sobra un tramo por cubrir, necesitas otro listón entero.", "penalizacion_segundos": 5}
            }
            err_dict = _construir_errores_previstos([
                (_fmt_dec(ans_arithmetic), TipoErrorEnum.PROBLEMA_INCOMPLETO,
                 f"Tu división está bien ({_fmt_dec(ans_arithmetic)}), pero los listones se venden enteros. Necesitas {ans_int}."),
                (f"{int(ans_arithmetic)}", TipoErrorEnum.PROBLEMA_INCOMPLETO,
                 f"Con {int(ans_arithmetic)} listones cubres {_fmt_dec(round(int(ans_arithmetic) * cap_liston, 2))} m y quedan {_fmt_dec(faltan)} m sin cubrir. Necesitas {ans_int}."),
            ], "Recuerda redondear hacia arriba: no se venden listones partidos.")

        elif is_two_step:
            cant = 3
            precio_unit = round(3.50 + (q_idx % 3) * 0.50, 2)
            billete = 20.0
            hora_compra = 14 + (q_idx % 4)
            total_gastado = round(cant * precio_unit, 2)
            ans_num = round(billete - total_gastado, 2)
            ans_str = _fmt_money(ans_num)

            enunciado = f"{personaje} llevó R$ {_fmt_money(billete)}. Compró {cant} cuadernos de R$ {_fmt_money(precio_unit)} cada uno. La compra fue a las {hora_compra}:00. ¿Cuánto le devolvieron?"

            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Dato irrelevante: la hora de la compra ({hora_compra}:00)."},
                    {"orden": 2, "texto": f"Paso 1 (inferido): {cant} × {_fmt_money(precio_unit)} = R$ {_fmt_money(total_gastado)}."},
                    {"orden": 3, "texto": f"Paso 2: R$ {_fmt_money(billete)} − R$ {_fmt_money(total_gastado)} = R$ {ans_str}."}
                ],
                "pista": {"texto": "Calcula primero el costo total de los cuadernos antes de restar del billete.", "penalizacion_segundos": 5}
            }
            err_dict = _construir_errores_previstos([
                (_fmt_money(total_gastado), TipoErrorEnum.PROBLEMA_INCOMPLETO,
                 "Calculaste el costo total de los cuadernos, pero falta restar del billete para hallar el vuelto."),
                (_fmt_money(round(billete - precio_unit, 2)), TipoErrorEnum.CALCULO,
                 "Compró 3 cuadernos, no uno solo. Debes multiplicar primero."),
                (_fmt_money(billete), TipoErrorEnum.PROBLEMA_INCOMPLETO,
                 "Ese es el dinero inicial. Aún falta restar el costo total de los cuadernos."),
            ], "Calcula el costo total de la compra y luego resta del billete.")

        else:
            billete = round(20.0 + (q_idx % 3) * 10.0, 2)
            item1 = round(3.50 + (q_idx % 5) * 0.80, 2)
            item2 = round(8.50 + (q_idx % 4) * 0.60, 2)
            hora_compra = 15 + (q_idx % 3)
            total = round(item1 + item2, 2)
            ans_num = round(billete - total, 2)
            ans_str = _fmt_money(ans_num)

            enunciado = f"{personaje} llevó R$ {_fmt_money(billete)}. Compró un cuaderno de R$ {_fmt_money(item1)}, un lápiz de R$ {_fmt_money(item2)}. La compra fue a las {hora_compra}:00. ¿Cuánto dinero le sobró?"

            explicacion = {
                "titulo": "Resolución",
                "pasos": [
                    {"orden": 1, "texto": f"Dato irrelevante: la hora de la compra ({hora_compra}:00)."},
                    {"orden": 2, "texto": f"Paso 1: R$ {_fmt_money(item1)} + R$ {_fmt_money(item2)} = R$ {_fmt_money(total)}."},
                    {"orden": 3, "texto": f"Paso 2: R$ {_fmt_money(billete)} − R$ {_fmt_money(total)} = R$ {ans_str}."}
                ],
                "pista": {"texto": "Suma los productos comprados y resta el resultado del billete que llevó.", "penalizacion_segundos": 5}
            }
            err_dict = _construir_errores_previstos([
                (_fmt_money(total), TipoErrorEnum.PROBLEMA_INCOMPLETO,
                 "Ese es el costo total gastado. Te piden cuánto le sobró del billete."),
                (_fmt_money(round(billete - item1, 2)), TipoErrorEnum.PROBLEMA_INCOMPLETO,
                 "Falta restar el segundo producto comprado."),
                (_fmt_money(billete), TipoErrorEnum.PROBLEMA_INCOMPLETO,
                 "Ese es el dinero inicial. Todavía falta descontar las compras."),
            ], "Suma lo comprado y resta el resultado del billete.")

    enunciado_prosa = re.sub(r"<svg.*?</svg>", "", enunciado, flags=re.DOTALL | re.IGNORECASE)
    enunciado_prosa = re.sub(r"<[^>]+>", " ", enunciado_prosa)
    words = enunciado_prosa.split()
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
    # D1 viene del compositor: registrar la plantilla hace auditable la variedad
    # estructural del bloque (si no se guarda, no se puede medir).
    if comp_d1 is not None:
        datos_num.update({
            "plantilla_id": comp_d1["plantilla_id"],
            "escenario_id": comp_d1["escenario_id"],
            "formula": comp_d1["formula"],
            "nivel_origen": comp_d1["nivel_id"],
            "valores": comp_d1["valores"],
            "unidad": comp_d1["unidad"],
        })

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

# ── 5. SIEMBRA DE CONFIGURACIÓN DE PROGRESO (26 filas) ───────────────────────

async def seed_configuracion_progreso(session: AsyncSession):
    print("Sembrando 26 filas en configuracion_progreso...")
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
    print("26 filas de `configuracion_progreso` sembradas.")

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
    print("SIEMBRA DE FASE 4 FINALIZADA CON ÉXITO")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_fase4_seed())
