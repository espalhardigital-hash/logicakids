"""Contratos de publicación del banco de Fase 7.

Comprueban que cada familia conserve identidad, enunciado y respuesta, y que
las figuras generadas para orientación, coordenadas y tiempo lleguen a la UI.
"""

import asyncio
import base64
import random

import pytest

from app.fase7.seed_fase7 import (
    _gen_fase7_pool, _generate_svg_route_options,
    _generate_svg_time_addition, _generate_svg_transit_route,
)


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


def _decode_svg(data_url: str) -> str:
    return base64.b64decode(data_url.split(",", 1)[1]).decode("utf-8")


def test_time_and_route_visuals_never_reveal_the_solution():
    time_svg = _decode_svg(_generate_svg_time_addition(1, 45, 2, 30))
    transit_svg = _decode_svg(_generate_svg_transit_route(18, 10, 22))
    options_svg = _decode_svg(_generate_svg_route_options(28, 16, 37))

    assert "4h 15m" not in time_svg
    assert "50 min" not in transit_svg
    assert "⭐" not in options_svg
    assert "Total = ?" in time_svg
    assert "Tiempo total: ?" in transit_svg
