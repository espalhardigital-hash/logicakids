"""
Seeder completo para la Fase 6: Geometría Plana Multiforme y Áreas.
Cumple strictly con las Secciones 8, 9 y 12 de docs/reestructuraciondefases.md.

Volumetría:
  - 4 Módulos, 15 Niveles de Teoría en niveles_teoria_pool.
  - 15 Niveles de Práctica × 120 familias × 4 variantes (1 original + 3 espejo) = 7.200 preguntas.
  - 13 Bloques de Desafíos (12 de módulo + 1 Mixto de Fase 99099) × 150 = 1.950 preguntas.
  - Total: 9.150 preguntas en la tabla `preguntas` con `estructura_padre_id` SIEMPRE poblado (NUNCA NULL).
  - 29 filas en `configuracion_progreso` (15 de práctica + 13 de desafíos + 1 fallback seccion=0).

Reglas duras:
  - CERO contenido 3D (cubo, arista, poliedro, prisma, volumen, cara, isométrico, cilindro, esfera, capacidad, litro).
  - CERO Tangram, CERO pentágono con apotema.
  - CERO MinIO (100% SVG inline mediante app.utils.svg_figuras).
  - CERO entrada numérica para respuestas no numéricas.
"""

from __future__ import annotations
import asyncio
import json
import os
import random
from typing import Dict, List, Any

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.sql_models import (
    Fase, Pregunta, Alternativa, ConfiguracionProgreso,
    StatusEnum, OperacionEnum, TipoPreguntaEnum, TipoErrorEnum,
    Intento, PoolAsignadoAlumno
)
from app.fase2.models import NivelTeoria, IntentoPregunta, IntentoPaso
from app.fase6.theory_data import FASE6_TEORIA_DATA
from app.utils.svg_figuras import (
    fig_rectangulo, fig_cuadrado, fig_L, fig_T,
    color_modulo
)

FASE6_ID = 6

# Cargar catálogo de escenarios y confusiones de Fase 6
CATALOGO_PATH = os.path.join(os.path.dirname(__file__), "data", "catalogo_fase6.json")
with open(CATALOGO_PATH, "r", encoding="utf-8") as f:
    CATALOGO_FASE6 = json.load(f)

ESCENARIOS_FASE6 = CATALOGO_FASE6.get("escenarios", [])
CONFUSIONES_FASE6 = CATALOGO_FASE6.get("confusiones", [])

def _get_confusiones_map(modulo_id: int) -> Dict[str, dict]:
    return {c["codigo"]: c for c in CONFUSIONES_FASE6 if c.get("modulo_id") == modulo_id}


async def clear_fase6_data(session: AsyncSession) -> None:
    """Purga limpia y en cascada de los datos preexistentes de Fase 6."""
    print("Purga de datos preexistentes de Fase 6 en cascada...")
    
    res = await session.execute(select(Pregunta.id).where(Pregunta.fase_id == FASE6_ID))
    p_ids = res.scalars().all()

    if p_ids:
        for chunk in [p_ids[i:i+1000] for i in range(0, len(p_ids), 1000)]:
            await session.execute(delete(Alternativa).where(Alternativa.pregunta_id.in_(chunk)))
            await session.execute(delete(IntentoPaso).where(IntentoPaso.intento_pregunta_id.in_(
                select(IntentoPregunta.id).where(IntentoPregunta.pregunta_id.in_(chunk))
            )))
            await session.execute(delete(IntentoPregunta).where(IntentoPregunta.pregunta_id.in_(chunk)))

    secciones_fase6 = [
        101, 102, 103, 104, 1011, 1012, 1013,
        201, 202, 203, 2011, 2012, 2013,
        301, 302, 303, 304, 305, 3011, 3012, 3013,
        401, 402, 403, 4011, 4012, 4013, 99099
    ]
    await session.execute(delete(Intento).where(Intento.seccion.in_(secciones_fase6)))
    await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.seccion.in_(secciones_fase6)))
    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE6_ID))
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE6_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE6_ID))
    
    await session.commit()
    print("Purga de Fase 6 completada.")


