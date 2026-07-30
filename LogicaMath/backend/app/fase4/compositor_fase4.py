"""
Motor Compositor con Validación para la Fase 4 (LogicaMath)
Cumple con las decisiones C7.1 - C7.11 y la norma de validación de contenido generado de deep_analise_pro §25.4.
"""

import json
import os
import random
from typing import Dict, Any, List

class CompositorFase4:
    def __init__(self, data_dir: str | None = None):
        if not data_dir:
            data_dir = os.path.join(os.path.dirname(__file__), "data")
        
        with open(os.path.join(data_dir, "escenarios_fase4.json"), "r", encoding="utf-8") as f:
            self.escenarios = json.load(f)
        with open(os.path.join(data_dir, "plantillas_fase4.json"), "r", encoding="utf-8") as f:
            self.plantillas = json.load(f)
        with open(os.path.join(data_dir, "confusiones_fase4.json"), "r", encoding="utf-8") as f:
            self.confusiones = json.load(f)
        with open(os.path.join(data_dir, "nombres_fase4.json"), "r", encoding="utf-8") as f:
            self.nombres = json.load(f)

    def validar_composicion(self, plantilla: dict, escenario: dict, etiqueta_tabla: str | None = None, texto_enunciado: str | None = None, opciones: list[str] | None = None) -> bool:
        # R2 check: Magnitude contract
        if plantilla.get("magnitud") != escenario.get("magnitud"):
            raise ValueError(f"R2 violada: plantilla '{plantilla['id']}' es de {plantilla.get('magnitud')} y escenario '{escenario['id']}' es de {escenario.get('magnitud')}")
        
        # R1 check: Required grammatical fields
        campos_req = plantilla.get("campos_requeridos", [])
        for campo in campos_req:
            if campo not in escenario or not escenario[campo]:
                raise ValueError(f"R1 violada: escenario '{escenario['id']}' carece del campo requerido '{campo}' exigido por la plantilla '{plantilla['id']}'")
        
        # Label length check (C8.1): <= 15 chars
        if etiqueta_tabla and len(etiqueta_tabla) > 15:
            raise ValueError(f"Etiqueta de tabla desbordada: '{etiqueta_tabla}' supera 15 caracteres ({len(etiqueta_tabla)})")
        
        # Character budget checks (§4.3): Enunciado <= 250 chars, Opciones <= 60 chars
        if texto_enunciado and len(texto_enunciado) > 250:
            raise ValueError(f"Presupuesto superado: enunciado tiene {len(texto_enunciado)} caracteres (máximo 250)")
        
        if opciones:
            for op in opciones:
                if len(str(op)) > 60:
                    raise ValueError(f"Presupuesto superado: opción '{op}' tiene {len(str(op))} caracteres (máximo 60)")
        
        return True

    def verificar_pool_nivel(self, pool: List[dict], modulo_id: int, nivel_id: int) -> dict:
        total = len(pool)
        if total == 0:
            raise ValueError(f"Pool vacío para módulo {modulo_id}, nivel {nivel_id}")
        
        conteo_esquemas: Dict[str, int] = {}
        for q in pool:
            pid = q.get("plantilla_id", "unknown")
            conteo_esquemas[pid] = conteo_esquemas.get(pid, 0) + 1
        
        n_esquemas = len(conteo_esquemas)
        if n_esquemas < 6:
            raise ValueError(f"Variedad insuficiente: nivel {nivel_id} del módulo {modulo_id} solo tiene {n_esquemas} esquemas (mínimo 6)")
        
        for pid, count in conteo_esquemas.items():
            pct = count / total
            if pct > 0.25:
                raise ValueError(f"Concentración excesiva: esquema '{pid}' representa el {pct:.1%} del pool en módulo {modulo_id}, nivel {nivel_id} (máximo 25%)")
        
        return {
            "total_preguntas": total,
            "n_esquemas": n_esquemas,
            "max_concentracion_pct": max(c / total for c in conteo_esquemas.values())
        }

    def componer_pregunta_practica(self, modulo_id: int, nivel_id: int, fam_idx: int, var_idx: int, seed_val: int) -> dict:
        rng = random.Random(seed_val)
        personaje = self.nombres[(fam_idx + var_idx) % len(self.nombres)]
        
        # Filter templates and scenarios for modulo & nivel
        plantillas_nivel = [p for p in self.plantillas if p["modulo_id"] == modulo_id and p["nivel_id"] == nivel_id]
        if not plantillas_nivel:
            raise ValueError(f"No hay plantillas definidas para módulo {modulo_id}, nivel {nivel_id}")
        
        # Rotate template choice ensuring <=25% concentration
        plantilla = plantillas_nivel[fam_idx % len(plantillas_nivel)]
        
        # Filter scenarios matching template magnitude and campos_requeridos
        escala_req = self._escala_requerida(plantilla)
        escenarios_compatibles = [
            e for e in self.escenarios
            if e["modulo_id"] == modulo_id and e["magnitud"] == plantilla["magnitud"]
            and all(req in e and e[req] for req in plantilla.get("campos_requeridos", []))
            and (escala_req is None or e.get("escala") == escala_req)
        ]
        if not escenarios_compatibles:
            raise ValueError(
                f"No hay escenarios compatibles para plantilla '{plantilla['id']}'"
                + (f" con escala '{escala_req}'" if escala_req else "")
            )
        
        esc = escenarios_compatibles[(fam_idx + var_idx) % len(escenarios_compatibles)]
        
        # Validate R1 & R2 contract
        self.validar_composicion(plantilla, esc)
        
        # ── Generación de valores ────────────────────────────────────────────
        # 'total' NO es la respuesta: es un dato del enunciado (presupuesto, meta,
        # billete...). La respuesta se deriva SIEMPRE de plantilla["formula"] sobre
        # estos mismos valores, para que enunciado y respuesta sean coherentes.
        n_cant = 2 + (fam_idx % 4)                      # 2..5
        a_val = round(1.20 + (fam_idx * 0.05) + rng.uniform(0.01, 0.05), 2)
        b_val = round(0.85 + (fam_idx * 0.03) + rng.uniform(0.01, 0.05), 2)
        c_val = round(0.50 + rng.uniform(0.01, 0.05), 2)
        # 'total' debe ser mayor que los aportes para que restas y faltantes den > 0
        total_val = round(a_val + b_val + c_val + 1.0 + rng.uniform(0.05, 0.4), 2)

        # 'factor_faltante' y 'dividendo' exigen un total coherente con a
        if plantilla["incognita"] == "factor_faltante":
            total_val = round(a_val * n_cant, 2)
        # divisor decimal (M3N3): b debe ser menor que a y no trivial
        if plantilla["formula"] in ("a/b",):
            b_val = round(max(0.25, min(b_val, a_val / 2)), 2)

        # ── Escala pedagógica de las conversiones ────────────────────────────
        # Al SUBIR la escalera (dividir por 100/1000) un valor de 1,22 daría
        # 0,01: el redondeo destruye la respuesta. El operando debe vivir en el
        # rango de la unidad de partida, no en el rango por defecto.
        formula = plantilla["formula"]
        if "/1000" in formula:
            a_val = round(a_val * 1000, 0) if formula.startswith("a/") else a_val
            total_val = round(total_val * 1000, 0) if formula.startswith("total/") else total_val
        elif "/100" in formula:
            a_val = round(a_val * 100, 0) if formula.startswith("a/") or formula.startswith("a*n_cant/") else a_val
            total_val = round(total_val * 100, 0) if formula.startswith("total/") else total_val
        elif "/10" in formula and formula.startswith("a/"):
            a_val = round(a_val * 10, 0)
        # Unidades mixtas: el operando menor debe ser una cantidad realista
        # (una tira de 0,89 cm no existe; 89 cm sí).
        if "b/100" in formula:
            b_val = round(b_val * 100, 0)
        elif "b/10" in formula:
            b_val = round(b_val * 10, 0)
        if "c/100" in formula:
            c_val = round(c_val * 100, 0)
        # a*1000-b y a*1000+b: 'b' está en la unidad menor (m frente a km)
        if "a*1000" in formula and ("+b" in formula or "-b" in formula):
            b_val = round(b_val * 1000, 0)
            if "-b" in formula and b_val >= a_val * 1000:
                b_val = round(a_val * 1000 / 2, 0)

        vals = {"a": a_val, "b": b_val, "c": c_val, "total": total_val, "n_cant": n_cant}
        resultado = self._evaluar_formula(plantilla, vals)

        def fmt(v: float) -> str:
            """Enteros sin decimales de relleno ('450 cm', no '450,00 cm')."""
            if abs(v - round(v)) < 1e-9:
                return str(int(round(v)))
            return f"{v:.2f}".replace('.', ',')

        fmt_a, fmt_b, fmt_c = fmt(a_val), fmt(b_val), fmt(c_val)
        fmt_total = fmt(total_val)
        fmt_res = fmt(resultado)

        unit = esc.get("unidad", "R$")
        objetos = esc.get("objetos") or ["artículo A", "artículo B"]
        obj0 = objetos[0]
        obj1 = objetos[1] if len(objetos) > 1 else "otro artículo"

        campos = dict(
            personaje=personaje,
            lugar=esc.get("lugar", "el comercio"),
            objetos_0=obj0, objetos_1=obj1,
            objeto_medible=esc.get("objeto_medible", "el elemento"),
            sujeto_medible=esc.get("sujeto_medible", "el total"),
            atributo=esc.get("atributo", "la medida"),
            unidad=unit, a=fmt_a, b=fmt_b, c=fmt_c, total=fmt_total,
            n_cant=n_cant, ruido=fmt_total,
        )
        # El marco Y la pregunta se formatean: dejar la pregunta sin formatear
        # deja placeholders crudos como "{unidad}" a la vista del alumno.
        enunciado = plantilla["marco"].format(**campos)
        pregunta_txt = f"{enunciado} {plantilla['pregunta'].format(**campos)}"
        pregunta_txt = self._contraer(pregunta_txt)

        # Character budget validation
        self.validar_composicion(plantilla, esc, texto_enunciado=pregunta_txt)

        return {
            "plantilla_id": plantilla["id"],
            "escenario_id": esc["id"],
            "personaje": personaje,
            "modulo_id": modulo_id,
            "nivel_id": nivel_id,
            "enunciado": pregunta_txt,
            "operacion_correcta": plantilla["operacion_correcta"],
            "incognita": plantilla["incognita"],
            "formula": plantilla["formula"],
            "valores": vals,
            "resultado_num": resultado,
            "respuesta_correcta": fmt_res,
            "unidad": unit,
        }

    # Operadores permitidos en las fórmulas de plantillas_fase4.json.
    # No se usa eval() sobre entrada arbitraria: la fórmula es dato del repo,
    # y aun así se restringe a nombres conocidos (deep_analise_pro §15.2).
    _NOMBRES_FORMULA = {"a", "b", "c", "total", "n_cant"}

    # Contracciones obligatorias del español. Los escenarios traen el artículo
    # incorporado ("el libro"), así que un marco con "de {objeto_medible}" produce
    # "de el libro". Se corrige al componer, no duplicando cada marco por género.
    _CONTRACCIONES = ((" de el ", " del "), (" a el ", " al "),
                      ("De el ", "Del "), ("A el ", "Al "))

    def _contraer(self, texto: str) -> str:
        for origen, destino in self._CONTRACCIONES:
            texto = texto.replace(origen, destino)
        # Un marco que abre con {objeto_medible} hereda el artículo en minúscula
        # ("el libro tiene..."): la frase empieza mal.
        if texto and texto[0].islower():
            texto = texto[0].upper() + texto[1:]
        # "de el." al final de una oración o antes de signo de puntuación
        import re as _re
        texto = _re.sub(r"\bde el\b(?=[.,;:?!)])", "del", texto)
        return texto

    def _escala_requerida(self, plantilla: dict) -> str | None:
        """Escala física que el marco presupone, derivada del factor de conversión.

        R2b: la magnitud sola no da coherencia. 'longitud' cubre el grosor de una
        moneda y una maratón, así que un marco de km montado sobre un escenario de
        espesor produce "recorrió un trayecto en la pila de monedas de 1,57 km".
        El factor de la fórmula ya identifica el par de unidades en juego.
        """
        # Solo el módulo 4 (escalera métrica) tiene escenarios etiquetados: en los
        # módulos 1-3 un factor 100 es dinero o porcentaje, no un salto de unidad.
        if plantilla.get("modulo_id") != 4:
            return None
        formula = plantilla.get("formula") or ""
        if "1000" in formula:
            return "distancia"
        if "100" in formula:
            return "objeto"
        if "10" in formula:
            return "micro"
        return None

    def _evaluar_formula(self, plantilla: dict, vals: dict) -> float:
        formula = plantilla.get("formula")
        if not formula:
            raise ValueError(f"Plantilla '{plantilla['id']}' sin campo 'formula': no se puede derivar la respuesta")

        import re as _re
        usados = set(_re.findall(r"[A-Za-z_]+", formula))
        desconocidos = usados - self._NOMBRES_FORMULA
        if desconocidos:
            raise ValueError(f"Fórmula de '{plantilla['id']}' usa nombres no permitidos: {sorted(desconocidos)}")

        try:
            res = eval(formula, {"__builtins__": {}}, dict(vals))  # noqa: S307 - fórmula versionada en el repo
        except ZeroDivisionError as exc:
            raise ValueError(f"Fórmula de '{plantilla['id']}' divide por cero con {vals}") from exc

        if res is None or res != res or res in (float("inf"), float("-inf")):
            raise ValueError(f"Fórmula de '{plantilla['id']}' produjo un resultado no finito con {vals}")
        if res <= 0:
            raise ValueError(f"Fórmula de '{plantilla['id']}' produjo un resultado no positivo ({res}) con {vals}")
        return round(float(res), 2)
