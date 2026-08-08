"""Invariantes de contenido de la Fase 4 (Operatoria Decimal y Conversiones).

Este archivo probaba el vocabulario de la ANTIGUA Fase 4 (fracciones: OBJETOS_FRACC,
BEBIDAS, PINTURAS) y tras el intercambio de fases quedó importando símbolos
inexistentes, lo que rompía la colección de TODA la suite. Además recorría el nivel
(3, 4), que ya no existe. Ahora cubre la Fase 4 vigente, con un test de regresión
por cada defecto detectado en la auditoría:

  - enunciado y respuesta derivados de la MISMA fórmula y los MISMOS números
  - toda plantilla con al menos un escenario compatible (R1 + R2 + escala)
  - pureza de magnitud C6.5: sin volumen ni superficie
  - coma decimal, sin placeholders crudos, sin "de el"
  - variedad estructural real (firmas, no reformulaciones)
"""

import json
import re
import pytest

from app.fase4.compositor_fase4 import CompositorFase4

COMP = CompositorFase4()
NIVELES = [(m, n) for m in range(1, 5) for n in range(1, 4)]


def _componer_todo(fams=12, vars_=4):
    for m, n in NIVELES:
        for f in range(fams):
            for v in range(vars_):
                yield m, n, COMP.componer_pregunta_practica(m, n, f, v, 9000 + f * 4 + v)


# ── Catálogos ────────────────────────────────────────────────────────────────

def test_plantillas_cubren_los_12_niveles():
    presentes = {(p["modulo_id"], p["nivel_id"]) for p in COMP.plantillas}
    assert presentes == set(NIVELES), f"Niveles sin plantillas: {set(NIVELES) - presentes}"


def test_toda_plantilla_declara_formula():
    """Sin 'formula' la respuesta no puede derivarse del enunciado."""
    sin = [p["id"] for p in COMP.plantillas if not p.get("formula")]
    assert not sin, f"Plantillas sin fórmula: {sin}"


def test_toda_plantilla_tiene_escenario_compatible():
    """Regresión: 4 plantillas declaraban magnitudes sin ningún escenario disponible."""
    huerfanas = []
    for p in COMP.plantillas:
        unidad_origen = COMP._unidad_origen_requerida(p)
        compatibles = [
            e for e in COMP.escenarios
            if e["modulo_id"] == p["modulo_id"] and e["magnitud"] == p["magnitud"]
            and all(req in e and e[req] for req in p.get("campos_requeridos", []))
            and (unidad_origen is None or e.get("unidad") == unidad_origen)
        ]
        if not compatibles:
            huerfanas.append((p["id"], p["magnitud"], unidad_origen))
    assert not huerfanas, f"Plantillas sin escenario compatible: {huerfanas}"


def test_escenarios_modulo4_declaran_escala():
    """La magnitud 'longitud' abarca el grosor de una moneda y una maratón: hace
    falta la escala para que un marco en km no caiga en un escenario de espesor."""
    sin = [e["id"] for e in COMP.escenarios
           if e["modulo_id"] == 4 and e.get("escala") not in ("micro", "objeto", "distancia")]
    assert not sin, f"Escenarios del módulo 4 sin escala válida: {sin}"


# ── Coherencia enunciado ↔ respuesta ─────────────────────────────────────────

def test_respuesta_deriva_de_la_formula_del_enunciado():
    """Regresión del defecto crítico: la respuesta era siempre a+b+c mientras el
    enunciado venía de otra plantilla, así que NINGUNA pregunta era correcta."""
    for m, n, c in _componer_todo(fams=6, vars_=2):
        esperado = COMP._evaluar_formula({"id": c["plantilla_id"], "formula": c["formula"]},
                                         c["valores"])
        assert abs(esperado - c["resultado_num"]) < 0.005, (
            f"M{m}N{n} {c['plantilla_id']}: la fórmula {c['formula']} da {esperado} "
            f"pero se publicó {c['resultado_num']}")


def test_formula_solo_usa_nombres_permitidos():
    for p in COMP.plantillas:
        usados = set(re.findall(r"[A-Za-z_]+", p["formula"]))
        assert usados <= COMP._NOMBRES_FORMULA, (
            f"{p['id']} usa nombres no permitidos: {usados - COMP._NOMBRES_FORMULA}")


# ── Presentación ─────────────────────────────────────────────────────────────

def test_enunciados_sin_placeholders_ni_defectos_gramaticales():
    """Regresión: solo se formateaba 'marco', así que 'pregunta' mostraba
    "{unidad}" crudo; y los escenarios traen artículo, produciendo "de el libro"."""
    for m, n, c in _componer_todo(fams=12, vars_=4):
        e = c["enunciado"]
        assert "{" not in e and "}" not in e, f"M{m}N{n}: placeholder crudo en {e!r}"
        assert " de el " not in e and " a el " not in e, f"M{m}N{n}: falta contracción en {e!r}"
        assert not e[:1].islower(), f"M{m}N{n}: minúscula inicial en {e!r}"
        assert not re.search(r"\d\.\d", e), f"M{m}N{n}: punto decimal en {e!r}"


def test_presupuesto_de_caracteres():
    for m, n, c in _componer_todo(fams=12, vars_=4):
        assert len(c["enunciado"]) <= 250, f"M{m}N{n}: {len(c['enunciado'])} caracteres"


# ── C6.5: pureza de magnitud ─────────────────────────────────────────────────

PROHIBIDO_C65 = ("litro", "mililitro", "dm³", "m³", "m²", "dm²", "cm²",
                 "volumen", "superficie", "botella")


