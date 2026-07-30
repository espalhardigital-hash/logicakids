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
        escenarios_compatibles = [
            e for e in self.escenarios 
            if e["modulo_id"] == modulo_id and e["magnitud"] == plantilla["magnitud"]
            and all(req in e and e[req] for req in plantilla.get("campos_requeridos", []))
        ]
        if not escenarios_compatibles:
            raise ValueError(f"No hay escenarios compatibles para plantilla '{plantilla['id']}'")
        
        esc = escenarios_compatibles[(fam_idx + var_idx) % len(escenarios_compatibles)]
        
        # Validate R1 & R2 contract
        self.validar_composicion(plantilla, esc)
        
        # Build text dynamically from template and scenario
        a_val = round(1.20 + (fam_idx * 0.05) + rng.uniform(0.01, 0.05), 2)
        b_val = round(0.85 + (fam_idx * 0.03) + rng.uniform(0.01, 0.05), 2)
        c_val = round(0.50 + rng.uniform(0.01, 0.05), 2)
        total_val = round(a_val + b_val + c_val, 2)
        
        fmt_a = f"{a_val:.2f}".replace('.', ',')
        fmt_b = f"{b_val:.2f}".replace('.', ',')
        fmt_c = f"{c_val:.2f}".replace('.', ',')
        fmt_total = f"{total_val:.2f}".replace('.', ',')
        
        unit = esc.get("unidad", "R$")
        obj0 = esc.get("objetos", ["artículo A"])[0]
        obj1 = esc.get("objetos", ["artículo B"])[1] if len(esc.get("objetos", [])) > 1 else "artículo B"
        lugar = esc.get("lugar", "el comercio")
        
        enunciado = plantilla["marco"].format(
            personaje=personaje, lugar=lugar,
            objetos_0=obj0, objetos_1=obj1,
            objeto_medible=esc.get("objeto_medible", "el elemento"),
            sujeto_medible=esc.get("sujeto_medible", "el total"),
            atributo=esc.get("atributo", "el valor"),
            unidad=unit, a=fmt_a, b=fmt_b, c=fmt_c, total=fmt_total, n_cant=3, ruido=fmt_total
        )
        pregunta_txt = f"{enunciado} {plantilla['pregunta']}"
        
        # Character budget validation
        self.validar_composicion(plantilla, esc, texto_enunciado=pregunta_txt)
        
        return {
            "plantilla_id": plantilla["id"],
            "escenario_id": esc["id"],
            "modulo_id": modulo_id,
            "nivel_id": nivel_id,
            "enunciado": pregunta_txt,
            "operacion_correcta": plantilla["operacion_correcta"],
            "respuesta_correcta": fmt_total
        }
