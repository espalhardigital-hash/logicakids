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
    M1_UNIQUE_FAMS = {101: 18, 102: 21, 103: 18, 104: 25}
    num_fams = M1_UNIQUE_FAMS.get(seccion, 120)
    num_vars = 1 if seccion in M1_UNIQUE_FAMS else 4
    for family_index in range(num_fams):
        for variant_index in range(num_vars):
            question, _ = _gen_practice_question(modulo, nivel, seccion, family_index, variant_index, confusions)
            data = question["datos_numericos"]
            assert question["enunciado"].strip()
            assert question["respuesta_correcta"].strip()
            assert data["plantilla_id"]
            assert data["tipo_visual"] in {"inline_svg", "textual"}
            assert data["requiere_figura"] == ("<svg" in question["enunciado"].lower())
            families.add(data["plantilla_id"])
    assert len(families) == num_fams


CHALLENGE_SECTIONS = (
    (1, 1, 1011, 18), (1, 2, 1012, 18), (1, 3, 1013, 20),
    (2, 1, 2011, 18), (2, 2, 2012, 18), (2, 3, 2013, 20),
    (3, 1, 3011, 18), (3, 2, 3012, 18), (3, 3, 3013, 20),
    (4, 1, 4011, 18), (4, 2, 4012, 18), (4, 3, 4013, 20),
    (1, 4, 99099, 24),
)


@pytest.mark.parametrize("modulo,desafio,seccion,expected_count", CHALLENGE_SECTIONS)
def test_challenge_questions_always_ship_their_required_figure(modulo, desafio, seccion, expected_count):
    confusions = _get_confusiones_map(modulo)
    seen_ids = set()
    for q_idx in range(expected_count):
        question, _ = _gen_challenge_question(modulo, desafio, seccion, q_idx, confusions)
        data = question["datos_numericos"]
        assert question["enunciado"].strip()
        assert question["respuesta_correcta"].strip()
        assert "<svg" in question["enunciado"].lower()
        assert data["plantilla_id"]
        assert data["requiere_figura"] is True
        assert data["tipo_visual"] == "inline_svg"
        seen_ids.add(data["plantilla_id"])
    assert len(seen_ids) == expected_count


def test_geometry_templates_use_a_figure_that_matches_the_statement():
    """Evita volver a dibujar rectángulos para conceptos geométricos distintos."""
    samples = (
        (2, 1, 201, 0, 0, "figura en l", ("tramo horizontal principal", "extensión")),
        (2, 3, 203, 0, 0, "círculo", ("<circle",)),
        (3, 1, 301, 0, 0, "malla", ("<rect", "<polygon")),
        (3, 3, 303, 0, 0, "triángulo", ("<polygon",)),
        (3, 5, 305, 0, 0, "círculo", ("<circle",)),
        (4, 2, 402, 0, 0, "marco de fotos", ("<rect",)),
    )
    for modulo, nivel, seccion, family, variant, phrase, svg_markers in samples:
        question, _ = _gen_practice_question(
            modulo, nivel, seccion, family, variant, _get_confusiones_map(modulo)
        )
        content = question["enunciado"].lower()
        assert phrase in content
        assert "<svg" in content
        assert all(marker in content for marker in svg_markers)


def test_l_perimeter_includes_the_visible_extension():
    question, _ = _gen_practice_question(2, 1, 201, 7, 2, _get_confusiones_map(2))
    data = question["datos_numericos"]
    assert int(question["respuesta_correcta"]) == 2 * (data["w1"] + data["w2"] + data["h1"])
