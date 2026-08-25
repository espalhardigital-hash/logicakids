"""Contratos de publicación del banco Fase 5.

Protegen figura ausente/incompatible, enunciado vacío y reducción de
diversidad estructural, fallas que un test de fórmula no detecta.
"""

import pytest

from app.fase5.compositor_fase5 import CompositorFase5


@pytest.fixture(scope="module")
def compositor():
    return CompositorFase5()


def test_every_level_has_twelve_distinct_families(compositor):
    for modulo in range(1, 5):
        for nivel in range(1, 4):
            families = [p for p in compositor.plantillas if p["modulo_id"] == modulo and p["nivel_id"] == nivel]
            assert len(families) == 12
            assert len({p["id"] for p in families}) == 12


@pytest.mark.parametrize("modulo", range(1, 5))
@pytest.mark.parametrize("nivel", range(1, 4))
def test_generated_questions_have_a_resolvable_visual_contract(compositor, modulo, nivel):
    expected_visual = {1: "pizza", 2: "collection_grid", 3: None, 4: "ratio_grid"}[modulo]
    seen_families = set()
    for family in range(12):
        question = compositor.componer_pregunta_practica(
            modulo, nivel, family, family % 5, 810000 + modulo * 10000 + nivel * 1000 + family
        )
        data = question["datos_numericos"]
        seen_families.add(data["plantilla_id"])
        assert question["enunciado"].strip()
        assert question["respuesta_correcta"].strip()
        assert data["requiere_figura"] is True
        assert data["tipo_visual"]
        if expected_visual:
            assert data["tipo_visual"] == expected_visual
        if modulo == 2:
            assert data["total"] > 0
            assert data["grupos"] > 0
            assert data["total"] % data["grupos"] == 0
        if modulo == 3 and nivel == 3:
            assert data["tipo_visual"] == "bar_chart"
            assert data["val_c"] > 0
        if modulo == 4:
            assert data["ratio_a"] > 0 and data["ratio_b"] > 0
    assert len(seen_families) == 12
