"""Contrato de contenido y operación para los simulacros de Fase 9."""

import random

from app.api.rutas.simulados import FASE_ID, PREGUNTAS_POR_SIMULACRO, router
from app.fase11.banco_simulados import BANCO_SIMULADOS
from app.fase11.seed_fase9 import _cuatro_alternativas


def test_fase9_uses_the_live_phase9_contract():
    assert FASE_ID == 9
    assert router.prefix == "/fases/9/simulados"
    assert PREGUNTAS_POR_SIMULACRO == 10


def test_fase9_source_bank_is_complete_and_has_unique_options():
    assert len(BANCO_SIMULADOS) >= 200
    enunciados = set()
    for item in BANCO_SIMULADOS:
        assert item["tema"].strip()
        assert item["enunciado"].strip()
        assert item["explicacion"].strip()
        assert item["correcta"].strip()
        assert item["dificultad"] in {1, 2, 3}
        assert len(item["distractores"]) >= 3
        opciones = _cuatro_alternativas(item)
        assert len(opciones) == len(set(opciones)) == 4
        assert item["enunciado"] not in enunciados
        enunciados.add(item["enunciado"])


def test_all_twenty_simulacros_receive_ten_distinct_valid_questions():
    for numero in range(1, 21):
        indices = random.Random(9_900_000 + numero).sample(range(len(BANCO_SIMULADOS)), 10)
        assert len(indices) == PREGUNTAS_POR_SIMULACRO
        assert len(indices) == len(set(indices))
        for orden, indice in enumerate(indices, start=1):
            item = BANCO_SIMULADOS[indice]
            alternativas = _cuatro_alternativas(item)
            random.Random(9_910_000 + numero * 100 + orden).shuffle(alternativas)
            letra_correcta = "ABCD"[alternativas.index(item["correcta"])]
            assert alternativas["ABCD".index(letra_correcta)] == item["correcta"]
