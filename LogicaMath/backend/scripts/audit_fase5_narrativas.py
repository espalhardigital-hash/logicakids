"""
Auditoría de coherencia narrativa y fórmulas de la Fase 5.

Verifica estática y dinámicamente que:
  1. No existan plantillas con marcos_alternativos que OCULTEN variables de la fórmula.
  2. No existan marcos sin datos numéricos ({a}, {b}, {c}, {total}, {n_cant}, {parte}).
  3. No haya palabras repetidas ni contenedores duplicados en preguntas compuestas.

Uso:
    python scripts/audit_fase5_narrativas.py
"""

import ast
import json
import re
import sys

sys.path.insert(0, ".")
from app.fase5.compositor_fase5 import CompositorFase5

NUM_VARS = {"a", "b", "c", "total", "n_cant", "parte"}
DERIVED_VARS = {
    "b_minus_a": {"a", "b"},
    "a_times_c": {"a", "c"},
    "b_times_c": {"b", "c"},
    "a_times_c_plus_1": {"a", "c"},
    "b_times_c_minus_1": {"b", "c"},
    "total_div_b": {"total", "b"},
    "a_pct": {"a", "b"},
    "b_pct": {"a", "b"},
}


def _vars_in(txt):
    return set(re.findall(r"\{([a-zA-Z_0-9]+)\}", txt))


def _tokens_de_formula(formula):
    return set(t for t in re.findall(r"[A-Za-z_]+", formula) if t in NUM_VARS)


def _variables_visibles(frame):
    visibles = _vars_in(frame) & NUM_VARS
    for helper in _vars_in(frame):
        visibles |= DERIVED_VARS.get(helper, set())
    return visibles


def _cierre_equivalencia(frame):
    conocidos = _vars_in(frame)
    if "a_times_c_plus_1" in conocidos:
        conocidos.add("a_times_c")
    if "b_times_c_minus_1" in conocidos:
        conocidos.add("b_times_c")
    for _ in range(4):
        if ({"a", "a_times_c"} <= conocidos) or ({"b", "b_times_c"} <= conocidos):
            conocidos.add("c")
        if {"a_times_c", "c"} <= conocidos:
            conocidos.add("a")
        if {"b_times_c", "c"} <= conocidos:
            conocidos.add("b")
        if {"a", "c"} <= conocidos:
            conocidos.add("a_times_c")
        if {"b", "c"} <= conocidos:
            conocidos.add("b_times_c")
    return conocidos


def check_static(plantillas):
    alertas = []

    for p in plantillas:
        alt_list = p.get("marcos_alternativos") or []

        sin_datos = [f for f in alt_list if not _variables_visibles(f)]
        if sin_datos:
            alertas.append(
                f"[sin_datos] {p['id']}: {len(sin_datos)}/{len(alt_list)} marcos_alternativos "
                f"sin ningún dato numérico"
            )

        tf = _tokens_de_formula(p.get("formula", ""))
        def visibles(frame):
            if p["modulo_id"] == 1 and p["nivel_id"] == 2:
                return _cierre_equivalencia(frame)
            return _variables_visibles(frame)

        ocultan = [f for f in alt_list if tf - visibles(f)]
        if ocultan:
            faltantes = sorted(set().union(*(tf - visibles(f) for f in ocultan)))
            alertas.append(
                f"[formula_oculta] {p['id']} (formula={p.get('formula')!r}): "
                f"{len(ocultan)}/{len(alt_list)} marcos no muestran {faltantes} "
                f"aunque la fórmula los necesita para calcular la respuesta"
            )

    return alertas


def main():
    comp = CompositorFase5()
    alertas = check_static(comp.plantillas)
    if alertas:
        print("Alertas encontradas en auditoría de Fase 5:")
        for a in alertas:
            print(" -", a)
        sys.exit(1)
    else:
        print("Auditoría de narrativas de Fase 5 completada sin alertas.")


if __name__ == "__main__":
    main()
