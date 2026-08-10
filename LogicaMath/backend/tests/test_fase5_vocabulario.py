"""Invariantes de contenido de la Fase 5 (Fracciones, Porcentajes y Proporciones).

Cubre la Fase 5 reconstruida con un arnés de tests de regresión:
  - Enunciado y respuesta derivados de la MISMA fórmula y los MISMOS números.
  - Toda plantilla con al menos un escenario compatible (R1 + R2 + magnitud).
  - Toda variante narrativa muestra TODAS las variables numéricas que la fórmula exige.
  - Ausencia de placeholders crudos, errores gramaticales ("de el", "un agua").
  - Variedad estructural real (firmas estructurales por nivel).
  - Determinismo con semilla.
"""

import ast
import json
import re
import pytest

from app.fase5.compositor_fase5 import CompositorFase5

COMP = CompositorFase5()
NIVELES = [(m, n) for m in (1, 2, 3, 4) for n in (1, 2, 3)]

# Auxiliares narrativos que el compositor precalcula (_valores_auxiliares) y
# que algunos marcos imprimen en vez de las variables crudas -- p.ej. un marco
# puede mostrar "{a_times_c}" (a*c ya resuelto) en lugar de "{a}" y "{c}" por
# separado. Ambas formas son igualmente válidas: lo que importa es que el
# alumno pueda reconstruir el resultado con los números impresos, no que la
# fórmula use exactamente los nombres de variable crudos.
_AUXILIARES_EXPR = {
    "b_minus_a": "b - a",
    "a_times_c": "a * c",
    "b_times_c": "b * c",
    "total_div_b": "total // b",
    "a_pct": "(a * 100) // (a + b)",
    "b_pct": "(b * 100) // (a + b)",
}
_AUXILIARES_AST = {k: ast.dump(ast.parse(v, mode="eval").body) for k, v in _AUXILIARES_EXPR.items()}


def _cubierto(node: ast.AST, impresos: set) -> bool:
    """¿Puede reconstruirse este nodo de la fórmula solo con lo impreso?

    Un nodo está cubierto si es una constante, si es una variable cruda que
    aparece impresa, si coincide exactamente con un auxiliar narrativo
    impreso (mismo subárbol), o si es una operación cuyos dos operandos ya
    están cubiertos.
    """
    dump = ast.dump(node)
    if any(dump == _AUXILIARES_AST[h] for h in impresos if h in _AUXILIARES_AST):
        return True
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.Name):
        return node.id in impresos
    if isinstance(node, ast.BinOp):
        return _cubierto(node.left, impresos) and _cubierto(node.right, impresos)
    if isinstance(node, ast.UnaryOp):
        return _cubierto(node.operand, impresos)
    return False


def _componer_todo(fams=6, vars_=2):
    for m, n in NIVELES:
        for f in range(fams):
            for v in range(vars_):
                yield m, n, COMP.componer_pregunta_practica(m, n, f, v, 9000 + f * 4 + v)


# ── Catálogos ────────────────────────────────────────────────────────────────

def test_plantillas_cubren_los_niveles():
    presentes = {(p["modulo_id"], p["nivel_id"]) for p in COMP.plantillas}
    assert presentes == set(NIVELES), f"Niveles sin plantillas: {set(NIVELES) - presentes}"


def test_toda_plantilla_declara_formula():
    """Sin 'formula' la respuesta no puede derivarse del enunciado."""
    sin = [p["id"] for p in COMP.plantillas if not p.get("formula")]
    assert not sin, f"Plantillas sin fórmula: {sin}"


def test_toda_plantilla_tiene_escenario_compatible():
    """Toda plantilla debe tener al menos un escenario con la misma magnitud y campos requeridos."""
    huerfanas = []
    for p in COMP.plantillas:
        compatibles = [
            e for e in COMP.escenarios
            if e.get("modulo_id") == p["modulo_id"] and e.get("magnitud") == p["magnitud"]
            and all(req in e and e[req] for req in p.get("campos_requeridos", []))
        ]
        if not compatibles:
            huerfanas.append((p["id"], p["magnitud"]))
    assert not huerfanas, f"Plantillas sin escenario compatible: {huerfanas}"


