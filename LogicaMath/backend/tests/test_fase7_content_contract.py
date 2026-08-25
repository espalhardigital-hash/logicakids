"""Contratos de publicación del banco de Fase 7.

Comprueban que cada familia conserve identidad, enunciado y respuesta, y que
las figuras generadas para orientación, coordenadas y tiempo lleguen a la UI.
"""

import asyncio
import random

import pytest

from app.fase7.seed_fase7 import _gen_fase7_pool


LEVELS = tuple((modulo, nivel) for modulo in range(1, 5) for nivel in (1, 2, 3, 11, 12, 13))


@pytest.mark.parametrize("modulo,nivel", LEVELS)
def test_generated_questions_are_complete_and_visual(modulo, nivel):
    for sample in range(24):
        question = asyncio.run(_gen_fase7_pool(random.Random(7000 + modulo * 100 + nivel * 10 + sample), modulo, nivel))
        visual = question["metadata_visual"]
        assert question["enunciado"].strip()
        assert question["respuesta_correcta"].strip()
        assert len(set(question["alts"])) == len(question["alts"])
        assert question["respuesta_correcta"] in question["alts"]
        assert visual["requiere_imagen"] is True
        assert visual["svg_base64"].startswith("data:image/svg+xml;base64,")


@pytest.mark.parametrize("modulo,nivel", LEVELS)
def test_each_level_produces_real_variety(modulo, nivel):
    questions = [
        asyncio.run(_gen_fase7_pool(random.Random(9000 + modulo * 1000 + nivel * 100 + sample), modulo, nivel))
        for sample in range(40)
    ]
    assert len({question["enunciado"] for question in questions}) >= 12
