"""Contratos de publicación del banco Fase 5.

Protegen figura ausente/incompatible, enunciado vacío y reducción de
diversidad estructural, fallas que un test de fórmula no detecta.
"""

import pytest

from app.fase5.compositor_fase5 import CompositorFase5


@pytest.fixture(scope="module")
def compositor():
    return CompositorFase5()


def test_every_level_has_reference_family_and_distinct_coverage(compositor):
    for modulo in range(1, 5):
        for nivel in range(1, 4):
            families = [p for p in compositor.plantillas if p["modulo_id"] == modulo and p["nivel_id"] == nivel]
            assert len(families) == 13
            assert len({p["id"] for p in families}) == 13
            assert any(p["id"].startswith("tplr_") for p in families)


def test_equivalence_level_excludes_artificial_operations_on_fraction_terms(compositor):
    families = [p for p in compositor.plantillas if p["modulo_id"] == 1 and p["nivel_id"] == 2]
    assert len(families) == 13
    # Se admiten rutas directas, inversas, inferencia de factor, revisión de
    # errores y conteo de subdivisiones; siguen prohibidas las antiguas sumas,
    # diferencias o dobles arbitrarios de los términos de una fracción.
    assert {p["formula"] for p in families} == {
        "a*c", "b*c", "c", "a", "b", "a*(c-1)", "b*(c-1)",
    }
    assert {p.get("habilidad") for p in families} >= {
        "inferir_factor", "simplificar_inversa", "leer_subdivision",
        "contar_cortes", "detectar_error", "simplificar",
    }
    for family in range(compositor.family_count(1, 2)):
        question = compositor.componer_pregunta_practica(1, 2, family, 0, 825000 + family)
        assert "más el denominador original" not in question["enunciado"]
        assert "suman el nuevo numerador" not in question["enunciado"]
        assert "multiplicando por" not in question["enunciado"].lower()
        assert question["datos_numericos"]["tipo_visual"] == "equivalence_strip"


@pytest.mark.parametrize("modulo", range(1, 5))
@pytest.mark.parametrize("nivel", range(1, 4))
def test_generated_questions_have_a_resolvable_visual_contract(compositor, modulo, nivel):
    allowed_visuals = {
        1: {"pizza", "fraction_strip", "equivalence_strip"},
        2: {"collection_grid", "group_cards"},
        3: {"percentage_beaker", "bar_chart", "hundred_grid", "data_table"},
        4: {"ratio_grid", "ratio_table"},
    }[modulo]
    seen_families = set()
    for family in range(compositor.family_count(modulo, nivel)):
        question = compositor.componer_pregunta_practica(
            modulo, nivel, family, family % 5, 810000 + modulo * 10000 + nivel * 1000 + family
        )
        data = question["datos_numericos"]
        seen_families.add(data["plantilla_id"])
        assert question["enunciado"].strip()
        assert question["respuesta_correcta"].strip()
        assert data["requiere_figura"] is True
        assert data["tipo_visual"]
        assert data["tipo_visual"] in allowed_visuals
        if data["plantilla_id"].startswith("tplr_"):
            assert data["tipo_visual"] in {
                "fraction_strip", "equivalence_strip", "group_cards",
                "hundred_grid", "data_table", "ratio_table",
            }
        if modulo == 2:
            assert data["total"] > 0
            assert data["grupos"] > 0
            assert data["total"] % data["grupos"] == 0
        if modulo == 3 and nivel == 3 and data["tipo_visual"] == "bar_chart":
            assert data["val_c"] > 0
        if data["tipo_visual"] == "data_table":
            assert len(data["valores_tabla"]) == 3
        if modulo == 4:
            assert data["ratio_a"] > 0 and data["ratio_b"] > 0
    assert len(seen_families) == compositor.family_count(modulo, nivel)
