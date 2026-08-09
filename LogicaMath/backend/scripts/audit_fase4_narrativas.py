"""
Auditoría de coherencia narrativa de la Fase 4.

Genera una muestra grande de preguntas reales con CompositorFase4 (sin tocar
la base de datos) y detecta patrones de incoherencia detectados durante la
corrección de raíz de agosto 2026:

  1. Marcos sin ningún dato numérico (a/b/c/total/n_cant) -> pregunta imposible.
  2. `pregunta` con un sustantivo fijo que no aparece en los marcos_alternativos
     de la misma plantilla -> la pregunta puede hablar de un objeto distinto
     al de la historia.
  3. Envases duplicados ("paquete del saco de X").
  4. Palabra repetida consecutiva.
  5. Unidad de origen incoherente en Módulo 4 (p.ej. "mide 3 cm, ¿a cuántos
     cm equivale?") -- solo aplica a fórmulas de un solo token físico.
  6. Marco que OCULTA una variable que la fórmula necesita (el más grave de
     todos: produce una respuesta "correcta" que no se deduce del enunciado
     mostrado -- bug real reportado por un alumno en agosto 2026, ver
     screenshot "necesita 3 piezas... cada pieza mide 2,4 cm" con una "Medida
     unitaria" fantasma de 1,5 cm que nunca aparecía en el texto).

Uso:
    python scripts/audit_fase4_narrativas.py [--muestras N]

Sale con código 1 si encuentra alguna alerta (útil para CI / pre-commit).
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, ".")
from app.fase4.compositor_fase4 import CompositorFase4  # noqa: E402

OBJECT_VARS = {"objeto_medible", "objetos_0", "objetos_1", "sujeto_medible", "atributo"}
NUM_VARS = {"a", "b", "c", "total", "n_cant"}
CONTAINERS = (
    "saco", "sacos", "bolsa", "bolsas", "paquete", "paquetes", "caja", "cajas",
    "rollo", "rollos", "cesta", "cestas", "balde", "baldes", "fardo", "fardos",
    "lata", "latas", "frasco", "frascos", "bobina", "bobinas", "costal",
    "costales", "bidón", "bidones", "tambor", "tambores",
)


def _vars_in(txt):
    return set(re.findall(r"\{([a-zA-Z_0-9]+)\}", txt))


def _tokens_de_formula(formula):
    return set(t for t in re.findall(r"[A-Za-z_]+", formula) if t in NUM_VARS)


def check_static(plantillas):
    """Chequeos que no requieren generar preguntas: sobre las plantillas tal
    cual están en plantillas_fase4.json."""
    alertas = []

    for p in plantillas:
        alt_list = p.get("marcos_alternativos") or []

        sin_datos = [f for f in alt_list if not (_vars_in(f) & NUM_VARS)]
        if sin_datos:
            alertas.append(
                f"[sin_datos] {p['id']}: {len(sin_datos)}/{len(alt_list)} marcos_alternativos "
                f"sin ningún dato numérico (a/b/c/total/n_cant)"
            )

        preg_obj_vars = _vars_in(p.get("pregunta", "")) & OBJECT_VARS
        alt_obj_vars = set()
        for f in alt_list:
            alt_obj_vars |= (_vars_in(f) & OBJECT_VARS)
        if preg_obj_vars and alt_obj_vars and not (preg_obj_vars & alt_obj_vars):
            alertas.append(
                f"[var_cruzada] {p['id']}: pregunta usa {sorted(preg_obj_vars)} pero "
                f"marcos_alternativos usa {sorted(alt_obj_vars)}"
            )

        # El más grave: el marco tiene que mostrar TODAS las variables que la
        # fórmula usa para calcular la respuesta. Si oculta una, el alumno no
        # puede deducir la respuesta "correcta" a partir de lo que lee (bug
        # real: "necesita 3 piezas... cada pieza mide 2,4 cm" pero el sistema
        # evaluaba a*b con una "b" que nunca aparecía en el enunciado).
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


def check_generated(compositor, n_por_combo=40, n_variantes=3):
    """Chequeos que requieren texto ya compuesto (sustitución real de
    escenarios): contenedores duplicados, palabra repetida, unidad de origen
    incoherente en Módulo 4."""
    alertas = []
    combos = sorted(set((p["modulo_id"], p["nivel_id"]) for p in compositor.plantillas))

    vistos = set()
    unidad_por_plantilla = defaultdict(Counter)

    for modulo_id, nivel_id in combos:
        for fam_idx in range(n_por_combo):
            for var_idx in range(n_variantes):
                seed_val = modulo_id * 100000 + nivel_id * 10000 + fam_idx * 100 + var_idx
                try:
                    q = compositor.componer_pregunta_practica(modulo_id, nivel_id, fam_idx, var_idx, seed_val)
                except Exception as exc:
                    alertas.append(f"[excepcion] modulo={modulo_id} nivel={nivel_id} fam={fam_idx} var={var_idx}: {exc}")
                    continue

                txt = q["enunciado"]
                low = txt.lower()
                unidad_por_plantilla[q["plantilla_id"]][q["unidad"]] += 1

                if txt in vistos:
                    continue
                vistos.add(txt)

                # Captura también los números como su propio token: si no,
                # "R$ 1,4, R$ 0,97 y R$ 0,58" deja tres "r" (de "R$") como si
                # fueran adyacentes al filtrar los números entre medio ->
                # falso positivo de "palabra repetida".
                words = re.findall(r"[a-záéíóúñ]+|\d[\d.,]*", low)
                for i in range(len(words) - 1):
                    if words[i] == words[i + 1]:
                        alertas.append(f"[palabra_repetida] {q['plantilla_id']}: {txt}")
                        break

                positions = [i for i, w in enumerate(words) if w in CONTAINERS]
                for idx in range(len(positions) - 1):
                    if positions[idx + 1] - positions[idx] <= 3:
                        alertas.append(f"[envase_duplicado] {q['plantilla_id']}: {txt}")
                        break

    # Unidad de origen incoherente en Módulo 4: para fórmulas de un solo token
    # físico, TODAS las muestras deberían compartir la misma unidad (la que
    # exige _unidad_origen_requerida). Si aparece más de una, hay mezcla.
    for p in compositor.plantillas:
        if p.get("modulo_id") != 4:
            continue
        tokens = [t for t in compositor._tokens_formula(p) if t != "n_cant"]
        if len(tokens) != 1:
            continue
        conteo = unidad_por_plantilla.get(p["id"])
        if conteo and len(conteo) > 1:
            alertas.append(f"[unidad_mixta] {p['id']}: unidades observadas {dict(conteo)} (debería ser una sola)")

    return alertas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--muestras", type=int, default=40, help="fam_idx por combo módulo/nivel (default 40)")
    args = parser.parse_args()

    compositor = CompositorFase4()

    alertas = []
    alertas += check_static(compositor.plantillas)
    alertas += check_generated(compositor, n_por_combo=args.muestras)

    # verificar_pool_nivel: variedad y concentración por módulo/nivel, usando
    # el mismo mecanismo de rotación que usa seed.py.
    combos = sorted(set((p["modulo_id"], p["nivel_id"]) for p in compositor.plantillas))
    for modulo_id, nivel_id in combos:
        pool = []
        for fam_idx in range(40):
            for var_idx in range(3):
                seed_val = modulo_id * 100000 + nivel_id * 10000 + fam_idx * 100 + var_idx
                try:
                    pool.append(compositor.componer_pregunta_practica(modulo_id, nivel_id, fam_idx, var_idx, seed_val))
                except Exception:
                    continue
        try:
            compositor.verificar_pool_nivel(pool, modulo_id, nivel_id)
        except ValueError as exc:
            alertas.append(f"[pool_nivel] modulo={modulo_id} nivel={nivel_id}: {exc}")

    if alertas:
        print(f"{len(alertas)} ALERTA(S):\n")
        for a in alertas:
            print(" -", a)
        sys.exit(1)

    print("Sin alertas: 0 marcos sin datos, 0 sustantivos cruzados, 0 envases duplicados, "
          "0 palabras repetidas, 0 unidades mixtas, pools OK.")


if __name__ == "__main__":
    main()