# ── Coherencia enunciado ↔ respuesta ─────────────────────────────────────────

def test_respuesta_deriva_de_la_formula_del_enunciado():
    """La respuesta publicada debe derivar exactamente de evaluar la fórmula con los mismos valores."""
    for m, n, c in _componer_todo(fams=4, vars_=2):
        esperado = COMP._evaluar_formula(
            {"id": c["plantilla_id"], "formula": c["formula"]},
            c["valores"]
        )
        assert abs(esperado - c["resultado_num"]) < 0.01, (
            f"M{m}N{n} {c['plantilla_id']}: la fórmula {c['formula']} da {esperado} "
            f"pero se publicó {c['resultado_num']}"
        )


def test_formula_solo_usa_nombres_permitidos():
    for p in COMP.plantillas:
        usados = set(re.findall(r"[A-Za-z_]+", p["formula"]))
        assert usados <= COMP._NOMBRES_FORMULA, (
            f"{p['id']} usa nombres no permitidos: {usados - COMP._NOMBRES_FORMULA}"
        )


def test_sin_marcos_que_oculten_variables_de_formula():
    """Regresión bug crítico: toda variante narrativa debe dar al alumno suficiente
    información impresa (variables crudas y/o auxiliares narrativos) para reconstruir
    el resultado de la fórmula. No puede haber ningún dato NECESARIO que no aparezca
    en el texto de ninguna forma."""
    alertas = []
    for p in COMP.plantillas:
        arbol = ast.parse(p["formula"], mode="eval").body
        alt_list = p.get("marcos_alternativos") or []
        for f in alt_list:
            impresos = set(re.findall(r"\{([a-zA-Z_0-9]+)\}", f))
            if not _cubierto(arbol, impresos):
                alertas.append(f"{p['id']} (formula={p['formula']!r}): marco {f!r} no da suficiente información")
    assert not alertas, f"Variantes narrativas que ocultan variables de fórmula:\n" + "\n".join(alertas)


# ── Presentación ─────────────────────────────────────────────────────────────

def test_enunciados_sin_placeholders_ni_defectos_gramaticales():
    for m, n, c in _componer_todo(fams=4, vars_=2):
        e = c["enunciado"]
        assert "{" not in e and "}" not in e, f"M{m}N{n}: placeholder crudo en {e!r}"
        assert " de el " not in e and " a el " not in e, f"M{m}N{n}: falta contracción en {e!r}"
        assert not e[:1].islower(), f"M{m}N{n}: minúscula inicial en {e!r}"


def test_presupuesto_de_caracteres():
    for m, n, c in _componer_todo(fams=4, vars_=2):
        assert len(c["enunciado"]) <= 350, f"M{m}N{n}: {len(c['enunciado'])} caracteres supera límite 350"


# ── Variedad estructural ─────────────────────────────────────────────────────

def test_variedad_estructural_por_nivel():
    por_id = {p["id"]: p for p in COMP.plantillas}
    for m, n in NIVELES:
        pool = [COMP.componer_pregunta_practica(m, n, f, v, 9000 + f * 4 + v)
                for f in range(6) for v in range(2)]
        firmas = {(por_id[c["plantilla_id"]]["operacion_correcta"],
                   por_id[c["plantilla_id"]]["incognita"],
                   len(por_id[c["plantilla_id"]].get("campos_requeridos", [])))
                  for c in pool}
        assert len(firmas) >= 2, f"M{m}N{n}: solo {len(firmas)} firmas estructurales"


def test_determinismo():
    a = COMP.componer_pregunta_practica(3, 2, 2, 1, 4242)
    b = COMP.componer_pregunta_practica(3, 2, 2, 1, 4242)
    assert a == b


def test_r2_rechaza_magnitudes_incompatibles():
    p = next(p for p in COMP.plantillas if p["magnitud"] == "fraccion_visual")
    e = next((e for e in COMP.escenarios if e["magnitud"] != "fraccion_visual"), None)
    if e is None:
        pytest.skip("todos los escenarios son de fraccion_visual")
    with pytest.raises(ValueError, match="R2"):
        COMP.validar_composicion(p, e)
