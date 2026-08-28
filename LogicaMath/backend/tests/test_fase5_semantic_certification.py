"""Regresión de los defectos pedagógicos y de UX hallados en Fase 5."""

import json
import re
from pathlib import Path

from app.fase5.compositor_fase5 import CompositorFase5
from app.fase5.contenido_teoria import TEORIA_FASE5
from app.fase5.theory_examples import obtener_ejemplos_expandidos_fase5


def test_all_published_families_are_complete_and_do_not_copy_the_answer():
    comp = CompositorFase5()
    forbidden = re.compile(
        r"¿Cuánto es (?:las|los)\b|(?:regala|dona)[^?!.]*estudiantes|"
        r"(?:gasta|gastó|gastado)[^?!.]*caramelos|¿Cuál es (?:dos|tres|cuatro)\b|"
        r"\b1\s+(?:[A-Za-zÁÉÍÓÚÑáéíóúñ]+\s+)?(?:están|fueron|son)\b|"
        r"¿Cuánt[oa]s\s+(?:parte|porción|celda|caja|división|grupo|taza|litro|gramo|vaso|cuadrado|parcela)\b",
        re.IGNORECASE,
    )
    for module in range(1, 5):
        for level in range(1, 4):
            for family in range(comp.family_count(module, level)):
                for variant in range(10):
                    item = comp.componer_pregunta_practica(
                        module, level, family, variant,
                        5_000_000 + module * 100_000 + level * 10_000 + family * 100 + variant,
                    )
                    answer = item["respuesta_correcta"]
                    assert not forbidden.search(item["enunciado"])
                    assert not re.search(rf"(?<!\d){re.escape(answer)}(?!\d)", item["enunciado"])
                    assert len(item["opciones_meta"]) == 4
                    assert len({option["texto"] for option in item["opciones_meta"]}) == 4
                    assert sum(option["es_correcta"] for option in item["opciones_meta"]) == 1
                    assert all(option["feedback_error"] for option in item["opciones_meta"] if not option["es_correcta"])
                    visual = item["datos_numericos"]
                    assert visual["requiere_figura"] is True
                    assert visual["tipo_visual"]
                    if module == 2:
                        assert visual["etiqueta_elementos"]
                    if module == 3 and level in (1, 2):
                        assert visual["tipo_visual"] == "hundred_grid"
                        assert visual["porcentaje"] > 0


def test_equivalence_visual_targets_only_the_requested_term():
    comp = CompositorFase5()
    assert comp.family_count(1, 2) == 13
    families = [
        template for template in comp.plantillas
        if template["modulo_id"] == 1 and template["nivel_id"] == 2
    ]
    assert {
        "inferir_factor", "simplificar_inversa", "leer_subdivision",
        "contar_cortes", "detectar_error", "simplificar",
        "comparar_representaciones",
    } <= {template.get("habilidad") for template in families}
    assert len({template["formula"] for template in families}) >= 7
    assert not any(template["id"] in comp._PLANTILLAS_PEDAGOGICAMENTE_EXCLUIDAS for template in families)

    for family in range(comp.family_count(1, 2)):
        for variant in range(4):
            item = comp.componer_pregunta_practica(1, 2, family, variant, 8_260_000 + family * 10 + variant)
            visual = item["datos_numericos"]
            assert visual["tipo_visual"] == "equivalence_strip"
            assert visual["objetivo_visual"]
            assert "expresion_visual" not in visual
            assert "×" not in visual["objetivo_visual"]
            assert set(visual["fraccion_izquierda"]) == {"numerador", "denominador"}
            assert set(visual["fraccion_derecha"]) == {"numerador", "denominador"}
            visible_terms = {
                str(value)
                for fraction in (visual["fraccion_izquierda"], visual["fraccion_derecha"])
                for value in fraction.values()
                if value is not None
            }
            assert item["respuesta_correcta"] not in visible_terms
            assert len(item["explicacion_pasos"]) >= 4


def test_theory_matches_the_twelve_published_levels():
    expected = {(module, level) for module in range(1, 5) for level in range(1, 4)}
    assert set(TEORIA_FASE5) == expected
    for key in expected:
        theory = TEORIA_FASE5[key]
        examples = obtener_ejemplos_expandidos_fase5(*key)
        assert len(theory["parrafos"]) >= 3
        assert theory["diccionario"]
        assert len(examples) == 4
        for example in examples:
            assert example["enunciado"].strip()
            assert [step["orden"] for step in example["pasos"]] == [1, 2, 3]
            assert all(step["texto"].strip() for step in example["pasos"])

    assert all("descuento" in ex["enunciado"].lower() or "recargo" in ex["enunciado"].lower()
               for ex in obtener_ejemplos_expandidos_fase5(3, 2))
    assert all("promedio" in ex["enunciado"].lower()
               for ex in obtener_ejemplos_expandidos_fase5(3, 3))
    assert any("quedan libres" in ex["enunciado"].lower()
               for ex in obtener_ejemplos_expandidos_fase5(1, 3))


def test_no_mirror_flow_and_mandatory_ten_second_error_pause():
    root = Path(__file__).resolve().parents[1]
    phase_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (root / "app" / "fase5").rglob("*.py")
    ).lower()
    assert "pregunta_espejo" not in phase_source
    assert "es_espejo" not in phase_source

    router = (root / "app" / "fase5" / "router.py").read_text(encoding="utf-8")
    assert "pausa_obligatoria_segundos=0 if es_correcta else 10" in router


def test_mixed_challenge_uses_only_its_certified_section():
    root = Path(__file__).resolve().parents[1]
    router = (root / "app" / "fase5" / "router.py").read_text(encoding="utf-8")
    pool_query = router.split("# Cada bloque consume", 1)[1].split(
        "preguntas_db = result_q.scalars().all()", 1
    )[0]
    assert "Pregunta.seccion == seccion" in pool_query
    assert "if is_challenge and modulo_id == 99" not in pool_query


def test_graduation_copy_describes_the_real_topology():
    root = Path(__file__).resolve().parents[1]
    router = (root / "app" / "fase5" / "router.py").read_text(encoding="utf-8")
    assert "12 de práctica, 12 desafíos y 1 desafío mixto" in router
    assert "13 de práctica y 12 desafíos" not in router
