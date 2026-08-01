"""Regresión de dos defectos confirmados en HANDOFF_CAMBIOS_PENDIENTES_FASE4.md:

1. El feedback cognitivo de las 3.456 preguntas de práctica y las preguntas
   numéricas de desafío (DF) nunca llegaba al alumno: el seed guardaba
   `errores_previstos` como un dict plano {texto: feedback}, pero
   `router.py` lee `errores_previstos["respuestas_erroneas"]` (una lista de
   {valor, tipo_error, feedback}). La clave nunca coincidía, así que
   `.get("respuestas_erroneas", [])` devolvía `[]` siempre.

2. La plantilla D2 de división (módulo 3) afirmaba de forma incondicional
   que "el resultado es entero", aunque para varias combinaciones de
   dividendo/divisor el cociente real es decimal.

Ambos se corrigen aquí para que no puedan volver a colarse sin que un test
los detecte primero.
"""

import re

import pytest

from app.fase4.seed import (
    _construir_errores_previstos,
    _generate_practice_question,
    _generate_challenge_question,
)
from app.utils.math_utils import normalize_response
from app.models.enums import TipoErrorEnum

SECCIONES_DESAFIO = [m * 1000 + d for m in (1, 2, 3, 4) for d in (11, 12, 13)] + [99099]


def _esquema_canonico_valido(ep: dict) -> bool:
    if not isinstance(ep, dict):
        return False
    if "respuestas_erroneas" not in ep or "calculo" not in ep:
        return False
    for item in ep["respuestas_erroneas"]:
        if set(item) < {"valor", "tipo_error", "feedback"}:
            return False
        try:
            TipoErrorEnum(item["tipo_error"])
        except ValueError:
            return False
        if not item["feedback"]:
            return False
    return True


def test_construir_errores_previstos_produce_el_esquema_que_lee_el_router():
    ep = _construir_errores_previstos(
        [("12,00", TipoErrorEnum.VALOR_POSICIONAL, "Revisa la coma.")],
        "Vuelve a intentarlo.",
    )
    assert ep == {
        "respuestas_erroneas": [
            {"valor": "12,00", "tipo_error": "valor_posicional", "feedback": "Revisa la coma."}
        ],
        "calculo": "Vuelve a intentarlo.",
    }


def test_errores_previstos_de_practica_tienen_esquema_canonico():
    """Regresión: antes era un dict plano {texto: feedback} sin la clave
    'respuestas_erroneas' que el router necesita para encontrar algo."""
    for m in (1, 2, 3, 4):
        for n in (1, 2, 3):
            for f in range(12):
                for v in range(4):
                    r = _generate_practice_question(m, n, f, v, 9000 + f * 4 + v)
                    ep = r["errores_previstos"]
                    assert _esquema_canonico_valido(ep), f"M{m}N{n} f{f}v{v}: esquema inválido {ep!r}"


def test_errores_previstos_de_desafios_numericos_tienen_esquema_canonico():
    for sec in SECCIONES_DESAFIO:
        for q in range(20):
            r = _generate_challenge_question(sec, q, 60000000 + sec * 1000 + q)
            ep = r["q_dict"]["errores_previstos"]
            assert _esquema_canonico_valido(ep), f"sec{sec} q{q}: esquema inválido {ep!r}"


def test_feedback_llega_al_alumno_simulando_la_logica_del_router():
    """Reproduce exactamente el bucle de router.py (búsqueda por valor
    normalizado) para confirmar que, si el alumno escribe un error previsto,
    el feedback correcto se identifica — no solo que el esquema sea válido."""
    r = _generate_practice_question(1, 1, 3, 0, 999001)
    ep = r["errores_previstos"]
    assert ep["respuestas_erroneas"], "esta pregunta debe tener al menos un error previsto"

    esperado = ep["respuestas_erroneas"][0]
    normalized_dada = normalize_response(esperado["valor"], is_money=False)

    feedback_mostrado = None
    tipo_error = None
    for err in ep["respuestas_erroneas"]:
        if normalize_response(err["valor"], is_money=False) == normalized_dada:
            try:
                tipo_error = TipoErrorEnum(err["tipo_error"])
            except ValueError:
                tipo_error = TipoErrorEnum.CALCULO
            feedback_mostrado = err["feedback"]
            break

    assert feedback_mostrado == esperado["feedback"]
    assert tipo_error == TipoErrorEnum(esperado["tipo_error"])


def test_d2_division_es_entero_coincide_con_el_calculo_real():
    """Regresión: la alternativa correcta afirmaba incondicionalmente
    "Sí, el resultado es entero", falso para combinaciones como 4,5 ÷ 1,0."""
    verificadas = 0
    for sec in (1012, 2012, 3012, 4012):
        for q in range(150):
            r = _generate_challenge_question(sec, q, 60000000 + sec * 1000 + q)
            enunciado = r["q_dict"]["enunciado"]
            if "es entero" not in enunciado:
                continue
            m = re.search(r"dividió ([\d,]+) . ([\d,]+) desplazando", enunciado)
            assert m, f"no se pudo parsear el enunciado: {enunciado!r}"
            div = float(m.group(1).replace(",", "."))
            divisor = float(m.group(2).replace(",", "."))
            resultado_real = round(div / divisor, 2)
            es_entero_real = abs(resultado_real - round(resultado_real)) < 1e-9

            correcta = next(a["texto"] for a in r["alts"] if a["es_correcta"])
            afirma_entero = correcta.strip().lower().startswith(("sí", "si"))

            assert afirma_entero == es_entero_real, (
                f"sec{sec} q{q}: {div} ÷ {divisor} = {resultado_real} "
                f"(¿entero? {es_entero_real}), pero la respuesta correcta dice: {correcta!r}"
            )
            verificadas += 1
    assert verificadas >= 20, "la muestra debe cubrir casos entero y no-entero"
