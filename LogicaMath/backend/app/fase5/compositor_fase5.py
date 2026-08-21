"""
Motor Compositor con Validación para la Fase 5 (LogicaMath)
Fracciones, Porcentajes y Proporciones
Cumple con la norma de validación de contenido generado de deep_analise_pro §25.4.
"""

import ast
import json
import operator
import os
import random
import re
from typing import Dict, Any, List

from app.models.enums import TipoErrorEnum

# Valores admitidos por la columna Alternativa.tipo_error (Enum). Cualquier
# etiqueta fuera de este conjunto se guarda cruda en la BD y luego revienta
# al LEER la fila por ORM (LookupError), tumbando /responder con un 500 en
# cada respuesta incorrecta. Por eso el compositor coerciona SIEMPRE a un
# miembro válido, incluso si confusiones_fase5.json es editado a mano.
_TIPOS_ERROR_VALIDOS = {e.value for e in TipoErrorEnum}


def _coerce_tipo_error(raw: str | None) -> str:
    """Devuelve un miembro válido de TipoErrorEnum; 'calculo' como respaldo."""
    if raw and raw in _TIPOS_ERROR_VALIDOS:
        return raw
    return "calculo"


class CompositorFase5:
    _NOMBRES_FORMULA = {"a", "b", "c", "total", "n_cant", "parte"}

    # Plantillas cuya fórmula es una RESTA de dos cantidades compuestas
    # (p.ej. "tomados menos restantes", "componente B menos componente A").
    # _generar_valores debe garantizar, para cada una, que el minuendo sea
    # siempre >= al sustraendo: si no se restringe el rango de valores, la
    # resta puede dar negativo (una "diferencia" negativa no tiene sentido
    # para un niño) y --caso real detectado-- alimentar un valor negativo a
    # _generar_distractores podía colgar el generador en un bucle infinito.
    _PLANTILLAS_RESTA_ORDENADA = {
        "tpl_m1_n1_diferencia",
        "tpl_m1_n3_resto_menos_usadas",
        "tpl_m2_n2_diferencia_tomados_resto",
        "tpl_m3_n2_diferencia_precio_ahorro",
        "tpl_m4_n1_diferencia_componentes",
        "tpl_m4_n2_diferencia_a_b",
        "tpl_m4_n3_diferencia_pct",
    }

    _OPERADORES_PERMITIDOS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    # Símbolos legibles para narrar el procedimiento paso a paso (E4).
    _OP_SIMBOLO = {
        ast.Add: "+",
        ast.Sub: "−",
        ast.Mult: "×",
        ast.Div: "÷",
        ast.FloorDiv: "÷",
        ast.Mod: "resto de",
        ast.Pow: "elevado a",
    }

    def __init__(self, data_dir: str | None = None):
        if not data_dir:
            data_dir = os.path.join(os.path.dirname(__file__), "data")

        with open(os.path.join(data_dir, "escenarios_fase5.json"), "r", encoding="utf-8") as f:
            self.escenarios = json.load(f)
        with open(os.path.join(data_dir, "plantillas_fase5.json"), "r", encoding="utf-8") as f:
            self.plantillas = json.load(f)
        with open(os.path.join(data_dir, "confusiones_fase5.json"), "r", encoding="utf-8") as f:
            self.confusiones = json.load(f)
        with open(os.path.join(data_dir, "nombres_fase5.json"), "r", encoding="utf-8") as f:
            self.nombres = json.load(f)

    def validar_composicion(
        self,
        plantilla: dict,
        escenario: dict,
        texto_enunciado: str | None = None,
        opciones: list[str] | None = None
    ) -> bool:
        # R2 check: Magnitude contract
        if plantilla.get("magnitud") != escenario.get("magnitud"):
            raise ValueError(
                f"R2 violada: plantilla '{plantilla['id']}' es de {plantilla.get('magnitud')} "
                f"y escenario '{escenario['id']}' es de {escenario.get('magnitud')}"
            )

        # R1 check: Required grammatical fields
        campos_req = plantilla.get("campos_requeridos", [])
        for campo in campos_req:
            if campo not in escenario or not escenario[campo]:
                raise ValueError(
                    f"R1 violada: escenario '{escenario['id']}' carece del campo requerido '{campo}' "
                    f"exigido por la plantilla '{plantilla['id']}'"
                )

        # Character budget checks: Enunciado <= 350 chars, Opciones <= 60 chars
        if texto_enunciado and len(texto_enunciado) > 350:
            raise ValueError(f"Presupuesto superado: enunciado tiene {len(texto_enunciado)} caracteres (máximo 350)")

        if opciones:
            for op in opciones:
                if len(str(op)) > 60:
                    raise ValueError(f"Presupuesto superado: opción '{op}' tiene {len(str(op))} caracteres (máximo 60)")

        return True

    def _eval_ast(self, node: ast.AST, variables: dict) -> float:
        """Evalúa un nodo AST restringido a aritmética pura sobre `variables`.

        Sustituye a eval() sobre una cadena que viene de plantillas_fase5.json:
        un JSON editable por un admin no debe poder ejecutar código arbitrario
        (import, atributos, llamadas...). Solo se permiten números, nombres
        declarados en `variables` y los operadores aritméticos de
        _OPERADORES_PERMITIDOS.
        """
        if isinstance(node, ast.Expression):
            return self._eval_ast(node.body, variables)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Name):
            if node.id not in variables:
                raise ValueError(f"Variable no permitida en fórmula: {node.id!r}")
            return variables[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in self._OPERADORES_PERMITIDOS:
            izq = self._eval_ast(node.left, variables)
            der = self._eval_ast(node.right, variables)
            return self._OPERADORES_PERMITIDOS[type(node.op)](izq, der)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._OPERADORES_PERMITIDOS:
            return self._OPERADORES_PERMITIDOS[type(node.op)](self._eval_ast(node.operand, variables))
        raise ValueError(f"Nodo no permitido en fórmula: {ast.dump(node)}")

    def _evaluar_formula(self, plantilla: dict, valores: dict) -> float:
        formula = plantilla["formula"]
        local_vars = {k: float(v) for k, v in valores.items() if k in self._NOMBRES_FORMULA}

        try:
            arbol = ast.parse(formula, mode="eval")
            res = self._eval_ast(arbol, local_vars)
            return round(float(res), 2)
        except Exception as exc:
            raise ValueError(f"Error evaluando fórmula {formula!r} con valores {valores}: {exc}") from exc

    @staticmethod
    def _fmt_num(x: float) -> str:
        return str(int(x)) if float(x).is_integer() else str(round(float(x), 2)).replace(".", ",")

    def _narrar_nodo(self, node: ast.AST, variables: dict, pasos: list) -> float:
        """Recorre el AST en post-orden evaluando con los valores reales y va
        acumulando en `pasos` cada operación como texto legible ("20 ÷ 4 = 5").
        Es la base de la explicación paso a paso (E4): en vez de imprimir la
        fórmula cruda, muestra la aritmética concreta que resuelve la pregunta.
        """
        if isinstance(node, ast.Expression):
            return self._narrar_nodo(node.body, variables, pasos)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name):
            return float(variables[node.id])
        if isinstance(node, ast.BinOp) and type(node.op) in self._OPERADORES_PERMITIDOS:
            izq = self._narrar_nodo(node.left, variables, pasos)
            der = self._narrar_nodo(node.right, variables, pasos)
            val = self._OPERADORES_PERMITIDOS[type(node.op)](izq, der)
            simbolo = self._OP_SIMBOLO.get(type(node.op), "?")
            pasos.append(f"{self._fmt_num(izq)} {simbolo} {self._fmt_num(der)} = {self._fmt_num(val)}")
            return val
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._OPERADORES_PERMITIDOS:
            return self._OPERADORES_PERMITIDOS[type(node.op)](self._narrar_nodo(node.operand, variables, pasos))
        raise ValueError(f"Nodo no permitido al narrar: {ast.dump(node)}")

    def _visual_payload(self, modulo_id: int, nivel_id: int, valores: dict) -> dict:
        """E2: figura por módulo (tipo_visual + datos que espera el visualizador
        del frontend). Muestra el PLANTEO (contexto) sin revelar la respuesta;
        el alumno razona sobre la figura.
          M1 → pizza (fracción a/b); M1N2 → pizza de equivalencias (base/factor)
          M2 → pizza (fracción del grupo)
          M3N1/N2 → percentage_beaker; M3N3 → bar_chart (promedio)
          M4 → ratio_grid (razón a:b)
        """
        a = int(valores.get("a", 0))
        b = int(valores.get("b", 0))
        c = int(valores.get("c", 0))
        total = int(valores.get("total", 0))

        if modulo_id == 1:
            if nivel_id == 2 and c > 0:
                return {"tipo_visual": "pizza", "num_base": a, "den_base": b, "factor": c}
            cortes = b if b > 0 else 8
            return {"tipo_visual": "pizza", "cortes": cortes,
                    "sombreados": list(range(min(max(a, 0), cortes)))}
        if modulo_id == 2:
            cortes = b if b > 0 else 4
            return {"tipo_visual": "pizza", "cortes": cortes,
                    "sombreados": list(range(min(max(a, 0), cortes)))}
        if modulo_id == 3:
            if nivel_id == 3:
                return {"tipo_visual": "bar_chart", "val_a": a, "val_b": b,
                        "categorias": ["Nota 1", "Nota 2"]}
            return {"tipo_visual": "percentage_beaker", "total": total if total > 0 else 100}
        if modulo_id == 4:
            return {"tipo_visual": "ratio_grid", "val_a": a, "val_b": b}
        return {}

    def _explicar_pasos(self, plantilla: dict, valores: dict, resultado_num: float) -> list[dict]:
        """Devuelve la explicación como lista de pasos [{orden, texto}] en
        lenguaje concreto (aritmética real), no la fórmula interna."""
        local_vars = {k: float(v) for k, v in valores.items() if k in self._NOMBRES_FORMULA}
        pasos_txt: list[str] = []
        try:
            arbol = ast.parse(plantilla["formula"], mode="eval")
            self._narrar_nodo(arbol, local_vars, pasos_txt)
        except Exception:
            pasos_txt = []
        pasos = [{"orden": 1, "texto": "Resolvámoslo paso a paso:"}]
        for t in pasos_txt:
            pasos.append({"orden": len(pasos) + 1, "texto": t})
        pasos.append({"orden": len(pasos) + 1, "texto": f"Por eso, la respuesta correcta es {self._fmt_num(resultado_num)}."})
        return pasos

    # Vocabulario contable cerrado (sustantivos hardcodeados en las plantillas
    # más las unidades de los escenarios). Verificado real: sin concordancia,
    # el compositor produce "3 taza", "4 gramo base" o "1 partes" -- el mismo
    # defecto gramatical detectado y corregido en la Fase 4.
    _SINGULAR_A_PLURAL = {
        "parte": "partes", "porción": "porciones", "celda": "celdas",
        "caja": "cajas", "división": "divisiones", "grupo": "grupos",
        "lote": "lotes", "caramelo": "caramelos", "moneda": "monedas",
        "estudiante": "estudiantes", "libro": "libros", "canica": "canicas",
        "manzana": "manzanas", "cristal": "cristales", "franja": "franjas",
        "parcela": "parcelas", "taza": "tazas", "litro": "litros",
        "gramo": "gramos", "vaso": "vasos", "cuadrado": "cuadrados",
        "rebanada": "rebanadas",
        # Contenedores y objetos mod2/mod3 que aparecen tras "los/las" o cifras:
        "bolsa": "bolsas", "equipo": "equipos", "estante": "estantes",
        "alcancía": "alcancías", "canasta": "canastas", "artículo": "artículos",
        "dispositivo": "dispositivos", "cuenta": "cuentas", "archivo": "archivos",
    }

    def _normalizar_texto(self, texto: str) -> str:
        """Corrige defectos gramaticales mecánicos del texto ya ensamblado.

        1) Contrae "de el" -> "del" (el escenario del pastel usa artículo
           "el", y algunos marcos anteponen "de" de forma fija: "de el
           pastel" sin contraer).
        2) Concuerda en número los sustantivos contables cuando el marco los
           imprime pegados a la cantidad ("3 taza" -> "3 tazas", "1 partes"
           -> "1 parte"). Opera sobre singular Y plural porque el marco puede
           traer cualquiera de las dos formas (las unidades de escenario se
           guardan en singular; varios sustantivos de plantilla, en plural).
        """
        texto = re.sub(r"\bde el\b", "del", texto)
        texto = re.sub(r"\ba el\b", "al", texto)

        # Concordancia de artículo con el número 1: un marco fija el artículo en
        # plural ("las {a} partes tomadas") y, cuando a=1, la concordancia de
        # sustantivo de abajo produce "las 1 parte" (artículo plural + singular).
        # Se corrige el artículo a singular. Verificado real: 4 enunciados.
        _art_sing = {"las": "la", "los": "el", "unas": "una", "unos": "un"}
        texto = re.sub(
            r"\b(las|los|unas|unos)\s+1\b",
            lambda m: f"{_art_sing[m.group(1).lower()]} 1",
            texto,
        )

        formas = {}
        for sing, plur in self._SINGULAR_A_PLURAL.items():
            formas[sing] = (sing, plur)
            formas[plur] = (sing, plur)
        patron = re.compile(
            r"\b(\d+)\s+(" + "|".join(re.escape(f) for f in formas) + r")\b"
        )

        def _concordar(m: re.Match) -> str:
            numero, palabra = m.group(1), m.group(2)
            singular, plural = formas[palabra]
            correcta = singular if numero == "1" else plural
            return f"{numero} {correcta}"

        texto = patron.sub(_concordar, texto)

        # Concordancia número artículo-sustantivo: "los bolsa" → "los bolsas".
        # Un marco imprime "en {articulo} {contenedor}" con articulo="los" para
        # mod2 (concuerda con el OBJETO plural) pero contenedor es singular.
        # Verificado real: 21 preguntas F5 con "los bolsa", "las caja", etc.
        _pluralizables = "|".join(re.escape(s) for s in self._SINGULAR_A_PLURAL)
        texto = re.sub(
            r"\b(los|las)\s+(" + _pluralizables + r")\b",
            lambda m: f"{m.group(1)} {self._SINGULAR_A_PLURAL[m.group(2)]}",
            texto,
            flags=re.IGNORECASE,
        )
        # Mismo bug con cifras: "los 80 dispositivo" → "los 80 dispositivos"
        texto = re.sub(
            r"\b(los|las)\s+(\d+)\s+(" + _pluralizables + r")\b",
            lambda m: f"{m.group(1)} {m.group(2)} {self._SINGULAR_A_PLURAL[m.group(3)]}",
            texto,
            flags=re.IGNORECASE,
        )

        # Concordancia de género del pronombre interrogativo con el sustantivo:
        # los marcos genéricos escriben "¿Cuántos {sustantivo}...?" pero muchos
        # sustantivos son femeninos (monedas, partes, porciones, ...). Verificado
        # real: 22 preguntas F5 con "¿Cuántos monedas". Corrige a "¿Cuántas".
        _fem = {
            "monedas", "moneda", "partes", "parte", "porciones", "porción",
            "celdas", "celda", "cajas", "caja", "manzanas", "manzana",
            "naranjas", "naranja", "canicas", "canica", "tazas", "taza",
            "franjas", "franja", "parcelas", "parcela", "rebanadas", "rebanada",
            "divisiones", "división", "flores", "flor", "galletas", "galleta",
            "pizzas", "pizza",
        }
        _mas = {
            "caramelos", "caramelo", "libros", "libro", "estudiantes",
            "grupos", "grupo", "lotes", "lote", "vasos", "vaso",
            "cristales", "cristal", "cuadrados", "cuadrado", "gramos",
            "gramo", "litros", "litro",
        }

        def _concordar_pronombre(m: re.Match) -> str:
            pron, susta = m.group(1), m.group(2)
            palabra = susta.lower()
            if palabra in _fem:
                base = "Cuántas" if pron[0] == "C" else "cuántas"
            elif palabra in _mas:
                base = "Cuántos" if pron[0] == "C" else "cuántos"
            else:
                return m.group(0)
            return f"{base} {susta}"

        texto = re.sub(
            r"\b([Cc]uánt[oa]s)\s+([A-Za-zÁÉÍÓÚÑáéíóúñ]+)\b",
            _concordar_pronombre,
            texto,
        )
        return texto

    def _valores_auxiliares(self, valores: dict) -> dict:
        """Cadenas auxiliares que algunos marcos narrativos imprimen (p.ej.
        "la diferencia entre las porciones libres ({b_minus_a}) y las usadas
        ({a})"). Centralizado aquí para poder comprobar, antes de aceptar una
        composición, que el resultado final no coincida con ninguno de estos
        números ya visibles en el texto.
        """
        a_val = int(valores.get("a", 0))
        b_val = int(valores.get("b", 0))
        c_val = int(valores.get("c", 0))
        tot_val = int(valores.get("total", 0))
        return {
            "b_minus_a": str(b_val - a_val),
            "a_times_c": str(a_val * c_val),
            "b_times_c": str(b_val * c_val),
            "total_div_b": str(tot_val // b_val) if b_val > 0 else "0",
            "a_pct": str((a_val * 100) // (a_val + b_val)) if (a_val + b_val) > 0 else "0",
            "b_pct": str((b_val * 100) // (a_val + b_val)) if (a_val + b_val) > 0 else "0",
        }

    def componer_pregunta_practica(
        self,
        modulo_id: int,
        nivel_id: int,
        fam_idx: int,
        var_idx: int,
        seed_val: int
    ) -> dict:
        rng = random.Random(seed_val)
        sujeto_nombre = self.nombres[(fam_idx + var_idx) % len(self.nombres)]

        plantillas_nivel = [p for p in self.plantillas if p["modulo_id"] == modulo_id and p["nivel_id"] == nivel_id]
        if not plantillas_nivel:
            raise ValueError(f"No hay plantillas definidas para módulo {modulo_id}, nivel {nivel_id}")

        plantilla = plantillas_nivel[fam_idx % len(plantillas_nivel)]

        escenarios_compatibles = [
            e for e in self.escenarios
            if e["modulo_id"] == modulo_id and e["magnitud"] == plantilla["magnitud"]
            and all(req in e and e[req] for req in plantilla.get("campos_requeridos", []))
        ]
        if not escenarios_compatibles:
            raise ValueError(f"No hay escenarios compatibles para plantilla {plantilla['id']}")

        escenario = escenarios_compatibles[var_idx % len(escenarios_compatibles)]

        # Pick narrative frame first: los tokens que efectivamente imprime
        # (p.ej. "{b}" o "{b_minus_a}") determinan qué números puede ver el
        # alumno, y solo esos importan para la comprobación de coincidencia
        # de abajo.
        marcos = plantilla.get("marcos_alternativos", [])
        marco_fmt = marcos[var_idx % len(marcos)]
        tokens_impresos = set(re.findall(r"\{(\w+)\}", marco_fmt))
        # Constantes ENTERAS escritas literalmente en el marco (p.ej. "Divide
        # entre 2 ...", "Calcula 4 veces ..."). No son tokens, así que el guard
        # de coincidencia no las veía y la respuesta podía terminar valiendo
        # exactamente ese literal ("Divide entre 2" -> respuesta 2), quedando
        # impresa en el enunciado. Se tratan igual que un número visible.
        _sin_tokens = re.sub(r"\{\w+\}", " ", marco_fmt)
        literales_marco = set(re.findall(r"(?<!\d)\d+(?!\d)", _sin_tokens))

        # Generate numbers according to modulo and level. Cada intento debe
        # cumplir TRES condiciones: resultado entero (o el escenario es de
        # dinero), y la respuesta NO puede coincidir con ningún número que el
        # enunciado va a imprimir literalmente (los valores crudos a/b/c/total
        # o los auxiliares narrativos como "libres" o "el nuevo numerador") --
        # solo entre los que el marco elegido realmente usa. Sin esta última
        # condición un niño podía "adivinar" la respuesta porque ya aparecía
        # copiada en el propio enunciado -- comprobado real en 72/720
        # preguntas (10%), p.ej. promedios de notas muy cercanas entre sí
        # donde el promedio coincide con una de las notas.
        resultado_num = 0.0
        valores = {}
        helpers = {}
        for attempt in range(50):
            valores = self._generar_valores(plantilla, fam_idx, var_idx + attempt, rng)
            resultado_num = self._evaluar_formula(plantilla, valores)
            helpers = self._valores_auxiliares(valores)
            entero_ok = resultado_num.is_integer() or escenario.get("sub_magnitud") == "dinero"
            impresos = {
                str(int(v)) for k, v in valores.items()
                if k in tokens_impresos and float(v).is_integer()
            } | {v for k, v in helpers.items() if k in tokens_impresos} | literales_marco
            sin_coincidencia = str(int(resultado_num)) not in impresos if resultado_num.is_integer() else True
            if entero_ok and sin_coincidencia:
                break

        # Format variables dictionary with precomputed helpers
        fmt_dict = {
            **escenario,
            **{k: str(int(v)) if float(v).is_integer() else str(v) for k, v in valores.items()},
            "sujeto_nombre": sujeto_nombre,
            **helpers,
        }

        enunciado = marco_fmt.format(**fmt_dict)
        enunciado = self._normalizar_texto(enunciado)
        if enunciado:
            enunciado = enunciado[0].upper() + enunciado[1:]

        # Validate composition
        self.validar_composicion(plantilla, escenario, texto_enunciado=enunciado)

        # Format answer string
        if resultado_num.is_integer():
            ans_str = str(int(resultado_num))
        else:
            ans_str = str(resultado_num).replace(".", ",")

        # Distractors with diagnostic metadata
        distractores_meta = self._generar_distractores(resultado_num, modulo_id, rng)
        opciones_meta = [{"texto": ans_str, "es_correcta": True, "tipo_error": None, "feedback_error": None}]
        for d in distractores_meta:
            opciones_meta.append({
                "texto": d["texto"],
                "es_correcta": False,
                "tipo_error": d["tipo_error"],
                "feedback_error": d["feedback_error"]
            })

        rng.shuffle(opciones_meta)
        opciones = [o["texto"] for o in opciones_meta]

        # E4: explicación paso a paso real (aritmética concreta), no la fórmula.
        explicacion_pasos = self._explicar_pasos(plantilla, valores, resultado_num)
        explicacion_texto = " ".join(p["texto"] for p in explicacion_pasos)

        return {
            "plantilla_id": plantilla["id"],
            "escenario_id": escenario["id"],
            "modulo_id": modulo_id,
            "nivel_id": nivel_id,
            "enunciado": enunciado,
            "formula": plantilla["formula"],
            "valores": valores,
            "resultado_num": resultado_num,
            "respuesta_correcta": ans_str,
            "opciones": opciones,
            "opciones_meta": opciones_meta,
            "explicacion_pasos": explicacion_pasos,
            "explicacion": explicacion_texto,
            "datos_numericos": {
                **valores,
                "resultado_num": resultado_num,
                "formula": plantilla["formula"],
                **self._visual_payload(modulo_id, nivel_id, valores),
            }
        }

    def _generar_valores(self, plantilla: dict, fam_idx: int, var_idx: int, rng: random.Random) -> dict:
        modulo_id = plantilla["modulo_id"]
        nivel_id = plantilla["nivel_id"]
        resta_ordenada = plantilla["id"] in self._PLANTILLAS_RESTA_ORDENADA

        if modulo_id == 1:
            if nivel_id == 1:
                b = rng.choice([4, 6, 8, 10, 12])
                # tpl_m1_n1_diferencia calcula (b-a)-a = b-2a y narra "cuántas
                # partes MÁS quedan libres que tomadas": exige b-2a > 0, es
                # decir a < b/2. b siempre es par en este conjunto.
                a = rng.randint(1, b // 2 - 1) if resta_ordenada else rng.randint(1, b - 1)
                return {"a": a, "b": b}
            elif nivel_id == 2:
                a = rng.randint(1, 4)
                b = rng.choice([5, 6, 8])
                c = rng.choice([2, 3, 4])
                return {"a": a, "b": b, "c": c}
            else:  # nivel 3
                b = rng.choice([6, 8, 10, 12])
                # tpl_m1_n3_resto_menos_usadas: misma restricción que arriba
                # -- "¿en cuántas unidades supera el resto a las usadas?"
                # exige b-2a > 0. Bug real: sin esta cota a podía superar b/2
                # y el resultado negativo colgaba _generar_distractores en un
                # bucle infinito.
                a = rng.randint(1, b // 2 - 1) if resta_ordenada else rng.randint(1, b - 2)
                return {"a": a, "b": b}
        elif modulo_id == 2:
            if nivel_id == 1:
                b = rng.choice([2, 3, 4, 5, 10])
                k = rng.randint(4, 12)
                total = b * k
                return {"a": 1, "b": b, "total": total}
            elif nivel_id == 2:
                b = rng.choice([3, 4, 5, 10])
                # tpl_m2_n2_diferencia_tomados_resto: k*(2a-b) exige 2a>b para
                # que "tomados" > "restantes" ESTRICTO. Con 2a==b la diferencia
                # sería 0 y "en cuánto superan" carece de sentido.
                a = rng.randint(b // 2 + 1, b - 1) if resta_ordenada else rng.randint(2, b - 1)
                k = rng.randint(3, 8)
                total = b * k
                return {"a": a, "b": b, "total": total}
            else:  # nivel 3
                b = rng.choice([3, 4, 5, 8])
                a = rng.randint(1, b - 1)
                k = rng.randint(4, 10)
                total = b * k
                return {"a": a, "b": b, "total": total}
        elif modulo_id == 3:
            if nivel_id == 1:
                a = rng.choice([10, 20, 25, 50])
                totals_valid = [t for t in [40, 60, 80, 100, 120, 160, 200] if (a * t) % 100 == 0]
                total = rng.choice(totals_valid)
                return {"a": a, "total": total}
            elif nivel_id == 2:
                # tpl_m3_n2_diferencia_precio_ahorro: (total - t*a/100) - (t*a/100) = total*(1-2a/100)
                # exige a < 50 ESTRICTO (con a==50, precio pagado = ahorro, dif=0).
                opciones_a = [10, 20, 25, 30, 40, 50]
                if resta_ordenada:
                    opciones_a = [x for x in opciones_a if x < 50]
                a = rng.choice(opciones_a)
                totals_valid = [t for t in [40, 50, 60, 80, 100, 120, 150, 200] if (a * t) % 100 == 0]
                total = rng.choice(totals_valid)
                return {"a": a, "total": total}
            else:  # nivel 3: promedios de 3 notas
                a = rng.randint(12, 18)
                b = rng.randint(12, 18)
                c_base = rng.randint(12, 18)
                rem = (a + b + c_base) % 3
                c = c_base + ((3 - rem) if rem != 0 else 0)
                return {"a": a, "b": b, "c": c}
        else:  # modulo_id == 4
            if nivel_id == 1:
                a = rng.choice([1, 2, 3])
                # tpl_m4_n1_diferencia_componentes: c*(b-a) exige b > a ESTRICTO
                # para que "secundarias" SUPEREN a "base". Con b == a la resta
                # da 0 y "por cuántas partes superan" no tiene sentido (bug real
                # detectado en 8 preguntas). Si no hay b>a válido, se usa el
                # mayor b posible como fallback.
                if resta_ordenada:
                    opciones_b = [x for x in (2, 3, 4, 5) if x > a]
                    b = rng.choice(opciones_b) if opciones_b else max(a + 1, 2)
                else:
                    b = rng.choice([2, 3, 4, 5])
                c = rng.choice([2, 3, 4])
                total = a * c
                return {"a": a, "b": b, "c": c, "total": total}
            elif nivel_id == 2:
                a = rng.choice([1, 2, 3])
                # tpl_m4_n2_diferencia_a_b: k*(b-a) exige b > a ESTRICTO.
                if resta_ordenada:
                    opciones_b = [x for x in (2, 3, 4) if x > a]
                    b = rng.choice(opciones_b) if opciones_b else max(a + 1, 2)
                else:
                    b = rng.choice([2, 3, 4])
                k = rng.randint(3, 8)
                n_cant = a + b
                total = n_cant * k
                return {"a": a, "b": b, "n_cant": n_cant, "total": total}
            else:  # nivel 3: mezclas y % de volumen
                target_total = rng.choice([4, 5, 8, 10, 20, 25, 50])
                valid_a = [x for x in range(1, target_total) if (x * 100) % target_total == 0]
                # tpl_m4_n3_diferencia_pct: pct_b - pct_a exige b > a ESTRICTO
                # (a < total/2). Con a == total/2 el % de B iguala al de A y la
                # diferencia es 0 → "resta el % de A al de B" da 0 sin sentido.
                if resta_ordenada:
                    valid_a = [x for x in valid_a if x < target_total - x] or valid_a
                a = rng.choice(valid_a)
                b = target_total - a
                total = target_total
                return {"a": a, "b": b, "total": total}

    def _generar_distractores(self, correcto: float, modulo_id: int, rng: random.Random) -> list[dict]:
        c = int(correcto) if float(correcto).is_integer() else correcto
        magnitud_keys = {1: "fraccion_visual", 2: "fraccion_cantidad", 3: "porcentajes_promedios", 4: "razon_mezclas"}
        mag_key = magnitud_keys.get(modulo_id, "fraccion_visual")
        conf_list = self.confusiones.get(mag_key, [])

        candidates = [c + 1, max(1, c - 1), c * 2, max(1, c // 2), c + 2, c + 3]
        distractores_meta = []
        used_vals = {c}

        for idx, cand in enumerate(candidates):
            if len(distractores_meta) >= 3:
                break
            cand_val = int(cand) if float(cand).is_integer() else cand
            if cand_val not in used_vals and cand_val > 0:
                used_vals.add(cand_val)
                conf = conf_list[idx % len(conf_list)] if conf_list else {}
                distractores_meta.append({
                    "texto": str(cand_val),
                    "tipo_error": _coerce_tipo_error(conf.get("tipo")),
                    "feedback_error": conf.get("explicacion", "Revisa el cálculo realizado.")
                })

        # Relleno de respaldo. El offset SIEMPRE avanza en cada vuelta -- nunca
        # se recalcula a partir de len(distractores_meta) -- porque hacerlo así
        # producía un bucle infinito real: con una respuesta correcta negativa
        # (bug ya corregido en _generar_valores, pero esto queda como defensa
        # adicional), el candidato de relleno podía colisionar siempre con el
        # mismo valor ya usado y `len` nunca avanzaba para cambiarlo.
        offset = 1
        intentos = 0
        while len(distractores_meta) < 3 and intentos < 200:
            fake_val = max(1, int(c) + offset)
            offset += 1
            intentos += 1
            if fake_val in used_vals:
                continue
            used_vals.add(fake_val)
            distractores_meta.append({
                "texto": str(fake_val),
                "tipo_error": "calculo",
                "feedback_error": "Verifica tu procedimiento paso a paso."
            })

        return distractores_meta
