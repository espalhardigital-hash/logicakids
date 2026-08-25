"""Contratos de publicación del banco de Fase 6.

Protegen el enunciado, la respuesta, la identidad de familia y la relación
explícita entre una pregunta y la figura que necesita para resolverse.
"""

import pytest

from app.fase6.seed import _gen_challenge_question, _gen_practice_question, _get_confusiones_map


PRACTICE_LEVELS = (
    (1, 1, 101), (1, 2, 102), (1, 3, 103), (1, 4, 104),
    (2, 1, 201), (2, 2, 202), (2, 3, 203),
    (3, 1, 301), (3, 2, 302), (3, 3, 303), (3, 4, 304), (3, 5, 305),
    (4, 1, 401), (4, 2, 402), (4, 3, 403),
)


@pytest.mark.parametrize("modulo,nivel,seccion", PRACTICE_LEVELS)
def test_practice_questions_have_identity_and_visual_contract(modulo, nivel, seccion):
    families = set()
    confusions = _get_confusiones_map(modulo)
    for family_index in range(120):
        for variant_index in range(4):
            question, _ = _gen_practice_question(modulo, nivel, seccion, family_index, variant_index, confusions)
            data = question["datos_numericos"]
            assert question["enunciado"].strip()
            assert question["respuesta_correcta"].strip()
            assert data["plantilla_id"]
            assert data["tipo_visual"] in {"inline_svg", "textual"}
            assert data["requiere_figura"] == ("<svg" in question["enunciado"].lower())
            families.add(data["plantilla_id"])
    assert len(families) == 120


@pytest.mark.parametrize("modulo,desafio,seccion", (
    (1, 1, 1011), (1, 2, 1012), (1, 3, 1013),
    (2, 1, 2011), (2, 2, 2012), (2, 3, 2013),
    (3, 1, 3011), (3, 2, 3012), (3, 3, 3013),
    (4, 1, 4011), (4, 2, 4012), (4, 3, 4013), (1, 4, 99099),
))
def test_challenge_questions_always_ship_their_required_figure(modulo, desafio, seccion):
    question, _ = _gen_challenge_question(modulo, desafio, seccion, 0, _get_confusiones_map(modulo))
    data = question["datos_numericos"]
    assert question["enunciado"].strip()
    assert "<svg" in question["enunciado"].lower()
    assert data["plantilla_id"]
    assert data["requiere_figura"] is True
    assert data["tipo_visual"] == "inline_svg"
