"""
Motor Compositor con Validación para la Fase 4 (LogicaMath)
Cumple con las decisiones C7.1 - C7.11 y la norma de validación de contenido generado de deep_analise_pro §25.4.
"""

import json
import os
import random
from typing import Dict, Any, List

from app.utils.svg_figuras import diagrama_conversion, tabla_datos

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
        
        # Character budget checks (§4.3): Enunciado <= 350 chars, Opciones <= 60 chars
        if texto_enunciado and len(texto_enunciado) > 350:
            raise ValueError(f"Presupuesto superado: enunciado tiene {len(texto_enunciado)} caracteres (máximo 350)")
        
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
        
        # ── Generación de valores exactos (máx 2 decimales, CERO redondeos) ──
        # Para que un niño de 10 años no tenga que redondear ni truncar,
        # los operandos y el resultado DEBEN ser números exactos (enteros o max 2 decimales).
        # ── Generación de valores ────────────────────────────────────────────
        n_cant = 2 + (fam_idx % 4)                      # 2..5
        a_val = round(1.20 + (fam_idx * 0.05), 2)
        b_val = round(0.85 + (fam_idx * 0.03), 2)
        c_val = round(0.50 + (fam_idx * 0.02), 2)
        total_val = round(a_val + b_val + c_val + 1.0, 2)

        formula = plantilla.get("formula", "")

        # ── Garantía de cocientes y productos exactos (máx 2 decimales, sin redondeos) ──
        if formula == "a/n_cant":
            # Elegir un resultado objetivo exacto Q (entero o máx 2 decimales)
            opciones_q = [0.25, 0.4, 0.5, 0.75, 0.8, 1.2, 1.25, 1.5, 1.75, 2.2, 2.25, 2.4, 2.5, 3.2, 3.5, 4.25, 5.25]
            q_target = opciones_q[fam_idx % len(opciones_q)]
            a_val = round(q_target * n_cant, 2)
        elif formula == "a/b":
            # Parejas (b_val, q_target) donde a_val = b_val * q_target es exacto con <= 2 decimales
            parejas_div = [
                (0.5, 1.4),   # a = 0.7, a/b = 1.4
                (0.4, 1.25),  # a = 0.5, a/b = 1.25
                (0.8, 1.25),  # a = 1.0, a/b = 1.25
                (1.2, 1.5),   # a = 1.8, a/b = 1.5
                (1.5, 2.4),   # a = 3.6, a/b = 2.4
                (2.5, 1.8),   # a = 4.5, a/b = 1.8
                (0.5, 2.4),   # a = 1.2, a/b = 2.4
                (0.25, 4.8),  # a = 1.2, a/b = 4.8
                (1.6, 2.5),   # a = 4.0, a/b = 2.5
                (0.8, 2.25),  # a = 1.8, a/b = 2.25
                (1.25, 0.8),  # a = 1.0, a/b = 0.8
                (2.4, 1.5),   # a = 3.6, a/b = 1.5
            ]
            b_val, q_target = parejas_div[(fam_idx + var_idx) % len(parejas_div)]
            a_val = round(b_val * q_target, 2)
        elif plantilla.get("incognita") == "factor_faltante" or formula == "total/a":
            # total / a = entero o 1 decimal
            opciones_q = [2, 3, 4, 5, 1.5, 2.5, 3.5, 4.5, 1.2, 2.4]
            q_target = opciones_q[fam_idx % len(opciones_q)]
            a_val = round(1.2 + (fam_idx % 5) * 0.5, 2)
            total_val = round(a_val * q_target, 2)
        elif formula == "(total-c)/n_cant":
            opciones_q = [0.25, 0.5, 0.75, 1.2, 1.25, 1.5, 2.0, 2.5, 3.25, 4.5]
            q_target = opciones_q[fam_idx % len(opciones_q)]
            total_val = round(q_target * n_cant + c_val, 2)
        elif formula == "a*b":
            # Parejas exactas (a, b) cuyo producto a*b tiene MÁXIMO 2 decimales sin aproximar
            parejas_ab = [
                (1.5, 0.8),   # 1.2
                (2.4, 1.5),   # 3.6
                (3.5, 1.2),   # 4.2
                (1.25, 0.4),  # 0.5
                (2.5, 0.6),   # 1.5
                (1.8, 0.5),   # 0.9
                (4.2, 0.5),   # 2.1
                (3.6, 0.25),  # 0.9
                (2.8, 1.5),   # 4.2
                (1.6, 2.5),   # 4.0
                (3.2, 1.25),  # 4.0
                (2.25, 0.8),  # 1.8
                (1.4, 2.5),   # 3.5
                (3.8, 0.5),   # 1.9
                (4.5, 0.4),   # 1.8
                (2.6, 1.5),   # 3.9
                (3.4, 0.5),   # 1.7
                (4.8, 0.25),  # 1.2
                (2.15, 2.0),  # 4.3
                (1.75, 0.4),  # 0.7
                (4.4, 1.5),   # 6.6
                (2.2, 1.5),   # 3.3
                (3.25, 0.8),  # 2.6
                (1.45, 2.0),  # 2.9
                (2.75, 0.4),  # 1.1
                (3.12, 0.5),  # 1.56
                (4.24, 0.5),  # 2.12
                (2.36, 0.5),  # 1.18
                (1.84, 0.5),  # 0.92
                (3.68, 0.5),  # 1.84
                (2.14, 0.5),  # 1.07
                (4.16, 0.5),  # 2.08
                (1.52, 0.5),  # 0.76
                (2.48, 0.5),  # 1.24
                (3.72, 0.5),  # 1.86
            ]
            a_val, b_val = parejas_ab[(fam_idx + var_idx) % len(parejas_ab)]

        # ── Escala pedagógica de las conversiones ────────────────────────────
        if "/1000" in formula:
            a_val = round(a_val * 1000, 0) if formula.startswith("a/") else a_val
            total_val = round(total_val * 1000, 0) if formula.startswith("total/") else total_val
        elif "/100" in formula:
            a_val = round(a_val * 100, 0) if formula.startswith("a/") or formula.startswith("a*n_cant/") else a_val
            total_val = round(total_val * 100, 0) if formula.startswith("total/") else total_val
        elif "/10" in formula and formula.startswith("a/"):
            a_val = round(a_val * 10, 0)

        if "b/100" in formula:
            b_val = round(b_val * 100, 0)
        elif "b/10" in formula:
            b_val = round(b_val * 10, 0)
        if "c/100" in formula:
            c_val = round(c_val * 100, 0)

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
            return f"{v:.2f}".replace('.', ',').rstrip('0').rstrip(',') if '.' in f"{v:.2f}" else f"{v:.2f}".replace('.', ',')

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
            "figura_svg": self._figura_svg(plantilla, vals, unit, esc),
        }

    # Operadores permitidos en las fórmulas de plantillas_fase4.json.
    _COLOR_MODULO = {
        1: "#10B981",
        2: "#8B5CF6",
        3: "#F59E0B",
        4: "#EC4899",
    }

    def _figura_svg(self, plantilla: dict, vals: dict, unidad: str, esc: dict | None = None) -> str | None:
        modulo_id = plantilla["modulo_id"]
        color = self._COLOR_MODULO.get(modulo_id, "#A855F7")

        if modulo_id == 4:
            origen_destino = self._unidades_conversion(plantilla)
            if not origen_destino:
                return None
            origen, destino = origen_destino
            tokens = self._tokens_formula(plantilla)
            if len(tokens) == 1:
                token = tokens[0]
                return diagrama_conversion(
                    origen,
                    destino,
                    vals[token],
                    color=color,
                    marco=False,
                )

            filas = self._filas_conversion_svg(plantilla, vals)
            return tabla_datos(filas, titulo="Datos a unificar", color=color, marco=False)

        if int(plantilla.get("n_datos", 0)) < 2:
            return None

        filas, titulo_tabla = self._filas_datos_svg(plantilla, vals, unidad, esc or {})
        if len(filas) < 2:
            return None
        return tabla_datos(filas, titulo=titulo_tabla, color=color, marco=False)

    def _unidades_conversion(self, plantilla: dict) -> tuple[str, str] | None:
        pid = plantilla.get("id", "")
        formula = plantilla.get("formula", "")

        if "_m_cm" in pid or formula == "a*100" or formula == "a*n_cant*100":
            return "m", "cm"
        if "_km_m" in pid or formula in ("a*1000", "a*1000+b", "a*1000-b"):
            return "km", "m"
        if "_cm_mm" in pid or formula in ("a*10", "a+b/10"):
            return "cm", "mm"
        if "_cm_m" in pid or formula in ("a/100", "total/100", "a*n_cant/100", "a+b/100", "a-b/100", "a+b/100+c/100"):
            return "cm", "m"
        if "_m_km" in pid or formula in ("a/1000", "total/1000"):
            return "m", "km"
        if "_mm_cm" in pid or formula == "a/10":
            return "mm", "cm"
        return None

    def _filas_datos_svg(self, plantilla: dict, vals: dict, unidad: str, esc: dict) -> tuple[list[tuple[str, str]], str]:
        formula = plantilla.get("formula", "")
        tokens = self._tokens_formula(plantilla)

        # Variar títulos de tabla para romper la monotonía
        titulos = {
            1: "Resumen de compra",
            2: "Ficha del pedido",
            3: "Datos del reparto",
            4: "Registro de medidas"
        }
        titulo = titulos.get(plantilla.get("modulo_id", 1), "Resumen de datos")

        filas = []
        for token in tokens:
            valor = vals[token]
            
            # Formatear adecuadamente según el tipo de token y contexto (etiquetas <= 15 chars)
            if token == "n_cant":
                etiqueta = "Cantidad"
                texto_valor = f"{int(valor)} unidades"
            elif token == "a" and formula in ("a*b", "a*n_cant"):
                # Si 'a' es la cantidad de tramos/paquetes (conteo)
                if plantilla.get("magnitud") in ("longitud", "masa") and "tramos" in plantilla.get("marco", ""):
                    etiqueta = "Cantidad tramos"
                    texto_valor = f"{self._fmt_visual(valor)} tramos"
                elif plantilla.get("magnitud") == "dinero" and "paquetes" in plantilla.get("marco", ""):
                    etiqueta = "Cant. comprada"
                    texto_valor = f"{self._fmt_visual(valor)} paquetes"
                else:
                    etiqueta = "Valor A"
                    texto_valor = f"{self._fmt_visual(valor)} {unidad}" if unidad not in ("R$", "$", "EUR") else f"{unidad} {self._fmt_visual(valor)}"
            elif token == "b" and formula == "a*b":
                if unidad in ("R$", "$", "EUR"):
                    etiqueta = "Precio unitario"
                    texto_valor = f"{unidad} {self._fmt_visual(valor)}"
                else:
                    etiqueta = "Medida unitaria"
                    texto_valor = f"{self._fmt_visual(valor)} {unidad}"
            elif token == "total":
                etiqueta = "Monto total" if unidad in ("R$", "$", "EUR") else "Medida total"
                texto_valor = f"{unidad} {self._fmt_visual(valor)}" if unidad in ("R$", "$", "EUR") else f"{self._fmt_visual(valor)} {unidad}"
            else:
                etiquetas_default = {"a": "Valor A", "b": "Valor B", "c": "Valor C"}
                etiqueta = etiquetas_default.get(token, token.capitalize()[:15])
                if unidad in ("R$", "$", "EUR"):
                    texto_valor = f"{unidad} {self._fmt_visual(valor)}"
                else:
                    texto_valor = f"{self._fmt_visual(valor)} {unidad}"
                    
            filas.append((etiqueta, texto_valor))

        return filas, titulo


    def _tokens_formula(self, plantilla: dict) -> list[str]:
        import re as _re

        permitidos = {"a", "b", "c", "total", "n_cant"}
        tokens = []
        for token in _re.findall(r"[A-Za-z_]+", plantilla.get("formula", "")):
            if token in permitidos and token not in tokens:
                tokens.append(token)
        return tokens

    def _filas_conversion_svg(self, plantilla: dict, vals: dict) -> list[tuple[str, str]]:
        formula = plantilla.get("formula", "")
        unidades_por_formula = {
            "a*n_cant*100": {"a": "m", "n_cant": "unidades"},
            "a*n_cant/100": {"a": "cm", "n_cant": "unidades"},
            "a+b/100": {"a": "m", "b": "cm"},
            "a*1000+b": {"a": "km", "b": "m"},
            "a-b/100": {"a": "m", "b": "cm"},
            "a+b/10": {"a": "cm", "b": "mm"},
            "a*1000-b": {"a": "km", "b": "m"},
            "a+b/100+c/100": {"a": "m", "b": "cm", "c": "cm"},
        }
        etiquetas = {
            "a": "Medida A",
            "b": "Medida B",
            "c": "Medida C",
            "total": "Medida total",
            "n_cant": "Cantidad",
        }
        unidades = unidades_por_formula.get(formula, {})
        filas = []
        for token in self._tokens_formula(plantilla):
            valor = vals[token]
            if token == "n_cant":
                texto_valor = f"{int(valor)} unidades"
            else:
                unidad_token = unidades.get(token, "")
                texto_valor = f"{self._fmt_visual(valor)} {unidad_token}".strip()
            filas.append((etiquetas[token], texto_valor))
        return filas

    def _fmt_visual(self, valor: float) -> str:
        if abs(valor - round(valor)) < 1e-9:
            return str(int(round(valor)))
        return f"{valor:.2f}".replace(".", ",")

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
        if abs(res - round(res, 2)) > 1e-6:
            raise ValueError(f"Fórmula de '{plantilla['id']}' produjo un resultado no exacto/periódico ({res}) con {vals}")
        return round(float(res), 2)
