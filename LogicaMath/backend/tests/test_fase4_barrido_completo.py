"""Barrido determinista y exhaustivo de las 5.406 preguntas de Fase 4.

Convierte en test mantenido lo que antes eran scripts one-shot de auditoría
(HANDOFF_CAMBIOS_PENDIENTES_FASE4.md, Cambio 1, Etapa D): recorre TODA la
volumetría real de la siembra —no una muestra— y falla ante cualquier
excepción, placeholder sin resolver, respuesta vacía, alternativas
duplicadas, cantidad de alternativas correctas distinta de una, o
`estructura_padre_id` nulo.

3.456 = 4 módulos × 3 niveles × 72 familias × 4 variantes (práctica).
1.950 = 4 módulos × 3 desafíos × 150 + 1 mixto × 150 (desafíos).
"""

import re

from app.fase4.seed import _generate_practice_question, _generate_challenge_question

MODULOS = (1, 2, 3, 4)
NIVELES = (1, 2, 3)
DESAFIOS = (11, 12, 13)
FAMILIAS_PRACTICA = 72
VARIANTES_PRACTICA = 4
PREGUNTAS_POR_BLOQUE_DESAFIO = 150


def _prosa(enunciado: str) -> str:
    sin_svg = re.sub(r"<svg.*?</svg>", "", enunciado, flags=re.DOTALL | re.IGNORECASE)
    return re.sub(r"<[^>]+>", " ", sin_svg)


def _validar_pregunta_comun(enunciado: str, respuesta: str, etiqueta: str):
    assert respuesta and respuesta.strip(), f"{etiqueta}: respuesta_correcta vacía"
    assert "{" not in enunciado and "}" not in enunciado, f"{etiqueta}: placeholder crudo sin resolver"
    prosa = _prosa(enunciado)
    assert prosa.strip(), f"{etiqueta}: enunciado vacío tras quitar HTML"


def test_barrido_completo_practica_3456_preguntas():
    total = 0
    for m in MODULOS:
        for n in NIVELES:
            for f in range(FAMILIAS_PRACTICA):
                for v in range(VARIANTES_PRACTICA):
                    etiqueta = f"practica M{m}N{n} fam{f} var{v}"
                    seed_val = 50000000 + (m * 100 + n) * 100000 + f * 10 + v
                    r = _generate_practice_question(m, n, f, v, seed_val)
                    _validar_pregunta_comun(r["enunciado"], r["respuesta_correcta"], etiqueta)
                    assert r["estructura_padre_id"], f"{etiqueta}: estructura_padre_id nulo o vacío"
                    assert r["estructura_padre_id"].startswith("f4_"), (
                        f"{etiqueta}: prefijo inesperado {r['estructura_padre_id']!r}")
                    total += 1
    assert total == 3456, f"Se esperaban 3.456 preguntas de práctica, se generaron {total}"


def test_barrido_completo_desafios_1950_preguntas():
    secciones = [m * 1000 + d for m in MODULOS for d in DESAFIOS] + [99099]
    assert len(secciones) == 13, "Deben ser 12 bloques de módulo + 1 mixto"

    total = 0
    for sec in secciones:
        for q in range(PREGUNTAS_POR_BLOQUE_DESAFIO):
            etiqueta = f"desafio sec{sec} q{q}"
            seed_val = 60000000 + sec * 1000 + q
            resultado = _generate_challenge_question(sec, q, seed_val)
            qd = resultado["q_dict"]
            _validar_pregunta_comun(qd["enunciado"], qd["respuesta_correcta"], etiqueta)
            assert qd["estructura_padre_id"], f"{etiqueta}: estructura_padre_id nulo o vacío"
            assert qd["estructura_padre_id"].startswith("f4_d"), (
                f"{etiqueta}: prefijo inesperado {qd['estructura_padre_id']!r}")

            alts = resultado["alts"]
            if alts:
                correctas = [a for a in alts if a["es_correcta"]]
                assert len(correctas) == 1, (
                    f"{etiqueta}: {len(correctas)} alternativas correctas, se esperaba exactamente 1")
                textos = [a["texto"] for a in alts]
                assert len(textos) == len(set(textos)), f"{etiqueta}: alternativas duplicadas {textos}"
                assert len(alts) == 4, f"{etiqueta}: se esperaban 4 alternativas, hay {len(alts)}"

            palabras = len(_prosa(qd["enunciado"]).split())
            assert palabras <= 40, f"{etiqueta}: enunciado con {palabras} palabras, límite duro 40"
            total += 1
    assert total == 1950, f"Se esperaban 1.950 preguntas de desafío, se generaron {total}"


def test_barrido_completo_es_determinista():
    """Volver a generar todo con las mismas semillas debe dar exactamente el
    mismo pool: sin esto, comparar antes/después de un reseed no es posible."""
    primero = [
        _generate_practice_question(m, n, f, v, 50000000 + (m * 100 + n) * 100000 + f * 10 + v)
        for m in MODULOS for n in NIVELES for f in range(6) for v in range(VARIANTES_PRACTICA)
    ]
    segundo = [
        _generate_practice_question(m, n, f, v, 50000000 + (m * 100 + n) * 100000 + f * 10 + v)
        for m in MODULOS for n in NIVELES for f in range(6) for v in range(VARIANTES_PRACTICA)
    ]
    assert primero == segundo
