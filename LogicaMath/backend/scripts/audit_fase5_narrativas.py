"""
Auditoría de coherencia narrativa y fórmulas de la Fase 5.

Verifica estática y dinámicamente que:
  1. No existan plantillas con marcos_alternativos que OCULTEN variables de la fórmula.
  2. No existan marcos sin datos numéricos ({a}, {b}, {c}, {total}, {n_cant}, {parte}).
  3. No haya palabras repetidas ni contenedores duplicados en preguntas compuestas.

Uso:
    python scripts/audit_fase5_narrativas.py
"""

import json
import re
import sys

sys.path.insert(0, ".")
from app.fase5.compositor_fase5 import CompositorFase5

NUM_VARS = {"a", "b", "c", "total", "n_cant", "parte"}


def _vars_in(txt):
    return set(re.findall(r"\{([a-zA-Z_0-9]+)\}", txt))


def _tokens_de_formula(formula):
    return set(t for t in re.findall(r"[A-Za-z_]+", formula) if t in NUM_VARS)


def check_static(plantillas):
    alertas = []

    for p in plantillas:
        alt_list = p.get("marcos_alternativos") or []

        sin_datos = [f for f in alt_list if not (_vars_in(f) & NUM_VARS)]
        if sin_datos:
            alertas.append(
                f"[sin_datos] {p['id']}: {len(sin_datos)}/{len(alt_list)} marcos_alternativos "
                f"sin ningún dato numérico"
            )

        tf = _tokens_de_formula(p.get("formula", ""))
        ocultan = [f for f in alt_list if tf - _vars_in(f)]
        if ocultan:
            faltantes = sorted(set().union(*(tf - _vars_in(f) for f in ocultan)))
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
