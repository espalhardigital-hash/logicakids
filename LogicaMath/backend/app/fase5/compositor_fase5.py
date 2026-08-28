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

    # Las antiguas operaciones arbitrarias de M1N2 fueron retiradas de la
    # fuente. La lista permanece como guardia de migración si reaparece una
    # plantilla obsoleta en un catálogo externo.
    _PLANTILLAS_PEDAGOGICAMENTE_EXCLUIDAS = {
        "tpl_m1_n2_suma_amplif", "tpl_m1_n2_dif_amplif",
        "tpl_m1_n2_doble_nuevo_num", "tpl_m1_n2_den_cuadruple",
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

    # Guardas de publicación. No corrigen texto a posteriori: hacen fallar la
    # composición para que el defecto se repare en su plantilla o escenario,
    # que son las fuentes de verdad del banco.
    _PATRONES_ENUNCIADO_PROHIBIDOS = (
        (re.compile(r"¿Cuánto es (?:las|los)\b", re.IGNORECASE), "interrogativo sin concordancia"),
        (re.compile(r"\b(?:regala|dona)\b[^?!.]*\bestudiantes\b", re.IGNORECASE), "personas tratadas como objetos"),
        (re.compile(r"\b(?:gasta|gastó|gastado)\b[^?!.]*\bcaramelos\b", re.IGNORECASE), "verbo incompatible con objetos"),
        (re.compile(r"\bencuesta\b[^?!.]*(?:descuento|rebaja|precio|ahorro|comprar)", re.IGNORECASE), "contexto comercial aplicado a una encuesta"),
        (re.compile(r"\b(?:votos|puntos)\b[^?!.]*(?:descuento|rebaja|precio|ahorro|artículos?)", re.IGNORECASE), "unidad no monetaria en un problema comercial"),
        (re.compile(r"\bcuenta de ahorro\b[^?!.]*(?:nota|puntaje|promedio)", re.IGNORECASE), "promedio con contexto monetario incompatible"),
        (re.compile(r"¿Cuál es (?:dos|tres|cuatro)\b", re.IGNORECASE), "interrogativo incompatible con una cantidad plural"),
        (re.compile(r"\b1\s+están\b", re.IGNORECASE), "verbo plural aplicado a una unidad"),
        (re.compile(r"\b1\s+[A-Za-zÁÉÍÓÚÑáéíóúñ]+\s+(?:están|fueron|son)\b", re.IGNORECASE), "verbo plural aplicado a una unidad"),
        (re.compile(r"¿Cuánt[oa]s\s+(?:parte|porción|celda|caja|división|grupo|taza|litro|gramo|vaso|cuadrado|parcela)\b", re.IGNORECASE), "sustantivo singular tras interrogativo plural"),
    )

    # Compatibilidad semántica fina para el catálogo histórico. Se aplica al
    # cargarlo para que todos los consumidores reciban plantillas con contrato
    # explícito, sin depender de la magnitud general del módulo.
    _ESCENARIOS_POR_PLANTILLA = {
        # Fracciones de colecciones: nunca regalar/donar personas.
        "tpl_m2_n3_complemento": ["esc_fc_caramelos", "esc_fc_monedas", "esc_fc_libros", "esc_fc_canicas", "esc_fc_frutas"],
        "tpl_m2_n3_dada": ["esc_fc_caramelos", "esc_fc_monedas", "esc_fc_libros", "esc_fc_canicas", "esc_fc_frutas"],
        "tpl_m2_n3_mitad_complemento": ["esc_fc_monedas", "esc_fc_libros", "esc_fc_canicas", "esc_fc_frutas"],
        # Porcentajes básicos con un referente coherente para cada acción.
        "tpl_m3_n1_porcentaje_directo": ["esc_pp_notas", "esc_pp_votos", "esc_pp_ahorro", "esc_pp_descargas"],
        "tpl_m3_n1_complemento_pct": ["esc_pp_notas", "esc_pp_votos", "esc_pp_descargas"],
        "tpl_m3_n1_monto_restante": ["esc_pp_ahorro"],
        "tpl_m3_n1_doble_porcentaje": ["esc_pp_notas", "esc_pp_votos", "esc_pp_descargas"],
        "tpl_m3_n1_mitad_porcentaje": ["esc_pp_notas", "esc_pp_votos", "esc_pp_descargas"],
        "tpl_m3_n1_suma_monto_total": ["esc_pp_ahorro"],
        # Descuentos/recargos solo usan precios; promedios solo evaluaciones.
        "tpl_m3_n2_descuento_final": ["esc_pp_tienda"],
        "tpl_m3_n2_ahorro": ["esc_pp_tienda"],
        "tpl_m3_n2_dos_productos_descuento": ["esc_pp_tienda"],
        "tpl_m3_n2_diferencia_precio_ahorro": ["esc_pp_tienda"],
        "tpl_m3_n2_recargo": ["esc_pp_tienda"],
        "tpl_m3_n2_tres_ahorros": ["esc_pp_tienda"],
        "tpl_m3_n3_promedio_tres": ["esc_pp_notas"],
        "tpl_m3_n3_suma": ["esc_pp_notas"],
        "tpl_m3_n3_promedio_mas_bonus": ["esc_pp_notas"],
        "tpl_m3_n3_doble_promedio": ["esc_pp_notas"],
        "tpl_m3_n3_triple_promedio": ["esc_pp_notas"],
        "tpl_m3_n3_mitad_promedio": ["esc_pp_notas"],
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
        # El banco histórico tenía seis familias por nivel. Las extensiones
        # añaden familias de transferencia sin alterar las plantillas ya
        # auditadas; conservar esta identidad permite medir cobertura real.
        from .plantillas_extendidas import build_extended_templates
        self.plantillas.extend(build_extended_templates())
        self.plantillas = [
            plantilla for plantilla in self.plantillas
            if plantilla["id"] not in self._PLANTILLAS_PEDAGOGICAMENTE_EXCLUIDAS
        ]
        for plantilla in self.plantillas:
            if plantilla["id"] in self._ESCENARIOS_POR_PLANTILLA:
                plantilla["escenario_ids"] = self._ESCENARIOS_POR_PLANTILLA[plantilla["id"]]
            if plantilla["modulo_id"] == 3 and plantilla["nivel_id"] == 2:
                plantilla.setdefault("escenario_ids", ["esc_pp_tienda"])
            if plantilla["modulo_id"] == 3 and plantilla["nivel_id"] == 3:
                plantilla.setdefault("escenario_ids", ["esc_pp_notas"])

            plantilla_id = plantilla["id"]
            if plantilla["modulo_id"] == 2 and plantilla["nivel_id"] == 1:
                if "cuatro_grupos" in plantilla_id:
                    plantilla["grupos_solicitados"] = 4
                elif "tres_grupos" in plantilla_id:
                    plantilla["grupos_solicitados"] = 3
                elif "dos_grupos" in plantilla_id or "doble_unitaria" in plantilla_id:
                    plantilla["grupos_solicitados"] = 2
                if "grupos_solicitados" in plantilla:
                    plantilla["resultado_no_supera_total"] = True
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

        # La magnitud general no basta: porcentajes de votos, descuentos y
        # promedios comparten módulo, pero no son escenarios intercambiables.
        sub_magnitudes = plantilla.get("sub_magnitudes") or []
        if sub_magnitudes and escenario.get("sub_magnitud") not in sub_magnitudes:
            raise ValueError(
                f"R2b violada: plantilla '{plantilla['id']}' admite {sub_magnitudes}, "
                f"pero escenario '{escenario['id']}' usa {escenario.get('sub_magnitud')!r}"
            )

        escenarios_permitidos = plantilla.get("escenario_ids") or []
        if escenarios_permitidos and escenario.get("id") not in escenarios_permitidos:
            raise ValueError(
                f"R2c violada: escenario '{escenario.get('id')}' no pertenece al contrato "
                f"de la plantilla '{plantilla['id']}'"
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

        if texto_enunciado:
            if re.search(r"\{[A-Za-z_][A-Za-z0-9_]*\}", texto_enunciado):
                raise ValueError(f"Enunciado con placeholder sin resolver: {texto_enunciado!r}")
            for patron, motivo in self._PATRONES_ENUNCIADO_PROHIBIDOS:
                if patron.search(texto_enunciado):
                    raise ValueError(
                        f"Enunciado no publicable ({motivo}) en plantilla "
                        f"'{plantilla['id']}': {texto_enunciado!r}"
                    )

        if opciones:
            for op in opciones:
                if len(str(op)) > 60:
                    raise ValueError(f"Presupuesto superado: opción '{op}' tiene {len(str(op))} caracteres (máximo 60)")

        return True

    @staticmethod
    def _valores_cumplen_dominio(plantilla: dict, valores: dict, resultado: float) -> bool:
        """Comprueba restricciones pedagógicas declarativas de una familia."""
        if resultado <= 0:
            return False

        total = float(valores.get("total", 0) or 0)
        if plantilla.get("resultado_no_supera_total") and total > 0 and resultado > total:
            return False

        if plantilla.get("resultado_es_porcentaje") and not 0 <= resultado <= 100:
            return False

        if plantilla.get("resultado_es_promedio"):
            datos = [float(valores[k]) for k in ("a", "b", "c") if k in valores]
            if datos and not min(datos) <= resultado <= max(datos):
                return False

        grupos_solicitados = plantilla.get("grupos_solicitados")
        if grupos_solicitados is not None and int(grupos_solicitados) > int(valores.get("b", 0)):
            return False
        return True

    @staticmethod
    def _validar_visual(plantilla: dict, valores: dict, visual: dict) -> None:
        """Valida que la figura contenga el planteo y coincida con sus datos."""
        tipo = visual.get("tipo_visual")
        if not tipo:
            raise ValueError(f"Plantilla '{plantilla['id']}' no produjo tipo_visual")

        requeridos = {
            "pizza": (),
            "fraction_strip": ("numerador", "denominador"),
            "equivalence_strip": ("fraccion_izquierda", "fraccion_derecha", "objetivo_visual"),
            "collection_grid": ("total", "grupos", "grupos_destacados"),
            "group_cards": ("total", "grupos", "grupos_destacados"),
            "percentage_beaker": ("total",),
            "hundred_grid": ("porcentaje", "total"),
            "bar_chart": ("val_a", "val_b", "val_c"),
            "data_table": ("valores_tabla", "etiquetas"),
            "ratio_grid": ("ratio_a", "ratio_b"),
            "ratio_table": ("ratio_a", "ratio_b"),
        }
        if tipo not in requeridos:
            raise ValueError(f"Tipo visual no soportado en Fase 5: {tipo!r}")
        faltantes = [campo for campo in requeridos[tipo] if visual.get(campo) is None]
        if faltantes:
            raise ValueError(f"Visual '{tipo}' incompleto en '{plantilla['id']}': {faltantes}")

        if tipo == "equivalence_strip":
            for lado in ("fraccion_izquierda", "fraccion_derecha"):
                fraccion = visual.get(lado)
                if not isinstance(fraccion, dict) or not {"numerador", "denominador"} <= set(fraccion):
                    raise ValueError(f"Visual de equivalencia sin contrato de {lado} en '{plantilla['id']}'")
                num, den = fraccion["numerador"], fraccion["denominador"]
                if den is not None and int(den) <= 0:
                    raise ValueError(f"Denominador inválido en visual '{plantilla['id']}'")
                if num is not None and den is not None and not 0 <= int(num) <= int(den):
                    raise ValueError(f"Fracción visual inválida en '{plantilla['id']}'")

        if tipo == "pizza":
            if "num_base" in visual:
                if (
                    int(visual.get("num_base", -1)) != int(valores.get("a", -2))
                    or int(visual.get("den_base", -1)) != int(valores.get("b", -2))
                    or int(visual.get("factor", -1)) != int(valores.get("c", -2))
                ):
                    raise ValueError(f"Visual de equivalencia contradice los datos de '{plantilla['id']}'")
            else:
                cortes = int(visual.get("cortes", 0))
                sombreados = visual.get("sombreados") or []
                if cortes != int(valores.get("b", 0)) or len(sombreados) != int(valores.get("a", 0)):
                    raise ValueError(f"Pizza contradice numerador/denominador en '{plantilla['id']}'")

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

    @staticmethod
    def _equivalence_visual_payload(valores: dict, plantilla: dict) -> dict:
        """Construye el rompecabezas visual de equivalencia de M1N2.

        La incógnita se representa con ``None`` y nunca se imprime el factor ni
        la operación que produce la respuesta. Las dos tiras sí conservan las
        divisiones necesarias para comparar, agrupar, detectar un error o
        contar cortes; por eso la figura participa realmente en la solución.
        """
        a = int(valores["a"])
        b = int(valores["b"])
        c = int(valores["c"])
        ac, bc = a * c, b * c
        incognita = plantilla.get("incognita", "")

        izquierda = {"numerador": a, "denominador": b}
        derecha = {"numerador": ac, "denominador": bc}
        modo = "equivalencia"
        termino_incorrecto = None
        objetivos = {
            "nuevo_numerador": "completa el numerador equivalente",
            "nuevo_denominador": "completa el denominador equivalente",
            "factor_equivalencia": "deduce el factor común",
            "numerador_original": "recupera el numerador original",
            "denominador_original": "recupera el denominador original",
            "subdivisiones_por_parte": "compara las subdivisiones",
            "cortes_nuevos_coloreados": "cuenta cortes nuevos en la zona coloreada",
            "cortes_nuevos_totales": "cuenta cortes nuevos en toda la tira",
            "corregir_numerador": "corrige el numerador marcado",
            "corregir_denominador": "corrige el denominador marcado",
            "numerador_simplificado": "completa el numerador simplificado",
            "denominador_simplificado": "completa el denominador simplificado",
            "tira_equivalente": "completa las partes coloreadas de la segunda tira",
        }

        if incognita in {"nuevo_numerador", "tira_equivalente"}:
            derecha["numerador"] = None
        elif incognita == "nuevo_denominador":
            derecha["denominador"] = None
        elif incognita in {"numerador_original", "numerador_simplificado"}:
            izquierda["numerador"] = None
        elif incognita in {"denominador_original", "denominador_simplificado"}:
            izquierda["denominador"] = None
        elif incognita == "corregir_numerador":
            derecha["numerador"] = ac + 1
            modo = "revision"
            termino_incorrecto = "numerador"
        elif incognita == "corregir_denominador":
            derecha["denominador"] = bc - 1
            modo = "revision"
            termino_incorrecto = "denominador"

        return {
            "tipo_visual": "equivalence_strip",
            "fraccion_izquierda": izquierda,
            "fraccion_derecha": derecha,
            "objetivo_visual": objetivos.get(incognita, "compara las dos representaciones"),
            "modo_visual": modo,
            "termino_incorrecto": termino_incorrecto,
            "mostrar_cortes": incognita in {
                "factor_equivalencia", "subdivisiones_por_parte",
                "cortes_nuevos_coloreados", "cortes_nuevos_totales",
            },
        }

    def _visual_payload(
        self,
        modulo_id: int,
        nivel_id: int,
        valores: dict,
        plantilla: dict | None = None,
        escenario: dict | None = None,
    ) -> dict:
        """E2: figura por módulo (tipo_visual + datos que espera el visualizador
        del frontend). Muestra el PLANTEO (contexto) sin revelar la respuesta;
        el alumno razona sobre la figura.
          M1 → pizza (fracción a/b); M1N2 → pizza de equivalencias (base/factor)
          M2 → colección agrupada (fracción de una cantidad)
          M3N1/N2 → hundred_grid con el porcentaje dado; M3N3 → bar_chart (promedio)
          M4 → ratio_grid (razón a:b)
        """
        a = int(valores.get("a", 0))
        b = int(valores.get("b", 0))
        c = int(valores.get("c", 0))
        total = int(valores.get("total", 0))
        visual_model = plantilla.get("visual_model") if plantilla else None
        etiqueta_elementos = (escenario or {}).get("objeto", "elementos")

        if visual_model == "equivalence_strip":
            return self._equivalence_visual_payload(valores, plantilla)
        if visual_model == "fraction_strip":
            payload = {
                "tipo_visual": visual_model,
                "numerador": a,
                "denominador": b,
            }
            return payload
        if visual_model == "group_cards":
            return {
                "tipo_visual": "group_cards",
                "total": total,
                "grupos": b,
                "grupos_destacados": a,
                "etiqueta_elementos": etiqueta_elementos,
            }
        if visual_model == "hundred_grid":
            return {
                "tipo_visual": "hundred_grid",
                "porcentaje": a,
                "total": total,
            }
        if visual_model == "data_table":
            return {
                "tipo_visual": "data_table",
                "valores_tabla": [a, b, c],
                "etiquetas": ["Registro A", "Registro B", "Registro C"],
            }
        if visual_model == "ratio_table":
            return {
                "tipo_visual": "ratio_table",
                "ratio_a": a,
                "ratio_b": b,
                "factor": c if c > 1 else None,
                "total": total,
            }

        if modulo_id == 1:
            if nivel_id == 2 and c > 0:
                return self._equivalence_visual_payload(valores, plantilla or {})
            cortes = b if b > 0 else 8
            return {"tipo_visual": "pizza", "cortes": cortes,
                    "sombreados": list(range(min(max(a, 0), cortes)))}
        if modulo_id == 2:
            grupos = b if b > 0 else 4
            return {
                "tipo_visual": "collection_grid",
                "total": total,
                "grupos": grupos,
                "grupos_destacados": min(max(a, 0), grupos),
                "etiqueta_elementos": etiqueta_elementos,
            }
        if modulo_id == 3:
            if nivel_id == 3:
                return {"tipo_visual": "bar_chart", "val_a": a, "val_b": b,
                        "val_c": c, "categorias": ["Nota 1", "Nota 2", "Nota 3"]}
            return {
                "tipo_visual": "hundred_grid",
                "porcentaje": a,
                "total": total if total > 0 else 100,
            }
        if modulo_id == 4:
            return {
                "tipo_visual": "ratio_grid",
                "ratio_a": a,
                "ratio_b": b,
                "factor": c if c > 1 else None,
            }
        return {}

    def _explicar_pasos(self, plantilla: dict, valores: dict, resultado_num: float) -> list[dict]:
        """Devuelve la explicación como lista de pasos [{orden, texto}] en
        lenguaje concreto (aritmética real), no la fórmula interna."""
        if plantilla.get("modulo_id") == 1 and plantilla.get("nivel_id") == 2:
            a, b, c = (int(valores[k]) for k in ("a", "b", "c"))
            ac, bc = a * c, b * c
            incognita = plantilla.get("incognita", "")
            guias = {
                "nuevo_numerador": [
                    f"Compara los denominadores: {bc} ÷ {b} = {c}.",
                    f"Aplica ese mismo factor al numerador: {a} × {c} = {ac}.",
                ],
                "tira_equivalente": [
                    f"Cada una de las {b} partes originales se convirtió en {c} partes pequeñas porque {bc} ÷ {b} = {c}.",
                    f"Entonces las {a} partes coloreadas producen {a} × {c} = {ac} partes coloreadas pequeñas.",
                ],
                "nuevo_denominador": [
                    f"Compara los numeradores: {ac} ÷ {a} = {c}.",
                    f"Aplica ese mismo factor al denominador: {b} × {c} = {bc}.",
                ],
                "factor_equivalencia": [
                    f"Compara términos correspondientes: {bc} ÷ {b} = {c}.",
                    f"Se confirma con los numeradores: {ac} ÷ {a} = {c}.",
                ],
                "subdivisiones_por_parte": [
                    f"La tira pasó de {b} a {bc} partes iguales.",
                    f"Por cada parte original hay {bc} ÷ {b} = {c} partes pequeñas.",
                ],
                "numerador_original": [
                    f"La fracción se amplificó por {bc} ÷ {b} = {c}.",
                    f"Para volver al numerador original, agrupa: {ac} ÷ {c} = {a}.",
                ],
                "numerador_simplificado": [
                    f"El denominador se reduce de {bc} a {b}: {bc} ÷ {b} = {c}.",
                    f"Divide también el numerador: {ac} ÷ {c} = {a}.",
                ],
                "denominador_original": [
                    f"La fracción se amplificó por {ac} ÷ {a} = {c}.",
                    f"Para volver al denominador original, agrupa: {bc} ÷ {c} = {b}.",
                ],
                "denominador_simplificado": [
                    f"El numerador se reduce de {ac} a {a}: {ac} ÷ {a} = {c}.",
                    f"Divide también el denominador: {bc} ÷ {c} = {b}.",
                ],
                "cortes_nuevos_coloreados": [
                    f"Cada parte coloreada necesita {c} − 1 = {c - 1} cortes interiores nuevos.",
                    f"En {a} partes coloreadas se añaden {a} × {c - 1} = {a * (c - 1)} cortes.",
                ],
                "cortes_nuevos_totales": [
                    f"Cada parte original necesita {c} − 1 = {c - 1} cortes interiores nuevos.",
                    f"En las {b} partes se añaden {b} × {c - 1} = {b * (c - 1)} cortes.",
                ],
                "corregir_numerador": [
                    f"El denominador cambió por el factor {bc} ÷ {b} = {c}.",
                    f"El numerador debe cambiar con el mismo factor: {a} × {c} = {ac}; por eso {ac + 1} rompe la equivalencia.",
                ],
                "corregir_denominador": [
                    f"El numerador cambió por el factor {ac} ÷ {a} = {c}.",
                    f"El denominador debe cambiar con el mismo factor: {b} × {c} = {bc}; por eso {bc - 1} rompe la equivalencia.",
                ],
            }
            pasos_txt = guias.get(incognita)
            if pasos_txt:
                return [
                    {"orden": 1, "texto": "Compara términos que ocupan la misma posición en las dos fracciones."},
                    *[
                        {"orden": index + 2, "texto": texto}
                        for index, texto in enumerate(pasos_txt)
                    ],
                    {"orden": len(pasos_txt) + 2, "texto": f"Por eso, la respuesta correcta es {self._fmt_num(resultado_num)}."},
                ]

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

        # El sustantivo ya quedó en singular; ahora concuerda también el verbo
        # y el adjetivo que algunas plantillas variables escriben en plural.
        texto = re.sub(r"\b1 parte están coloreadas\b", "1 parte está coloreada", texto, flags=re.IGNORECASE)
        texto = re.sub(r"\b1 parte están marcadas\b", "1 parte está marcada", texto, flags=re.IGNORECASE)
        texto = re.sub(r"\b1 porción usadas\b", "1 porción usada", texto, flags=re.IGNORECASE)
        texto = re.sub(r"\b1 porción principales\b", "1 porción principal", texto, flags=re.IGNORECASE)

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
            sustantivo = self._SINGULAR_A_PLURAL.get(palabra, susta)
            return f"{base} {sustantivo}"

        texto = re.sub(
            r"\b([Cc]uánt[oa]s)\s+([A-Za-zÁÉÍÓÚÑáéíóúñ]+)\b",
            _concordar_pronombre,
            texto,
        )

        # Corrección de artículos indefinidos con sustantivos femeninos:
        texto = re.sub(
            r"\bun\s+(pizza|barra de chocolate|ventana|bandera|parcela|rebanada|flor|cuenta|caja|moneda|parte|porción|celda)\b",
            r"una \1",
            texto,
            flags=re.IGNORECASE,
        )
        texto = re.sub(
            r"\bUn\s+(pizza|barra de chocolate|ventana|bandera|parcela|rebanada|flor|cuenta|caja|moneda|parte|porción|celda)\b",
            r"Una \1",
            texto,
        )
        # Corrección de participio con sujeto masculino ("el pastel dividida" -> "el pastel dividido"):
        texto = re.sub(r"\b(el\s+[A-Za-zÁÉÍÓÚÑáéíóúñ]+)\s+(está|fue)\s+dividida\b", r"\1 \2 dividido", texto, flags=re.IGNORECASE)
        texto = re.sub(r"\b(El\s+[A-Za-zÁÉÍÓÚÑáéíóúñ]+)\s+(está|fue)\s+dividida\b", r"\1 \2 dividido", texto)
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
            "a_times_c_plus_1": str(a_val * c_val + 1),
            "b_times_c_minus_1": str(b_val * c_val - 1),
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
            and (
                not plantilla.get("sub_magnitudes")
                or e.get("sub_magnitud") in plantilla["sub_magnitudes"]
            )
            and (
                not plantilla.get("escenario_ids")
                or e.get("id") in plantilla["escenario_ids"]
            )
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
        valores_validos = False
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
            # En M1N2 la figura es parte del planteo. Un valor oculto en el
            # texto puede seguir apareciendo en una de las dos tiras (caso
            # real: el factor 2 coincidía con el numerador visible 2). También
            # se controla esa vía para que la imagen nunca copie la respuesta.
            if sin_coincidencia and modulo_id == 1 and nivel_id == 2 and resultado_num.is_integer():
                visual_prueba = self._equivalence_visual_payload(valores, plantilla)
                numeros_visibles = {
                    str(valor)
                    for lado in ("fraccion_izquierda", "fraccion_derecha")
                    for valor in visual_prueba[lado].values()
                    if valor is not None
                }
                sin_coincidencia = str(int(resultado_num)) not in numeros_visibles
            dominio_ok = self._valores_cumplen_dominio(plantilla, valores, resultado_num)
            if entero_ok and sin_coincidencia and dominio_ok:
                valores_validos = True
                break

        if not valores_validos:
            raise ValueError(
                f"No fue posible generar valores pedagógicamente válidos para "
                f"'{plantilla['id']}' después de 50 intentos"
            )

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
        if len(opciones) != 4 or len(set(opciones)) != 4:
            raise ValueError(f"Opciones inválidas o duplicadas en plantilla '{plantilla['id']}': {opciones}")
        self.validar_composicion(
            plantilla,
            escenario,
            texto_enunciado=enunciado,
            opciones=opciones,
        )

        # E4: explicación paso a paso real (aritmética concreta), no la fórmula.
        explicacion_pasos = self._explicar_pasos(plantilla, valores, resultado_num)
        explicacion_texto = " ".join(p["texto"] for p in explicacion_pasos)

        visual = self._visual_payload(
            modulo_id,
            nivel_id,
            valores,
            plantilla=plantilla,
            escenario=escenario,
        )
        self._validar_visual(plantilla, valores, visual)

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
                "plantilla_id": plantilla["id"],
                "habilidad": plantilla.get("habilidad", plantilla.get("operacion_correcta")),
                "requiere_figura": True,
                "resultado_num": resultado_num,
                "formula": plantilla["formula"],
                **visual,
            }
        }

    def family_count(self, modulo_id: int, nivel_id: int) -> int:
        """Cantidad de familias auditables disponibles en un nivel."""
        return len([
            p for p in self.plantillas
            if p["modulo_id"] == modulo_id and p["nivel_id"] == nivel_id
        ])

    def _generar_valores(self, plantilla: dict, fam_idx: int, var_idx: int, rng: random.Random) -> dict:
        modulo_id = plantilla["modulo_id"]
        nivel_id = plantilla["nivel_id"]
        resta_ordenada = (
            plantilla["id"] in self._PLANTILLAS_RESTA_ORDENADA
            or (plantilla["id"].startswith("tplx_") and "diferencia" in plantilla["id"])
        )

        if modulo_id == 1:
            if nivel_id == 1:
                b = rng.choice([4, 6, 8, 10, 12])
                # tpl_m1_n1_diferencia calcula (b-a)-a = b-2a y narra "cuántas
                # partes MÁS quedan libres que tomadas": exige b-2a > 0, es
                # decir a < b/2. b siempre es par en este conjunto.
                a = rng.randint(1, b // 2 - 1) if resta_ordenada else rng.randint(1, b - 1)
                return {"a": a, "b": b}
            elif nivel_id == 2:
                b = rng.choice([5, 6, 8])
                a = rng.randint(1, b - 1)
                if plantilla.get("id") == "tpl_m1_n2_den_cuadruple":
                    c = 4
                else:
                    c = rng.choice([2, 3, 4])
                return {"a": a, "b": b, "c": c}
            else:  # nivel 3
                b = rng.choice([6, 8, 10, 12])
                # Las familias que usan la mitad del resto exigen que (b - a)
                # sea estrictamente par para que //2 nunca trunque decimales.
                if plantilla.get("id") in {
                    "tpl_m1_n3_mitad_resto",
                    "tpl_m1_n3_suma_resto_usadas",
                }:
                    pares_validos = [x for x in range(2, b - 1, 2)]
                    a = rng.choice(pares_validos) if pares_validos else 2
                elif resta_ordenada:
                    a = rng.randint(1, b // 2 - 1)
                else:
                    a = rng.randint(1, b - 2)
                return {"a": a, "b": b}
        elif modulo_id == 2:
            if nivel_id == 1:
                minimo_grupos = int(plantilla.get("grupos_solicitados", 2))
                denominadores = [x for x in [2, 3, 4, 5, 10] if x >= minimo_grupos]
                b = rng.choice(denominadores)
                if plantilla.get("id") == "tpl_m2_n1_mitad_unitaria":
                    # k = total // b debe ser estrictamente par para que la mitad sea entera exacta
                    k = rng.choice([4, 6, 8, 10, 12])
                else:
                    k = rng.randint(4, 12)
                total = b * k
                return {"a": 1, "b": b, "total": total}
            elif nivel_id == 2:
                b = rng.choice([3, 4, 5, 10])
                if plantilla.get("id") == "tpl_m2_n2_mitad_tomados":
                    # (total // b) * a = k * a debe ser par; usamos k par
                    k = rng.choice([4, 6, 8])
                    a = rng.randint(2, b - 1)
                elif resta_ordenada:
                    # tpl_m2_n2_diferencia_tomados_resto: k*(2a-b) exige 2a>b para
                    # que "tomados" > "restantes" ESTRICTO. Con 2a==b la diferencia
                    # sería 0 y "en cuánto superan" carece de sentido.
                    a = rng.randint(b // 2 + 1, b - 1)
                    k = rng.randint(3, 8)
                else:
                    a = rng.randint(2, b - 1)
                    k = rng.randint(3, 8)
                total = b * k
                return {"a": a, "b": b, "total": total}
            else:  # nivel 3
                b = rng.choice([3, 4, 5, 8])
                if plantilla.get("id") == "tpl_m2_n3_mitad_complemento":
                    # k * (b - a) debe ser estrictamente par
                    k = rng.choice([4, 6, 8, 10])
                    a = rng.randint(1, b - 1)
                else:
                    a = rng.randint(1, b - 1)
                    k = rng.randint(4, 10)
                total = b * k
                return {"a": a, "b": b, "total": total}
        elif modulo_id == 3:
            if nivel_id == 1:
                a = rng.choice([10, 20, 25, 50])
                totals_valid = [t for t in [40, 60, 80, 100, 120, 160, 200] if (a * t) % 100 == 0]
                if plantilla.get("id") == "tpl_m3_n1_mitad_porcentaje":
                    # ((total * a) // 100) debe ser estrictamente par
                    totals_valid = [t for t in totals_valid if ((t * a) // 100) % 2 == 0]
                total = rng.choice(totals_valid) if totals_valid else 100
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
                if plantilla.get("id") == "tpl_m3_n3_mitad_promedio":
                    # El promedio (a + b + c) // 3 debe ser estrictamente par
                    target_prom = rng.choice([12, 14, 16, 18])
                    diff1 = rng.randint(-3, 3)
                    diff2 = rng.randint(-3, 3)
                    diff3 = -(diff1 + diff2)
                    a = target_prom + diff1
                    b = target_prom + diff2
                    c = target_prom + diff3
                    return {"a": a, "b": b, "c": c}
                else:
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
                if resta_ordenada:
                    opciones_b = [x for x in (2, 3, 4, 5) if x > a]
                    b = rng.choice(opciones_b) if opciones_b else max(a + 1, 2)
                else:
                    b = rng.choice([2, 3, 4, 5])
                if plantilla.get("id") == "tpl_m4_n1_mitad_a":
                    # a * c debe ser par
                    c = rng.choice([2, 4]) if a % 2 != 0 else rng.choice([2, 3, 4])
                else:
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
                if plantilla.get("id") == "tpl_m4_n2_mitad_a":
                    # k * a debe ser estrictamente par
                    k = rng.choice([4, 6, 8])
                else:
                    k = rng.randint(3, 8)
                n_cant = a + b
                total = n_cant * k
                return {"a": a, "b": b, "n_cant": n_cant, "total": total}
            else:  # nivel 3: mezclas y % de volumen
                target_total = rng.choice([4, 5, 8, 10, 20, 25, 50])
                valid_a = [x for x in range(1, target_total) if (x * 100) % target_total == 0]
                if plantilla.get("id") == "tpl_m4_n3_mitad_pct_a":
                    # (a * 100 // target_total) debe ser estrictamente par
                    valid_a = [x for x in valid_a if ((x * 100) // target_total) % 2 == 0] or valid_a
                elif resta_ordenada:
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