def test_sin_volumen_ni_superficie():
    """El volumen pasó a geometría 3D y la superficie a geometría plana."""
    for m, n, c in _componer_todo(fams=12, vars_=4):
        bajo = c["enunciado"].lower()
        hallados = [t for t in PROHIBIDO_C65 if t in bajo]
        assert not hallados, f"M{m}N{n}: magnitud ajena a la Fase 4 {hallados} en {c['enunciado']!r}"


# Volumen y superficie: 0 filas en escenarios_fase4.json para CUALQUIER módulo
# (confirmado contra el catálogo real) — nunca están en alcance de la Fase 4.
# Masa SÍ está en alcance para los módulos 1-3 (5, 3 y 5 escenarios reales
# respectivamente): no se prohíbe ahí. Solo el Módulo 4 (escalera métrica) es
# puro-longitud (20/20 escenarios), así que ahí sí se prohíbe masa/dinero.
_MAGNITUD_PROHIBIDA_GLOBAL_RE = re.compile(
    r"\bmL\b|mililitro|litro|volumen|superficie|\bárea\b|\bm2\b|m²|\bcm2\b|cm²|\bdm2\b|dm²|\bbotella",
    re.IGNORECASE,
)
_MAGNITUD_PROHIBIDA_MODULO4_RE = re.compile(
    r"\bkg\b|kilogramo|gramo|\bharina\b|\bmasa\b|\bpeso\b",
    re.IGNORECASE,
)


def test_teoria_sin_magnitudes_ajenas_a_fase4():
    """Regresión: la teoría del Módulo 4 mezclaba longitud con "kg → g" y
    "L → mL" en la misma frase (el Módulo 4 es puro-longitud), y el Módulo 3
    usaba "botellas" como ejemplo de redondeo por contexto (evoca volumen,
    que no existe en ningún módulo del catálogo real)."""
    from app.fase4.theory_data import FASE4_TEORIA_DATA

    for t in FASE4_TEORIA_DATA:
        texto = json.dumps(t, ensure_ascii=False)
        hallados = _MAGNITUD_PROHIBIDA_GLOBAL_RE.findall(texto)
        assert not hallados, f"M{t['modulo_id']}N{t['nivel_id']}: {hallados} en la teoría"
        if t["modulo_id"] == 4:
            hallados_m4 = _MAGNITUD_PROHIBIDA_MODULO4_RE.findall(texto)
            assert not hallados_m4, f"M4N{t['nivel_id']}: {hallados_m4} (Módulo 4 es puro-longitud)"


def test_ejemplos_guiados_sin_magnitudes_ajenas_a_fase4():
    """Regresión: ejemplos guiados de práctica calculaban área (m²) y volumen
    (L), magnitudes que no existen en ningún módulo del catálogo real
    (escenarios_fase4.json). Masa SÍ es válida en los módulos 1-3: no se
    prohíbe ahí, solo en el Módulo 4 (puro-longitud)."""
    from app.fase4.theory_examples import obtener_ejemplos_expandidos_fase4

    for m, n in NIVELES:
        for i, eg in enumerate(obtener_ejemplos_expandidos_fase4(m, n)):
            texto = json.dumps(eg, ensure_ascii=False)
            hallados = _MAGNITUD_PROHIBIDA_GLOBAL_RE.findall(texto)
            assert not hallados, f"M{m}N{n} ejemplo[{i}]: {hallados}"
            if m == 4:
                hallados_m4 = _MAGNITUD_PROHIBIDA_MODULO4_RE.findall(texto)
                assert not hallados_m4, f"M4N{n} ejemplo[{i}]: {hallados_m4} (Módulo 4 es puro-longitud)"


def test_sin_vocabulario_de_fracciones():
    for m, n, c in _componer_todo(fams=12, vars_=4):
        bajo = c["enunciado"].lower()
        for t in ("fracción", "fracciones", "numerador", "denominador"):
            assert t not in bajo, f"M{m}N{n}: '{t}' pertenece a la Fase 5"


# ── Variedad estructural ─────────────────────────────────────────────────────

def test_variedad_estructural_por_nivel():
    """Firma = (operación, incógnita, nº de campos). Seis reformulaciones de una
    misma estructura satisfacían el conteo de esquemas sin dar variedad real."""
    por_id = {p["id"]: p for p in COMP.plantillas}
    for m, n in NIVELES:
        pool = [COMP.componer_pregunta_practica(m, n, f, v, 9000 + f * 4 + v)
                for f in range(12) for v in range(4)]
        firmas = {(por_id[c["plantilla_id"]]["operacion_correcta"],
                   por_id[c["plantilla_id"]]["incognita"],
                   len(por_id[c["plantilla_id"]].get("campos_requeridos", [])))
                  for c in pool}
        assert len(firmas) >= 3, f"M{m}N{n}: solo {len(firmas)} firmas estructurales"


def test_determinismo():
    """La misma semilla debe dar la misma pregunta: la siembra es reproducible."""
    a = COMP.componer_pregunta_practica(3, 2, 4, 1, 4242)
    b = COMP.componer_pregunta_practica(3, 2, 4, 1, 4242)
    assert a == b


def test_r2_rechaza_magnitudes_incompatibles():
    """'No puedes sumar peras con manzanas': el contrato debe fallar, no adaptar."""
    p = next(p for p in COMP.plantillas if p["magnitud"] == "longitud")
    e = next((e for e in COMP.escenarios if e["magnitud"] != "longitud"), None)
    if e is None:
        pytest.skip("todos los escenarios son de longitud")
    with pytest.raises(ValueError, match="R2"):
        COMP.validar_composicion(p, e)
