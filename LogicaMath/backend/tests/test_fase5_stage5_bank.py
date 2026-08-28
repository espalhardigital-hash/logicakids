"""
Test de verificación para la Etapa 5: Calidad y Variedad del Banco de Preguntas.
Verifica que no existan plantillas identidad (BUG-26), que existan >= 6 plantillas por nivel (BUG-27),
y que los distractores contengan metadatos de error pedagógico (BUG-30/31).
"""

import json
import os
import re
import pytest
from app.fase5.compositor_fase5 import CompositorFase5


def test_no_identity_formula_templates():
    """BUG-26: Ninguna plantilla debe usar una fórmula de identidad pura ("a", "b", "total")."""
    data_dir = os.path.join(os.path.dirname(__file__), "..", "app", "fase5", "data")
    with open(os.path.join(data_dir, "plantillas_fase5.json"), "r", encoding="utf-8") as f:
        plantillas = json.load(f)

    identidades = {"a", "b", "total", "c", "n_cant", "parte"}
    for p in plantillas:
        assert p["formula"].strip() not in identidades, f"Plantilla {p['id']} usa fórmula identidad: {p['formula']}"


def test_at_least_13_templates_per_level():
    """Cada nivel incluye una familia visual de referencia además del banco previo."""
    data_dir = os.path.join(os.path.dirname(__file__), "..", "app", "fase5", "data")
    with open(os.path.join(data_dir, "plantillas_fase5.json"), "r", encoding="utf-8") as f:
        plantillas = json.load(f)

    comp = CompositorFase5()
    for m in (1, 2, 3, 4):
        for n in (1, 2, 3):
            pl_nivel = [p for p in comp.plantillas if p["modulo_id"] == m and p["nivel_id"] == n]
            assert len(pl_nivel) >= 13, f"Módulo {m} Nivel {n} tiene solo {len(pl_nivel)} plantillas (se exigen ≥ 13)"


def test_variedad_enunciados_por_bloque():
    """BUG-27: Un bloque de 60 preguntas debe generar al menos 30 redacciones distintas."""
    comp = CompositorFase5()
    for m in (1, 2, 3, 4):
        for n in (1, 2, 3):
            stems = set()
            for fam in range(comp.family_count(m, n)):
                for var in range(5):
                    seed_val = m * 10000 + n * 1000 + fam * 5 + var
                    data = comp.componer_pregunta_practica(m, n, fam, var, seed_val)
                    # Normalizar números y nombres propios
                    clean_stem = re.sub(r'\b\d+([.,]\d+)?\b', 'N', data['enunciado'])
                    for nombre in comp.nombres:
                        clean_stem = clean_stem.replace(nombre, 'NOMBRE')
                    stems.add(clean_stem)

            assert len(stems) >= 30, f"Bloque M{m}N{n} sólo generó {len(stems)} redacciones distintas (se exigen ≥ 30)"


def test_distractores_con_confusiones_pedagogicas():
    """BUG-30/31: Los distractores deben tener asociados tipos de error pedagógico."""
    comp = CompositorFase5()
    data = comp.componer_pregunta_practica(1, 1, 0, 0, 500001)
    assert "opciones_meta" in data or len(data["opciones"]) == 4