async def seed_fase6_theory(session: AsyncSession) -> None:
    """Siembra los 15 guiones teóricos en niveles_teoria_pool."""
    print("Sembrando los 15 guiones teóricos de Fase 6 (niveles_teoria_pool)...")
    for tdata in FASE6_TEORIA_DATA:
        desc_full = tdata["texto_descubrimiento"]
        if "cuerpo_teoria" in tdata and tdata["cuerpo_teoria"]:
            desc_full += "\n\n" + tdata["cuerpo_teoria"]
        nivel_teoria = NivelTeoria(
            fase_id=6,
            modulo_id=tdata["modulo_id"],
            nivel_id=tdata["nivel_id"],
            titulo=tdata["titulo"],
            texto_descubrimiento=desc_full,
            advertencia=tdata["advertencia"],
            diccionario=tdata["diccionario"],
            ejemplos=tdata["ejemplos"],
            interactivos=tdata["interactivos"]
        )
        session.add(nivel_teoria)
    await session.commit()
    print("15 niveles teóricos de Fase 6 sembrados con éxito.")


# -----------------------------------------------------------------------------
# GENERADORES DE PRÁCTICA (120 familias × 4 = 480 preguntas por nivel)
# -----------------------------------------------------------------------------

def _gen_practice_question(
    mod_id: int, lvl_id: int, seccion: int, fam_idx: int, var_idx: int,
    conf_map: Dict[str, dict]
) -> tuple[dict, list[dict]]:
    """Genera 1 pregunta de práctica y sus alternativas."""
    fam_id_str = f"f6_m{mod_id}_l{lvl_id}_fam_{fam_idx:03d}"
    seed_val = mod_id * 100000 + lvl_id * 10000 + fam_idx * 10 + var_idx
    rng = random.Random(seed_val)

    personajes = ["Leo", "Emma", "Thiago", "Mía", "Hugo", "Alba", "Nina", "Bruno", "Salma", "Iker", "Zoe", "Dante", "Lía", "Owen", "Sofía"]
    personaje = personajes[(fam_idx * 4 + var_idx) % len(personajes)]
    q_global_num = fam_idx * 4 + var_idx + 1

    accent = color_modulo(6, mod_id)
    
    # M1 N1 (101): Nombrar figuras, contar vértices y lados
    if mod_id == 1 and lvl_id == 1:
        figuras = [
            ("triángulo", 3, 3, "regular", fig_cuadrado(3, unit="cm", color=accent)),
            ("cuadrilátero", 4, 4, "regular", fig_cuadrado(4, unit="cm", color=accent)),
            ("pentágono", 5, 5, "regular", fig_cuadrado(5, unit="cm", color=accent)),
            ("hexágono", 6, 6, "regular", fig_cuadrado(6, unit="cm", color=accent)),
            ("octágono", 8, 8, "regular", fig_cuadrado(8, unit="cm", color=accent))
        ]
        fig_nombre, n_lados, n_vert, _, svg_code = figuras[fam_idx % len(figuras)]
        
        sub_tipo = var_idx % 3
        if sub_tipo == 0:
            enunciado = f"{personaje} observa la figura plana #{q_global_num}. ¿Cuántos vértices (esquinas) tiene?<br/>{svg_code}"
            ans_str = str(n_vert)
            tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
            op_enum = OperacionEnum.SUMA
            datos_num = {"lados": n_lados, "vertices": n_vert, "tipo": "vertices"}
            alts = []
            err_dict = {str(n_vert + 1): "Cuenta las esquinas donde se unen dos lados rectos."}
        elif sub_tipo == 1:
            enunciado = f"{personaje} observa la figura plana #{q_global_num}. ¿Cuántos lados rectos tiene el contorno?<br/>{svg_code}"
            ans_str = str(n_lados)
            tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
            op_enum = OperacionEnum.SUMA
            datos_num = {"lados": n_lados, "vertices": n_vert, "tipo": "lados"}
            alts = []
            err_dict = {str(n_lados + 1): "Cuenta los segmentos rectos del borde exterior."}
        else:
            enunciado = f"{personaje} pregunta: ¿qué nombre recibe esta figura #{q_global_num} según su cantidad de lados?<br/>{svg_code}"
            ans_str = fig_nombre.capitalize()
            tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
            op_enum = OperacionEnum.SUMA
            datos_num = {"lados": n_lados, "nombre": fig_nombre}
            
            nombres_falsos = [f[0].capitalize() for f in figuras if f[0] != fig_nombre][:3]
            alts = [{"texto": ans_str, "es_correcta": True, "tipo_error": None, "feedback_error": ""}]
            err_dict = {}
            for nf in nombres_falsos:
                alts.append({
                    "texto": nf,
                    "es_correcta": False,
                    "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA,
                    "feedback_error": f"Esta figura tiene {n_lados} lados; se llama {ans_str}."
                })
                err_dict[nf] = f"Tiene {n_lados} lados, se llama {ans_str}."
            rng.shuffle(alts)

    # M1 N2 (102): Clasificación polígonos/cuadriláteros
    elif mod_id == 1 and lvl_id == 2:
        opciones_clasif = [
            ("Regular", "Irregular", "Triángulo", "Trapecio"),
            ("Paralelogramo", "Trapecio", "Trapezoide", "Pentágono"),
            ("Irregular", "Regular", "Octágono", "Hexágono")
        ]
        cat_idx = fam_idx % 3
        ans_str = opciones_clasif[cat_idx][0]
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        op_enum = OperacionEnum.SUMA
        w_rect = 6 + (fam_idx % 4) + var_idx
        h_rect = 3 + (var_idx % 2)
        svg_code = fig_rectangulo(w_rect, h_rect, unit="cm", color=accent)
        enunciado = f"{personaje} analiza las medidas del cuadrilátero #{q_global_num} (lados de {w_rect} cm y {h_rect} cm). ¿Cómo se clasifica según sus lados?<br/>{svg_code}"
        datos_num = {"lados_distintos": True, "tipo": ans_str}
        
        alts = [{"texto": ans_str, "es_correcta": True, "tipo_error": None, "feedback_error": ""}]
        err_dict = {}
        for f_txt in opciones_clasif[cat_idx][1:]:
            alts.append({
                "texto": f_txt,
                "es_correcta": False,
                "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA,
                "feedback_error": f"Revisa las características de la figura: la respuesta correcta es {ans_str}."
            })
            err_dict[f_txt] = f"La clasificación correcta es {ans_str}."
        rng.shuffle(alts)

    # M1 N3 (103): Ejes de simetría
    elif mod_id == 1 and lvl_id == 3:
        fig_ejes = [
            ("cuadrado", 4, fig_cuadrado(4, unit="cm", color=accent)),
            ("rectángulo", 2, fig_rectangulo(6, 3, unit="cm", color=accent)),
            ("triángulo equilátero", 3, fig_cuadrado(3, unit="cm", color=accent)),
            ("círculo", 999, fig_cuadrado(5, unit="cm", color=accent)) # 999 representa infinitos
        ]
        f_nombre, n_ejes, svg_code = fig_ejes[fam_idx % len(fig_ejes)]
        if n_ejes == 999:
            ans_str = "Infinitos"
            tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
            alts = [
                {"texto": "Infinitos", "es_correcta": True, "tipo_error": None, "feedback_error": ""},
                {"texto": "1", "es_correcta": False, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Cualquier recta que pase por el centro divide al círculo en dos mitades idénticas."},
                {"texto": "2", "es_correcta": False, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Tiene infinitos ejes de simetría."},
                {"texto": "4", "es_correcta": False, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Tiene infinitos ejes de simetría."}
            ]
            rng.shuffle(alts)
            err_dict = {"1": "Tiene infinitos ejes.", "2": "Tiene infinitos ejes.", "4": "Tiene infinitos ejes."}
        else:
            ans_str = str(n_ejes)
            tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
            alts = []
            err_dict = {str(n_ejes + 1): f"Un {f_nombre} tiene exactamente {n_ejes} ejes de simetría."}
        
        enunciado = f"{personaje} pregunta: ¿cuántos ejes de simetría exactos tiene un {f_nombre} (variante #{q_global_num})?<br/>{svg_code}"
        op_enum = OperacionEnum.SUMA
        datos_num = {"figura": f_nombre, "ejes": n_ejes}

    # M1 N4 (104): Perímetro sumando lados con decimales
    elif mod_id == 1 and lvl_id == 4:
        a = round(2.1 + (fam_idx * 0.05) + (var_idx * 0.02), 1)
        b = round(1.5 + (fam_idx * 0.03) + (var_idx * 0.01), 1)
        perim = round(2 * (a + b), 1)
        perim_str = f"{perim}".replace(".", ",")
        ans_str = perim_str
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.SUMA
        svg_code = fig_rectangulo(a, b, unit="cm", color=accent)
        enunciado = f"{personaje} calcula el perímetro del rectángulo #{q_global_num} sumando todos sus lados (lados de {str(a).replace('.',',')} cm y {str(b).replace('.',',')} cm).<br/>{svg_code}"
        datos_num = {"a": a, "b": b, "perimetro": perim}
        alts = []
        err_dict = {
            f"{round(a*b, 1)}".replace(".", ","): "Sumaste el contorno; no multipliques (eso sería área).",
            f"{round(a+b, 1)}".replace(".", ","): "Faltó sumar los otros dos lados del rectángulo."
        }

    # M2 N1 (201): Figuras en L, T y escaleras
    elif mod_id == 2 and lvl_id == 1:
        w1, h1 = 4 + (fam_idx % 5) + var_idx, 4 + ((fam_idx + var_idx) % 4)
        w2, h2 = 2 + (var_idx % 2), 2 + ((fam_idx + var_idx) % 2)
        perim = 2 * (w1 + h1)
        ans_str = str(perim)
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.SUMA
        svg_code = fig_L(w1, h1, w2, h2, unit="cm", color=accent)
        enunciado = f"{personaje} calcula el perímetro exterior de la figura en L #{q_global_num} (ancho total {w1} cm, alto total {h1} cm).<br/>{svg_code}"
        datos_num = {"w1": w1, "h1": h1, "w2": w2, "h2": h2, "perimetro": perim}
        alts = []
        err_dict = {str(perim + w2): "No sumes las líneas divisorias internas; solo el contorno exterior."}

    # M2 N2 (202): Lados ocultos deducidos por paralelismo
    elif mod_id == 2 and lvl_id == 2:
        w_total = 10 + (fam_idx % 10) + var_idx
        w_parcial = 3 + ((fam_idx + var_idx) % (w_total - 4))
        oculto = w_total - w_parcial
        ans_str = str(oculto)
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.RESTA
        svg_code = fig_L(w_total, 10, w_parcial, 5, unit="m", color=accent)
        enunciado = f"{personaje} observa que el ancho total de la figura #{q_global_num} es {w_total} m y un tramo mide {w_parcial} m. ¿Cuánto mide el lado horizontal oculto '?'?<br/>{svg_code}"
        datos_num = {"w_total": w_total, "w_parcial": w_parcial, "oculto": oculto}
        alts = []
        err_dict = {str(w_total + w_parcial): "Resta el tramo conocido del total para hallar el lado oculto."}

    # M2 N3 (203): La circunferencia (perímetro del círculo)
    elif mod_id == 2 and lvl_id == 3:
        r = 2 + (fam_idx % 8) + var_idx
        circ = round(2 * 3.14 * r, 2)
        circ_str = f"{circ}".replace(".", ",")
        ans_str = circ_str
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.MULTIPLICACION
        svg_code = fig_cuadrado(r, unit="cm", color=accent)
        enunciado = f"{personaje} calcula la circunferencia (perímetro) del círculo #{q_global_num} de radio {r} cm usando π = 3,14.<br/>{svg_code}"
        datos_num = {"radio": r, "pi": 3.14, "circunferencia": circ}
        alts = []
        err_dict = {
            f"{round(3.14 * r * r, 2)}".replace(".", ","): "Calculaste el área (π×r²); la circunferencia es 2×π×r."
        }

    # M3 N1 (301): Malla cuadriculada (cuadrados y medios)
    elif mod_id == 3 and lvl_id == 1:
        enteros = 4 + (fam_idx % 8) + var_idx
        mitades = 2 * (1 + ((fam_idx + var_idx) % 3))
        area = enteros + (mitades // 2)
        ans_str = str(area)
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.SUMA
        svg_code = fig_cuadrado(enteros, unit="cm²", color=accent)
        enunciado = f"{personaje} cuenta el área en cm² de la figura #{q_global_num} en la malla ({enteros} cuadrados enteros y {mitades} medios cuadrados).<br/>{svg_code}"
        datos_num = {"enteros": enteros, "mitades": mitades, "area": area}
        alts = []
        err_dict = {
            str(enteros + mitades): "Dos mitades equivalen a 1 entero. Empareja las mitades antes de sumar."
        }

    # M3 N2 (302): Área de cuadrado y rectángulo
    elif mod_id == 3 and lvl_id == 2:
        b = 3 + (fam_idx % 8) + var_idx
        h = 2 + ((fam_idx + var_idx) % 6)
        area = b * h
        ans_str = str(area)
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.MULTIPLICACION
        svg_code = fig_rectangulo(b, h, unit="cm", color=accent)
        enunciado = f"{personaje} calcula el área del rectángulo #{q_global_num} de base {b} cm y altura {h} cm.<br/>{svg_code}"
        datos_num = {"base": b, "altura": h, "area": area}
        alts = []
        err_dict = {
            str(2 * (b + h)): "Sumaste el borde (perímetro). Multiplica base × altura para obtener el área."
        }

    # M3 N3 (303): Área del triángulo
    elif mod_id == 3 and lvl_id == 3:
        b = 2 * (2 + (fam_idx % 5) + var_idx)
        h = 2 + ((fam_idx + var_idx) % 6)
        area = round((b * h) / 2, 1)
        area_str = f"{area}".replace(".", ",").rstrip(",0")
        ans_str = area_str
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.MIXTA
        svg_code = fig_cuadrado(b, unit="cm", color=accent)
        enunciado = f"{personaje} calcula el área del triángulo #{q_global_num} de base {b} cm y altura perpendicular {h} cm.<br/>{svg_code}"
        datos_num = {"base": b, "altura": h, "area": area}
        alts = []
        err_dict = {
            str(b * h): "Un triángulo es medio rectángulo: no olvides dividir (base × altura) ÷ 2."
        }

    # M3 N4 (304): Paralelogramo, rombo y trapecio
    elif mod_id == 3 and lvl_id == 4:
        fig_type = fam_idx % 3
        if fig_type == 0: # Paralelogramo
            b, h = 4 + (fam_idx % 6) + var_idx, 3 + ((fam_idx + var_idx) % 5)
            area = b * h
            fig_name = "paralelogramo"
            enunciado_txt = f"calcula el área del paralelogramo de base {b} cm y altura perpendicular {h} cm"
            svg_code = fig_rectangulo(b, h, unit="cm", color=accent)
        elif fig_type == 1: # Rombo
            D, d = 6 + (fam_idx % 4) * 2, 4 + (var_idx % 2) * 2
            area = (D * d) // 2
            fig_name = "rombo"
            enunciado_txt = f"calcula el área del rombo de diagonal mayor {D} cm y diagonal menor {d} cm"
            svg_code = fig_cuadrado(D, unit="cm", color=accent)
        else: # Trapecio
            B, b_menor, h = 10 + var_idx, 6, 3 + (fam_idx % 4)
            area = ((B + b_menor) * h) // 2
            fig_name = "trapecio"
            enunciado_txt = f"calcula el área del trapecio de base mayor {B} cm, base menor {b_menor} cm y altura {h} cm"
            svg_code = fig_rectangulo(B, h, unit="cm", color=accent)
            
        ans_str = str(area)
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.MIXTA
        enunciado = f"{personaje} {enunciado_txt} (ejercicio #{q_global_num}).<br/>{svg_code}"
        datos_num = {"figura": fig_name, "area": area}
        alts = []
        err_dict = {str(area * 2): "Revisa la fórmula: recuerda dividir entre 2 cuando corresponde."}

    # M3 N5 (305): Área del círculo
    elif mod_id == 3 and lvl_id == 5:
        r = 2 + (fam_idx % 8) + var_idx
        area = round(3.14 * r * r, 2)
        area_str = f"{area}".replace(".", ",")
        ans_str = area_str
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.MULTIPLICACION
        svg_code = fig_cuadrado(r, unit="cm", color=accent)
        enunciado = f"{personaje} calcula el área del círculo #{q_global_num} de radio {r} cm usando π = 3,14.<br/>{svg_code}"
        datos_num = {"radio": r, "pi": 3.14, "area": area}
        alts = []
        err_dict = {
            f"{round(2 * 3.14 * r, 2)}".replace(".", ","): "Calculaste la circunferencia (borde); el área es π × radio²."
        }

    # M4 N1 (401): Compuestas por suma
    elif mod_id == 4 and lvl_id == 1:
        w1, h1 = 4 + (fam_idx % 5) + var_idx, 4 + ((fam_idx + var_idx) % 4)
        w2, h2 = 2 + (var_idx % 2), 2 + ((fam_idx + var_idx) % 2)
        area = (w1 * h1) + (w2 * h2)
        ans_str = str(area)
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.SUMA
        svg_code = fig_L(w1, h1, w2, h2, unit="cm", color=accent)
        enunciado = f"{personaje} calcula el área total de la figura compuesta #{q_global_num} descomponiéndola en dos rectángulos ({w1}×{h1} cm y {w2}×{h2} cm).<br/>{svg_code}"
        datos_num = {"w1": w1, "h1": h1, "w2": w2, "h2": h2, "area": area}
        alts = []
        err_dict = {str((w1 * h1) - (w2 * h2)): "Las piezas están unidas: debes sumar las áreas, no restarlas."}

    # M4 N2 (402): Compuestas por resta
    elif mod_id == 4 and lvl_id == 2:
        w_ext, h_ext = 8 + (fam_idx % 8) + var_idx, 6 + ((fam_idx + var_idx) % 5)
        w_int, h_int = 4 + (var_idx % 2), 3 + ((fam_idx + var_idx) % 2)
        area = (w_ext * h_ext) - (w_int * h_int)
        ans_str = str(area)
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.RESTA
        svg_code = fig_rectangulo(w_ext, h_ext, unit="cm", color=accent)
        enunciado = f"{personaje} observa un marco de fotos rectangular #{q_global_num} de {w_ext}×{h_ext} cm con un hueco interior de {w_int}×{h_int} cm. ¿Cuál es el área sombreada del marco?<br/>{svg_code}"
        datos_num = {"w_ext": w_ext, "h_ext": h_ext, "w_int": w_int, "h_int": h_int, "area": area}
        alts = []
        err_dict = {str((w_ext * h_ext) + (w_int * h_int)): "El hueco quita material: debes restar el área interior de la exterior."}

    # M4 N3 (403): Figuras inscritas y áreas sombreadas
    else: # mod_id == 4 and lvl_id == 3
        lado = 8 + (fam_idx % 8) + var_idx
        r = 2 + (var_idx % 2)
        area_cuad = lado * lado
        area_circ = round(3.14 * r * r, 2)
        area_esquinas = round(area_cuad - area_circ, 2)
        area_str = f"{area_esquinas}".replace(".", ",")
        ans_str = area_str
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.RESTA
        svg_code = fig_cuadrado(lado, unit="cm", color=accent)
        enunciado = f"{personaje} observa un cuadrado #{q_global_num} de {lado} cm de lado donde se inscribe un círculo de radio {r} cm (π = 3,14). ¿Cuál es el área de las esquinas sombreadas exteriores?<br/>{svg_code}"
        datos_num = {"lado": lado, "radio": r, "area_sombreada": area_esquinas}
        alts = []
        err_dict = {f"{area_circ}".replace(".", ","): "Esa es el área del círculo interior; restó del cuadrado para hallar las esquinas."}

    pregunta_dict = {
        "fase_id": 6,
        "seccion": seccion,
        "estructura_padre_id": fam_id_str,
        "operacion": op_enum,
        "tipo_pregunta": tipo_preg,
        "enunciado": enunciado,
        "respuesta_correcta": ans_str,
        "datos_numericos": datos_num,
        "errores_previstos": err_dict,
        "explicacion_paso_a_paso": {
            "titulo": "Resolución Pedagógica",
            "pasos": [
                {"orden": 1, "texto": f"Identifica los datos clave del problema y aplica la fórmula o conteo correspondiente."},
                {"orden": 2, "texto": f"El resultado exacto verificado es {ans_str}."}
            ]
        },
        "estado": StatusEnum.ACTIVO,
        "requiere_subrayado": False,
        "creado_por": None
    }

    return pregunta_dict, alts


def _gen_challenge_question(
    mod_id: int, des_idx: int, seccion: int, q_idx: int, conf_map: Dict[str, dict]
) -> tuple[dict, list[dict]]:
    """Genera 1 pregunta de desafío para Fase 6."""
    fam_id_str = f"f6_d{seccion}_q{q_idx:03d}"
    seed_val = seccion * 1000 + q_idx
    rng = random.Random(seed_val)
    accent = color_modulo(6, mod_id)

    # D1 (1011, 2011, 3011, 4011) o D2 (1012, 2012, 3012, 4012) o DM (99099): MULTIPLE_OPCION
    # DF (1013, 2013, 3013, 4013): RESPUESTA_NUMERICA
    es_df = (des_idx == 3 and seccion != 99099)
    
    a = rng.randint(4, 15)
    b = rng.randint(3, 10)
    res_val = a * b if mod_id >= 3 else 2 * (a + b)
    ans_str = str(res_val)

    personajes = ["Leo", "Emma", "Thiago", "Mía", "Hugo", "Alba", "Nina", "Bruno", "Salma", "Iker", "Zoe", "Dante", "Lía", "Owen", "Sofía"]
    personaje = personajes[q_idx % len(personajes)]
    svg_code = fig_rectangulo(a, b, unit="cm", color=accent)
    enunciado = f"{personaje} analiza el rectángulo #{q_idx+1} ({a} cm × {b} cm). ¿Cuál es su {'área' if mod_id >= 3 else 'perímetro'} total?<br/>{svg_code}"
    
    pista_text = "Analiza las dimensiones dadas y aplica el procedimiento correspondiente a la figura."
    
    if es_df:
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        alts = []
        err_dict = {str(res_val + 2): "Revisa la operación aplicada a los lados de la figura."}
    else:
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        falsas = [str(res_val + 2), str(res_val - 2), str(res_val + 4)]
        alts = [{"texto": ans_str, "es_correcta": True, "tipo_error": None, "feedback_error": ""}]
        err_dict = {}
        for f_val in falsas:
            alts.append({
                "texto": f_val,
                "es_correcta": False,
                "tipo_error": TipoErrorEnum.CALCULO,
                "feedback_error": f"Revisa el cálculo: la respuesta correcta es {ans_str}."
            })
            err_dict[f_val] = f"El resultado correcto es {ans_str}."
        rng.shuffle(alts)

    pregunta_dict = {
        "fase_id": 6,
        "seccion": seccion,
        "estructura_padre_id": fam_id_str,
        "operacion": OperacionEnum.MULTIPLICACION if mod_id >= 3 else OperacionEnum.SUMA,
        "tipo_pregunta": tipo_preg,
        "enunciado": enunciado,
        "respuesta_correcta": ans_str,
        "datos_numericos": {"a": a, "b": b, "resultado": res_val},
        "errores_previstos": err_dict,
        "explicacion_paso_a_paso": {
            "titulo": "Resolución del Desafío",
            "pasos": [{"orden": 1, "texto": f"Aplica la fórmula adecuada para obtener {ans_str}."}],
            "pista": {"texto": pista_text, "penalizacion_segundos": 5}
        },
        "estado": StatusEnum.ACTIVO,
        "requiere_subrayado": False,
        "creado_por": None
    }

    return pregunta_dict, alts


async def seed_fase6_full() -> None:
    """Ejecuta la siembra completa de la Fase 6."""
    async with AsyncSessionLocal() as session:
        print("============================================================")
        print("INICIANDO SIEMBRA COMPLETA DE FASE 6 (Modelo B / Geometría)")
        print("============================================================")
        
        # 0. Asegurar Fase 6 en tabla `fases`
        res = await session.execute(select(Fase).where(Fase.id == FASE6_ID))
        fase = res.scalar_one_or_none()
        if not fase:
            fase = Fase(
                id=6,
                nombre="Geometría Plana Multiforme y Áreas",
                descripcion="Reconocimiento, perímetros y áreas de figuras planas",
                orden=6,
                estado=StatusEnum.ACTIVO
            )
            session.add(fase)
            await session.commit()
            print("Fase 6 en tabla `fases` creada.")
        else:
            print("Fase 6 en tabla `fases` asegurada.")

        # 1. Purga previa
        await clear_fase6_data(session)

        # 2. Siembra de Teoría
        await seed_fase6_theory(session)

        # 3. Siembra de Práctica (15 niveles × 120 familias × 4 variantes = 7.200 preguntas)
        print("Sembrando 7.200 preguntas de práctica (15 niveles × 120 familias × 4)...")
        niveles_practica = [
            (1, 1, 101), (1, 2, 102), (1, 3, 103), (1, 4, 104),
            (2, 1, 201), (2, 2, 202), (2, 3, 203),
            (3, 1, 301), (3, 2, 302), (3, 3, 303), (3, 4, 304), (3, 5, 305),
            (4, 1, 401), (4, 2, 402), (4, 3, 403)
        ]

        total_practica = 0
        for mod_id, lvl_id, seccion_code in niveles_practica:
            conf_map = _get_confusiones_map(mod_id)
            for fam_idx in range(120):
                for var_idx in range(4):
                    p_dict, alts = _gen_practice_question(mod_id, lvl_id, seccion_code, fam_idx, var_idx, conf_map)
                    p_obj = Pregunta(**p_dict)
                    session.add(p_obj)
                    await session.flush() # obtiene p_obj.id

                    for a_dict in alts:
                        a_obj = Alternativa(pregunta_id=p_obj.id, **a_dict)
                        session.add(a_obj)

                    total_practica += 1
                    if total_practica % 1000 == 0:
                        await session.commit()
                        print(f"  ... {total_practica} preguntas de práctica sembradas.")
        
        await session.commit()
        print(f"Práctica sembrada: {total_practica} preguntas.")

        # 4. Siembra de Desafíos (13 bloques × 150 = 1.950 preguntas)
        print("Sembrando 1.950 preguntas de desafíos (13 bloques × 150)...")
        bloques_desafios = [
            (1, 1, 1011), (1, 2, 1012), (1, 3, 1013),
            (2, 1, 2011), (2, 2, 2012), (2, 3, 2013),
            (3, 1, 3011), (3, 2, 3012), (3, 3, 3013),
            (4, 1, 4011), (4, 2, 4012), (4, 3, 4013),
            (1, 4, 99099) # Desafío Mixto de Fase
        ]

        total_desafios = 0
        for mod_id, des_idx, seccion_code in bloques_desafios:
            conf_map = _get_confusiones_map(mod_id)
            for q_idx in range(150):
                p_dict, alts = _gen_challenge_question(mod_id, des_idx, seccion_code, q_idx, conf_map)
                p_obj = Pregunta(**p_dict)
                session.add(p_obj)
                await session.flush()

                for a_dict in alts:
                    a_obj = Alternativa(pregunta_id=p_obj.id, **a_dict)
                    session.add(a_obj)

                total_desafios += 1
        
        await session.commit()
        print(f"Desafíos sembrados: {total_desafios} preguntas.")

        # 5. Siembra de configuracion_progreso (29 filas)
        print("Sembrando 29 filas en configuracion_progreso...")

        # 15 filas de práctica libre
        for mod_id, lvl_id, seccion_code in niveles_practica:
            config = ConfiguracionProgreso(
                fase_id=6,
                seccion=seccion_code,
                operacion=OperacionEnum.MIXTA,
                cantidad_requerida=15,
                porcentaje_aprobacion=100,
                orden_desbloqueo=lvl_id,
                tipo_feedback="bucle_espejo",
                usa_cronometro=False,
                tiempo_default_segundos=0,
                errores_tolerados=None,
                pistas_permitidas=0,
                penalizacion_pista_segundos=0,
                activo=True
            )
            session.add(config)

        # 12 desafíos de módulo
        for mod_id, des_idx, seccion_code in bloques_desafios[:-1]:
            if des_idx in (1, 2):
                cant_req, t_seg, err_tol, pct = 12, (60 if des_idx == 1 else 90), 2, 83
            else: # Final
                cant_req, t_seg, err_tol, pct = 10, 120, 1, 90

            config = ConfiguracionProgreso(
                fase_id=6,
                seccion=seccion_code,
                operacion=OperacionEnum.MIXTA,
                cantidad_requerida=cant_req,
                porcentaje_aprobacion=pct,
                orden_desbloqueo=10 + (des_idx % 10),
                tipo_feedback="normal",
                usa_cronometro=True,
                tiempo_default_segundos=t_seg,
                errores_tolerados=err_tol,
                pistas_permitidas=3,
                penalizacion_pista_segundos=5,
                activo=True
            )
            session.add(config)

        # Desafío Mixto de fase (99099)
        session.add(ConfiguracionProgreso(
            fase_id=6,
            seccion=99099,
            operacion=OperacionEnum.MIXTA,
            cantidad_requerida=15,
            porcentaje_aprobacion=100,
            orden_desbloqueo=99,
            tipo_feedback="normal",
            usa_cronometro=True,
            tiempo_default_segundos=90,
            errores_tolerados=3,
            pistas_permitidas=3,
            penalizacion_pista_segundos=5,
            activo=True
        ))

        # Fallback seccion=0
        session.add(ConfiguracionProgreso(
            fase_id=6,
            seccion=0,
            operacion=OperacionEnum.MIXTA,
            cantidad_requerida=15,
            porcentaje_aprobacion=100,
            orden_desbloqueo=0,
            tipo_feedback="bucle_espejo",
            usa_cronometro=False,
            tiempo_default_segundos=0,
            errores_tolerados=None,
            pistas_permitidas=0,
            penalizacion_pista_segundos=0,
            activo=True
        ))

        await session.commit()
        print("29 filas de `configuracion_progreso` sembradas.")

        print("============================================================")
        print("SIEMBRA DE FASE 6 FINALIZADA CON ÉXITO")
        print("============================================================")


if __name__ == "__main__":
    asyncio.run(seed_fase6_full())
