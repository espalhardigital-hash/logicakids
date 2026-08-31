"""
Seeder completo para la Fase 6: Geometría Plana Multiforme y Áreas.
Cumple strictly con las Secciones 8, 9 y 12 de docs/reestructuraciondefases.md.

Volumetría:
  - 4 Módulos, 15 Niveles de Teoría en niveles_teoria_pool.
  - 15 niveles de práctica × 120 familias × 4 variantes contextuales = 7.200 preguntas.
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
from app.core.progression import PRACTICE_REQUIRED_CORRECT_ANSWERS
from app.utils.svg_figuras import (
    fig_rectangulo, fig_cuadrado, fig_L, fig_T, fig_malla,
    fig_poligono_regular, fig_triangulo, fig_circulo, fig_paralelogramo,
    fig_rombo, fig_trapecio, fig_compuesta_suma, fig_compuesta_hueco,
    fig_inscrita,
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
            ("triángulo", 3, 3, fig_poligono_regular(3, color=accent)),
            ("cuadrilátero", 4, 4, fig_poligono_regular(4, color=accent)),
            ("pentágono", 5, 5, fig_poligono_regular(5, color=accent)),
            ("hexágono", 6, 6, fig_poligono_regular(6, color=accent)),
            ("heptágono", 7, 7, fig_poligono_regular(7, color=accent)),
            ("octágono", 8, 8, fig_poligono_regular(8, color=accent))
        ]
        fig_idx = fam_idx % len(figuras)
        sub_tipo = (fam_idx // len(figuras)) % 3
        
        fig_nombre, n_lados, n_vert, svg_code = figuras[fig_idx]
        
        if sub_tipo == 0:
            enunciado = f"Observa la figura plana. ¿Cuántos vértices (esquinas) tiene?<br/>{svg_code}"
            ans_str = str(n_vert)
            tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
            op_enum = OperacionEnum.SUMA
            datos_num = {"lados": n_lados, "vertices": n_vert, "tipo": "vertices"}
            alts = []
            err_dict = {str(n_vert + 1): "Cuenta las esquinas donde se unen dos lados rectos."}
        elif sub_tipo == 1:
            enunciado = f"Observa la figura plana. ¿Cuántos lados rectos tiene el contorno?<br/>{svg_code}"
            ans_str = str(n_lados)
            tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
            op_enum = OperacionEnum.SUMA
            datos_num = {"lados": n_lados, "vertices": n_vert, "tipo": "lados"}
            alts = []
            err_dict = {str(n_lados + 1): "Cuenta los segmentos rectos del borde exterior."}
        else:
            enunciado = f"¿Qué nombre recibe esta figura según su cantidad de lados?<br/>{svg_code}"
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

    # M1 N2 (102): Clasificación de polígonos — 7 figuras × 3 perspectivas = 21 preguntas únicas
    elif mod_id == 1 and lvl_id == 2:
        figuras_clasif = [
            ("cuadrado", True, fig_cuadrado(6, unit="cm", color=accent)),
            ("rectángulo", False, fig_rectangulo(8, 5, unit="cm", color=accent)),
            ("rombo", False, fig_rombo(8, 6, unit="cm", color=accent)),
            ("paralelogramo", False, fig_paralelogramo(9, 5, unit="cm", color=accent)),
            ("trapecio", False, fig_trapecio(10, 6, 5, unit="cm", color=accent)),
            ("pentágono regular", True, fig_poligono_regular(5, color=accent)),
            ("hexágono regular", True, fig_poligono_regular(6, color=accent)),
        ]
        fig_idx = fam_idx % len(figuras_clasif)
        sub_tipo = (fam_idx // len(figuras_clasif)) % 3

        nombre, es_regular, svg_code = figuras_clasif[fig_idx]
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        op_enum = OperacionEnum.SUMA

        todos_nombres = [f[0].capitalize() for f in figuras_clasif]

        if sub_tipo == 0:
            enunciado = f"Observa la figura. ¿Qué nombre recibe según sus propiedades?<br/>{svg_code}"
            ans_str = nombre.capitalize()
            nombres_falsos = [n for n in todos_nombres if n != ans_str][:3]
            datos_num = {"figura": nombre, "tipo": "nombre"}
        elif sub_tipo == 1:
            enunciado = f"Observa la figura. ¿Es un polígono regular o irregular?<br/>{svg_code}"
            ans_str = "Regular" if es_regular else "Irregular"
            nombres_falsos = ["Irregular", "Cóncavo", "Abierto"] if es_regular else ["Regular", "Cóncavo", "Abierto"]
            datos_num = {"figura": nombre, "tipo": "regularidad", "es_regular": es_regular}
        else:
            es_cuadrilatero = nombre in ("cuadrado", "rectángulo", "rombo", "paralelogramo", "trapecio")
            enunciado = f"Observa la figura. ¿Es un cuadrilátero (figura de 4 lados)?<br/>{svg_code}"
            ans_str = "Sí" if es_cuadrilatero else "No"
            nombres_falsos = ["No", "Tiene 3 lados", "Tiene más de 4"] if es_cuadrilatero else ["Sí", "Tiene 4 lados", "Es un cuadrado"]
            datos_num = {"figura": nombre, "tipo": "cuadrilatero", "es_cuadrilatero": es_cuadrilatero}

        alts = [{"texto": ans_str, "es_correcta": True, "tipo_error": None, "feedback_error": ""}]
        err_dict = {}
        for nf in nombres_falsos:
            alts.append({
                "texto": nf,
                "es_correcta": False,
                "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA,
                "feedback_error": f"La respuesta correcta es {ans_str}."
            })
            err_dict[nf] = f"La respuesta correcta es {ans_str}."
        rng.shuffle(alts)

    # M1 N3 (103): Ejes de simetría — 9 figuras × 2 perspectivas = 18 preguntas únicas
    elif mod_id == 1 and lvl_id == 3:
        fig_ejes = [
            ("cuadrado", 4, fig_cuadrado(5, unit="cm", color=accent)),
            ("rectángulo", 2, fig_rectangulo(7, 4, unit="cm", color=accent)),
            ("triángulo equilátero", 3, fig_poligono_regular(3, color=accent)),
            ("hexágono regular", 6, fig_poligono_regular(6, color=accent)),
            ("pentágono regular", 5, fig_poligono_regular(5, color=accent)),
            ("rombo", 2, fig_rombo(8, 6, unit="cm", color=accent)),
            ("triángulo isósceles", 1, fig_triangulo(4, 8, unit="cm", color=accent)),
            ("círculo", 999, fig_circulo(radio=5, unit="cm", color=accent, mostrar="radio")),
            ("triángulo escaleno", 0, fig_triangulo(9, 3, unit="cm", color=accent)),
        ]
        fig_idx = fam_idx % len(fig_ejes)
        sub_tipo = (fam_idx // len(fig_ejes)) % 2

        f_nombre, n_ejes, svg_code = fig_ejes[fig_idx]
        op_enum = OperacionEnum.SUMA
        datos_num = {"figura": f_nombre, "ejes": n_ejes}

        if sub_tipo == 0:
            # ¿Cuántos ejes de simetría tiene?
            enunciado = f"¿Cuántos ejes de simetría tiene esta figura ({f_nombre})?<br/>{svg_code}"
            if n_ejes == 999:
                ans_str = "Infinitos"
                tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
                alts = [
                    {"texto": "Infinitos", "es_correcta": True, "tipo_error": None, "feedback_error": ""},
                    {"texto": "1", "es_correcta": False, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "Cualquier recta que pase por el centro divide al círculo en dos mitades idénticas."},
                    {"texto": "4", "es_correcta": False, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "El círculo tiene infinitos ejes de simetría."},
                    {"texto": "8", "es_correcta": False, "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA, "feedback_error": "El círculo tiene infinitos ejes de simetría."}
                ]
                rng.shuffle(alts)
                err_dict = {"1": "Tiene infinitos ejes.", "4": "Tiene infinitos ejes.", "8": "Tiene infinitos ejes."}
            else:
                ans_str = str(n_ejes)
                tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
                alts = []
                err_dict = {str(n_ejes + 1): f"Un {f_nombre} tiene exactamente {n_ejes} eje(s) de simetría."}
        else:
            # ¿Tiene al menos un eje de simetría?
            enunciado = f"¿Tiene al menos un eje de simetría esta figura ({f_nombre})?<br/>{svg_code}"
            tiene = n_ejes > 0 or n_ejes == 999
            ans_str = "Sí" if tiene else "No"
            tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
            if tiene:
                falsas = ["No", "No se puede determinar", "Solo si es regular"]
            else:
                falsas = ["Sí, tiene 1", "Sí, tiene 2", "No se puede determinar"]
            alts = [{"texto": ans_str, "es_correcta": True, "tipo_error": None, "feedback_error": ""}]
            for nf in falsas:
                alts.append({
                    "texto": nf,
                    "es_correcta": False,
                    "tipo_error": TipoErrorEnum.OPERACION_INCORRECTA,
                    "feedback_error": f"Un {f_nombre} {'sí' if tiene else 'no'} tiene eje de simetría."
                })
            err_dict = {nf: f"La respuesta correcta es {ans_str}." for nf in falsas}
            rng.shuffle(alts)

    # M1 N4 (104): Perímetro con decimales — 25 preguntas únicas (20 rectángulos + 5 cuadrados)
    elif mod_id == 1 and lvl_id == 4:
        rect_dims = [
            (3.5, 2.0), (4.2, 3.1), (5.0, 2.5), (6.3, 4.0), (7.1, 3.5),
            (8.0, 5.5), (4.8, 2.3), (5.5, 3.2), (6.0, 4.5), (7.5, 2.8),
            (3.0, 1.5), (4.0, 2.0), (5.2, 3.8), (6.5, 4.2), (7.0, 5.0),
            (8.5, 3.0), (9.0, 4.5), (3.8, 2.2), (4.5, 3.5), (5.8, 4.0),
        ]
        cuad_dims = [3.5, 4.0, 5.5, 6.0, 7.5]

        if fam_idx < len(rect_dims):
            a, b = rect_dims[fam_idx]
            perim = round(2 * (a + b), 1)
            svg_code = fig_rectangulo(a, b, unit="cm", color=accent)
            enunciado = f"Calcula el perímetro de este rectángulo.<br/>{svg_code}"
        else:
            lado = cuad_dims[fam_idx - len(rect_dims)]
            a, b = lado, lado
            perim = round(4 * lado, 1)
            svg_code = fig_cuadrado(lado, unit="cm", color=accent)
            enunciado = f"Calcula el perímetro de este cuadrado.<br/>{svg_code}"

        perim_str = f"{perim}".replace(".", ",")
        ans_str = perim_str
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.SUMA
        datos_num = {"a": a, "b": b, "perimetro": perim}
        alts = []
        err_dict = {
            f"{round(a * b, 1)}".replace(".", ","): "Multiplicaste los lados (eso da el área); para el perímetro, suma los 4 lados.",
            f"{round(a + b, 1)}".replace(".", ","): "Faltó sumar los otros dos lados: el perímetro es 2 × (largo + ancho)."
        }

    # M2 N1 (201): Figuras en L, T y escaleras
    elif mod_id == 2 and lvl_id == 1:
        w1, h1 = 4 + (fam_idx % 5) + var_idx, 4 + ((fam_idx + var_idx) % 4)
        w2, h2 = 2 + (var_idx % 2), 2 + ((fam_idx + var_idx) % 2)
        # La figura L incluye la extensión horizontal `w2`: su borde exterior
        # es 2 × (w1 + w2 + h1), no el perímetro del rectángulo principal.
        perim = 2 * (w1 + w2 + h1)
        ans_str = str(perim)
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.SUMA
        svg_code = fig_L(w1, h1, w2, h2, unit="cm", color=accent)
        enunciado = f"{personaje} calcula el perímetro exterior de la figura en L #{q_global_num}: el tramo horizontal principal mide {w1} cm, la extensión mide {w2} cm y el alto total mide {h1} cm. No cuentes líneas internas.<br/>{svg_code}"
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
        svg_code = fig_L(oculto, 10, w_parcial, 5, unit="m", color=accent, ocultar_lado=0)
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
        svg_code = fig_circulo(radio=r, unit="cm", color=accent, mostrar="radio")
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
        slots = enteros + mitades
        cols = 5
        rows = (slots + cols - 1) // cols
        celdas = [(index % cols, index // cols) for index in range(enteros)]
        medias = [((enteros + index) % cols, (enteros + index) // cols, "BL" if index % 2 == 0 else "TR") for index in range(mitades)]
        svg_code = fig_malla(celdas, medias, cols=cols, rows=rows, unit="cm", color=accent)
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
        svg_code = fig_triangulo(b, h, unit="cm", color=accent)
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
            svg_code = fig_paralelogramo(b, h, unit="cm", color=accent)
        elif fig_type == 1: # Rombo
            D, d = 6 + (fam_idx % 4) * 2, 4 + (var_idx % 2) * 2
            area = (D * d) // 2
            fig_name = "rombo"
            enunciado_txt = f"calcula el área del rombo de diagonal mayor {D} cm y diagonal menor {d} cm"
            svg_code = fig_rombo(D, d, unit="cm", color=accent)
        else: # Trapecio
            B, b_menor, h = 10 + var_idx, 6, 3 + (fam_idx % 4)
            area = ((B + b_menor) * h) // 2
            fig_name = "trapecio"
            enunciado_txt = f"calcula el área del trapecio de base mayor {B} cm, base menor {b_menor} cm y altura {h} cm"
            svg_code = fig_trapecio(B, b_menor, h, unit="cm", color=accent)
            
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
        svg_code = fig_circulo(radio=r, unit="cm", color=accent, mostrar="radio")
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
        svg_code = fig_compuesta_suma((w1, h1), (w2, h2), unit="cm", color=accent)
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
        svg_code = fig_compuesta_hueco((w_ext, h_ext), (w_int, h_int), unit="cm", color=accent)
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
        svg_code = fig_inscrita("circulo_en_cuadrado", "circulo", {"lado": lado, "radio": r}, unit="cm", color=accent)
        enunciado = f"{personaje} observa un cuadrado #{q_global_num} de {lado} cm de lado donde se inscribe un círculo de radio {r} cm (π = 3,14). ¿Cuál es el área de las esquinas sombreadas exteriores?<br/>{svg_code}"
        datos_num = {"lado": lado, "radio": r, "area_sombreada": area_esquinas}
        alts = []
        err_dict = {f"{area_circ}".replace(".", ","): "Esa es el área del círculo interior; restó del cuadrado para hallar las esquinas."}

    # Contrato explícito para auditar la familia y su dependencia visual.
    if isinstance(datos_num, dict):
        datos_num["plantilla_id"] = fam_id_str
        datos_num["requiere_figura"] = "<svg" in enunciado.lower()
        datos_num["tipo_visual"] = "inline_svg" if datos_num["requiere_figura"] else "textual"

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
    """Genera 1 pregunta de desafío para Fase 6 de forma pedagógicamente pertinente y variada."""
    fam_id_str = f"f6_d{seccion}_q{q_idx:03d}"
    seed_val = seccion * 1000 + q_idx
    rng = random.Random(seed_val)
    accent = color_modulo(6, mod_id)

    # ─────────────────────────────────────────────────────────────────────────
    # MÓDULO 1: Perímetro y borde (1011: Polígonos, 1012: Simetría, 1013: Perímetro Numérico)
    # ─────────────────────────────────────────────────────────────────────────
    if seccion == 1011:
        # D1: Reconocimiento y propiedades de polígonos (18 preguntas)
        poligonos = [
            ("triángulo", 3, 3, fig_poligono_regular(3, color=accent)),
            ("cuadrilátero", 4, 4, fig_poligono_regular(4, color=accent)),
            ("pentágono", 5, 5, fig_poligono_regular(5, color=accent)),
            ("hexágono", 6, 6, fig_poligono_regular(6, color=accent)),
            ("heptágono", 7, 7, fig_poligono_regular(7, color=accent)),
            ("octágono", 8, 8, fig_poligono_regular(8, color=accent)),
        ]
        sub = q_idx // len(poligonos)
        p_nombre, n_lados, n_vert, svg_code = poligonos[q_idx % len(poligonos)]
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        op_enum = OperacionEnum.SUMA

        if sub == 0:
            enunciado = f"¿Cuántos vértices tiene este polígono?<br/>{svg_code}"
            ans_str = str(n_vert)
            falsas = [str(n_vert + 1), str(n_vert + 2), str(max(2, n_vert - 1))]
        elif sub == 1:
            enunciado = f"¿Cuántos lados rectos delimitan este polígono?<br/>{svg_code}"
            ans_str = str(n_lados)
            falsas = [str(n_lados + 1), str(n_lados + 2), str(max(2, n_lados - 1))]
        else:
            enunciado = f"¿Qué nombre recibe este polígono regular según su número de lados?<br/>{svg_code}"
            ans_str = p_nombre.capitalize()
            falsas = [p[0].capitalize() for p in poligonos if p[0] != p_nombre][:3]

        datos_num = {"lados": n_lados, "vertices": n_vert, "nombre": p_nombre}

    elif seccion == 1012:
        # D2: Ejes de simetría y clasificación (18 preguntas)
        fig_ejes = [
            ("cuadrado", 4, fig_cuadrado(5, unit="cm", color=accent)),
            ("rectángulo", 2, fig_rectangulo(7, 4, unit="cm", color=accent)),
            ("rombo", 2, fig_rombo(8, 6, unit="cm", color=accent)),
            ("triángulo equilátero", 3, fig_poligono_regular(3, color=accent)),
            ("hexágono regular", 6, fig_poligono_regular(6, color=accent)),
            ("pentágono regular", 5, fig_poligono_regular(5, color=accent)),
            ("triángulo isósceles", 1, fig_triangulo(4, 8, unit="cm", color=accent)),
            ("triángulo escaleno", 0, fig_triangulo(9, 3, unit="cm", color=accent)),
            ("círculo", 999, fig_circulo(radio=5, unit="cm", color=accent, mostrar="radio")),
        ]
        sub = q_idx // len(fig_ejes)
        f_nombre, n_ejes, svg_code = fig_ejes[q_idx % len(fig_ejes)]
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        op_enum = OperacionEnum.SUMA

        if sub == 0:
            enunciado = f"¿Cuántos ejes de simetría tiene esta figura ({f_nombre})?<br/>{svg_code}"
            if n_ejes == 999:
                ans_str = "Infinitos"
                falsas = ["1", "2", "4"]
            else:
                ans_str = str(n_ejes)
                falsas = [str(n_ejes + 1), str(n_ejes + 2), str(max(0, n_ejes - 1))]
        else:
            enunciado = f"¿Tiene esta figura ({f_nombre}) al menos un eje de simetría?<br/>{svg_code}"
            tiene = (n_ejes > 0 or n_ejes == 999)
            ans_str = "Sí" if tiene else "No"
            falsas = ["No", "No se puede determinar", "Solo si es regular"] if tiene else ["Sí, tiene 1", "Sí, tiene 2", "No se puede determinar"]

        datos_num = {"figura": f_nombre, "ejes": n_ejes}

    elif seccion == 1013:
        # DF: Perímetro numérico directo (20 preguntas)
        rect_dims = [
            (6, 4), (8, 5), (7, 3), (9, 6), (10, 4),
            (12, 5), (11, 7), (8, 6), (14, 8), (15, 9)
        ]
        cuad_dims = [4, 6, 7, 9, 12]
        poly_dims = [
            ("triángulo equilátero", 3, 6),
            ("pentágono regular", 5, 5),
            ("hexágono regular", 6, 4),
            ("octágono regular", 8, 3),
            ("heptágono regular", 7, 4),
        ]

        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.SUMA

        if q_idx < len(rect_dims):
            a, b = rect_dims[q_idx]
            perim = 2 * (a + b)
            svg_code = fig_rectangulo(a, b, unit="cm", color=accent)
            enunciado = f"Calcula el perímetro total de este rectángulo.<br/>{svg_code}"
            datos_num = {"a": a, "b": b, "perimetro": perim}
        elif q_idx < len(rect_dims) + len(cuad_dims):
            lado = cuad_dims[q_idx - len(rect_dims)]
            perim = 4 * lado
            svg_code = fig_cuadrado(lado, unit="cm", color=accent)
            enunciado = f"Calcula el perímetro total de este cuadrado.<br/>{svg_code}"
            datos_num = {"lado": lado, "perimetro": perim}
        else:
            p_nom, n_l, l_val = poly_dims[q_idx - len(rect_dims) - len(cuad_dims)]
            perim = n_l * l_val
            svg_code = fig_poligono_regular(n_l, color=accent)
            enunciado = f"Calcula el perímetro de este {p_nom} si cada lado mide {l_val} cm.<br/>{svg_code}"
            datos_num = {"figura": p_nom, "lados": n_l, "lado_cm": l_val, "perimetro": perim}

        ans_str = str(perim)
        falsas = []

    # ─────────────────────────────────────────────────────────────────────────
    # MÓDULO 2: Área en malla y perímetro compuesto (2011: L y T, 2012: Lados Ocultos, 2013: Circunferencia DF)
    # ─────────────────────────────────────────────────────────────────────────
    elif seccion == 2011:
        # D1: Perímetro exterior de figuras en L y T (18 preguntas)
        l_dims = [
            (5, 6, 3, 2), (6, 7, 4, 3), (4, 5, 2, 2), (7, 8, 3, 4), (5, 5, 2, 2),
            (8, 9, 4, 3), (6, 8, 3, 4), (4, 6, 3, 2), (7, 7, 3, 3), (5, 8, 4, 3)
        ]
        t_dims = [
            (8, 3, 4, 5), (10, 4, 4, 6), (9, 3, 3, 5), (12, 4, 4, 6),
            (8, 2, 4, 4), (10, 3, 4, 5), (7, 2, 3, 4), (11, 3, 5, 6)
        ]
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        op_enum = OperacionEnum.SUMA

        if q_idx < len(l_dims):
            w1, h1, w2, h2 = l_dims[q_idx]
            perim = 2 * (w1 + w2 + h1)
            svg_code = fig_L(w1, h1, w2, h2, unit="cm", color=accent)
            enunciado = f"Calcula el perímetro exterior de esta figura en L.<br/>{svg_code}"
            datos_num = {"w1": w1, "h1": h1, "w2": w2, "h2": h2, "perimetro": perim}
        else:
            ala, h_ala, tallo, h_tallo = t_dims[q_idx - len(l_dims)]
            perim = 2 * ala + 2 * (h_ala + h_tallo)
            svg_code = fig_T(ala, h_ala, tallo, h_tallo, unit="cm", color=accent)
            enunciado = f"Calcula el perímetro exterior de esta figura en T.<br/>{svg_code}"
            datos_num = {"ala": ala, "h_ala": h_ala, "tallo": tallo, "h_tallo": h_tallo, "perimetro": perim}

        ans_str = str(perim)
        falsas = [str(perim + 2), str(perim - 2), str(perim + 4)]

    elif seccion == 2012:
        # D2: Deducción de lados ocultos por paralelismo (18 preguntas)
        lados_data = [
            (10, 4, 8, 3), (12, 5, 9, 4), (14, 6, 10, 5), (9, 3, 7, 2), (15, 7, 11, 5),
            (11, 4, 8, 3), (13, 8, 9, 4), (16, 9, 12, 6), (8, 3, 6, 2), (10, 6, 7, 3),
            (12, 7, 8, 4), (14, 8, 10, 4), (15, 6, 9, 3), (11, 5, 7, 2), (13, 6, 8, 3),
            (16, 7, 11, 4), (9, 4, 6, 2), (12, 4, 8, 3)
        ]
        w_tot, w_par, h_tot, h_par = lados_data[q_idx % len(lados_data)]
        w2 = w_tot - w_par
        h2 = h_tot - h_par
        ans_str = str(w2)
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        op_enum = OperacionEnum.RESTA
        svg_code = fig_L(w_par, h_tot, w2, h2, unit="cm", color=accent, ocultar_lado=1)
        enunciado = f"Observa los lados paralelos de la figura. ¿Cuánto mide el lado horizontal señalado con '?'?<br/>{svg_code}"
        datos_num = {"w_total": w_tot, "w_parcial": w_par, "lado_oculto": w2}
        falsas = [str(w2 + 2), str(max(1, w2 - 2)), str(w2 + 1)]

    elif seccion == 2013:
        # DF: Circunferencia y perímetros combinados (20 preguntas)
        radios = [3, 4, 5, 6, 7, 8, 9, 10, 12, 15]
        l_dims_df = [
            (6, 8, 4, 3), (8, 10, 5, 4), (7, 9, 3, 3), (9, 11, 4, 5), (10, 12, 5, 4),
            (5, 7, 3, 2), (8, 8, 4, 3), (11, 13, 5, 6), (7, 10, 4, 4), (6, 9, 3, 3)
        ]
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.SUMA

        if q_idx < len(radios):
            r = radios[q_idx]
            circ = round(2 * 3.14 * r, 1)
            ans_str = f"{circ}".replace(".", ",")
            svg_code = fig_circulo(radio=r, unit="cm", color=accent)
            enunciado = f"Calcula la longitud de la circunferencia de radio {r} cm (usa π = 3,14).<br/>{svg_code}"
            datos_num = {"radio": r, "circunferencia": circ}
        else:
            w1, h1, w2, h2 = l_dims_df[q_idx - len(radios)]
            perim = 2 * (w1 + w2 + h1)
            ans_str = str(perim)
            svg_code = fig_L(w1, h1, w2, h2, unit="cm", color=accent)
            enunciado = f"Calcula el perímetro exterior total de esta figura en L.<br/>{svg_code}"
            datos_num = {"w1": w1, "h1": h1, "w2": w2, "h2": h2, "perimetro": perim}
        falsas = []

    # ─────────────────────────────────────────────────────────────────────────
    # MÓDULO 3: Figuras compuestas y áreas analíticas (3011: Malla/Triángulo, 3012: Rombo/Trapecio, 3013: DF Áreas)
    # ─────────────────────────────────────────────────────────────────────────
    elif seccion == 3011:
        # D1: Área en cuadrícula/malla y triángulos (18 preguntas)
        tri_dims = [
            (6, 4), (8, 5), (10, 6), (7, 4), (9, 6),
            (12, 5), (8, 3), (10, 4), (14, 6)
        ]
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        op_enum = OperacionEnum.MULTIPLICACION

        if q_idx < 9:
            # Malla con conteos de 3 a 11 celdas
            cols, rows = 5, 4
            num_llenas = 3 + q_idx
            celdas_llenas = [(i % cols, i // cols) for i in range(num_llenas)]
            medias = [(num_llenas % cols, num_llenas // cols, "TR"), ((num_llenas + 1) % cols, (num_llenas + 1) // cols, "BL")]
            area_u = num_llenas + 1 # 2 medias celdas = 1 entera
            ans_str = str(area_u)
            svg_code = fig_malla(celdas_llenas, medias, cols, rows, unit="u", color=accent)
            enunciado = f"Calcula el área total de la figura #{q_idx+1} sombreada en la cuadrícula (en u²).<br/>{svg_code}"
            datos_num = {"celdas_enteras": num_llenas, "medias": 2, "area": area_u}
            falsas = [str(area_u + 1), str(max(1, area_u - 1)), str(area_u + 2)]
        else:
            # Triángulo
            b, h = tri_dims[q_idx - 9]
            area = (b * h) // 2
            ans_str = str(area)
            svg_code = fig_triangulo(b, h, unit="cm", color=accent)
            enunciado = f"Calcula el área de este triángulo (base = {b} cm, altura = {h} cm).<br/>{svg_code}"
            datos_num = {"base": b, "altura": h, "area": area}
            falsas = [str(b * h), str(area + 2), str(max(1, area - 2))]

    elif seccion == 3012:
        # D2: Paralelogramo, rombo y trapecio (18 preguntas)
        paralelos = [(8, 5), (10, 6), (9, 4), (12, 5), (7, 6), (11, 4)]
        rombos = [(10, 6), (8, 4), (12, 8), (14, 6), (10, 8), (16, 8)]
        trapecios = [(10, 6, 4), (12, 8, 5), (9, 5, 4), (14, 8, 6), (11, 7, 5), (13, 7, 4)]

        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        op_enum = OperacionEnum.MULTIPLICACION

        if q_idx < 6:
            b, h = paralelos[q_idx]
            area = b * h
            ans_str = str(area)
            svg_code = fig_paralelogramo(b, h, unit="cm", color=accent)
            enunciado = f"Calcula el área de este paralelogramo (base = {b} cm, altura = {h} cm).<br/>{svg_code}"
            datos_num = {"base": b, "altura": h, "area": area}
            falsas = [str(area + 4), str(area - 4), str(area + 8)]
        elif q_idx < 12:
            d_may, d_men = rombos[q_idx - 6]
            area = (d_may * d_men) // 2
            ans_str = str(area)
            svg_code = fig_rombo(d_may, d_men, unit="cm", color=accent)
            enunciado = f"Calcula el área de este rombo (D = {d_may} cm, d = {d_men} cm).<br/>{svg_code}"
            datos_num = {"D": d_may, "d": d_men, "area": area}
            falsas = [str(d_may * d_men), str(area + 4), str(max(2, area - 4))]
        else:
            b_may, b_men, h = trapecios[q_idx - 12]
            area = ((b_may + b_men) * h) // 2
            ans_str = str(area)
            svg_code = fig_trapecio(b_may, b_men, h, unit="cm", color=accent)
            enunciado = f"Calcula el área de este trapecio (B = {b_may} cm, b = {b_men} cm, h = {h} cm).<br/>{svg_code}"
            datos_num = {"B": b_may, "b": b_men, "h": h, "area": area}
            falsas = [str((b_may + b_men) * h), str(area + 3), str(max(2, area - 3))]

    elif seccion == 3013:
        # DF: Cálculo exacto de áreas analíticas (20 preguntas numéricas)
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.MULTIPLICACION

        if q_idx < 5:
            tri = [(6, 4), (8, 6), (10, 5), (12, 4), (14, 5)][q_idx]
            area = (tri[0] * tri[1]) // 2
            svg_code = fig_triangulo(tri[0], tri[1], unit="cm", color=accent)
            enunciado = f"Calcula el área exacta de este triángulo.<br/>{svg_code}"
            datos_num = {"base": tri[0], "altura": tri[1], "area": area}
        elif q_idx < 10:
            par = [(7, 5), (9, 4), (10, 6), (11, 5), (12, 7)][q_idx - 5]
            area = par[0] * par[1]
            svg_code = fig_paralelogramo(par[0], par[1], unit="cm", color=accent)
            enunciado = f"Calcula el área exacta de este paralelogramo.<br/>{svg_code}"
            datos_num = {"base": par[0], "altura": par[1], "area": area}
        elif q_idx < 15:
            rom = [(10, 6), (12, 8), (14, 6), (16, 8), (8, 6)][q_idx - 10]
            area = (rom[0] * rom[1]) // 2
            svg_code = fig_rombo(rom[0], rom[1], unit="cm", color=accent)
            enunciado = f"Calcula el área exacta de este rombo.<br/>{svg_code}"
            datos_num = {"D": rom[0], "d": rom[1], "area": area}
        else:
            trap = [(10, 6, 4), (12, 8, 5), (14, 6, 5), (16, 10, 6), (11, 7, 4)][q_idx - 15]
            area = ((trap[0] + trap[1]) * trap[2]) // 2
            svg_code = fig_trapecio(trap[0], trap[1], trap[2], unit="cm", color=accent)
            enunciado = f"Calcula el área exacta de este trapecio.<br/>{svg_code}"
            datos_num = {"B": trap[0], "b": trap[1], "h": trap[2], "area": area}

        ans_str = str(area)
        falsas = []

    # ─────────────────────────────────────────────────────────────────────────
    # MÓDULO 4: Figuras compuestas y áreas sombreadas (4011: Suma, 4012: Resta/Hueco, 4013: DF Inscritas)
    # ─────────────────────────────────────────────────────────────────────────
    elif seccion == 4011:
        # D1: Figuras compuestas por adición (18 preguntas)
        sumas = [
            ((6, 4), (4, 3)), ((7, 5), (5, 3)), ((8, 4), (4, 2)), ((9, 5), (6, 3)),
            ((5, 4), (3, 2)), ((10, 6), (6, 4)), ((8, 5), (5, 2)), ((7, 4), (4, 3)),
            ((6, 5), (3, 3)), ((9, 6), (5, 4)), ((8, 6), (4, 3)), ((10, 5), (6, 3)),
            ((7, 3), (4, 2)), ((8, 3), (5, 2)), ((11, 6), (6, 4)), ((6, 3), (3, 2)),
            ((9, 4), (5, 3)), ((10, 4), (4, 2))
        ]
        r_a, r_b = sumas[q_idx % len(sumas)]
        area = (r_a[0] * r_a[1]) + (r_b[0] * r_b[1])
        ans_str = str(area)
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        op_enum = OperacionEnum.SUMA
        svg_code = fig_compuesta_suma(r_a, r_b, unit="cm", color=accent)
        enunciado = f"Calcula el área total de la figura sumando las regiones A ({r_a[0]}×{r_a[1]} cm) y B ({r_b[0]}×{r_b[1]} cm).<br/>{svg_code}"
        datos_num = {"rect_a": r_a, "rect_b": r_b, "area": area}
        falsas = [str(area + 6), str(area - 6), str(area + 10)]

    elif seccion == 4012:
        # D2: Marcos y figuras con hueco interior por sustracción (18 preguntas)
        huecos = [
            ((10, 8), (4, 3)), ((12, 9), (5, 4)), ((11, 7), (4, 3)), ((14, 10), (6, 4)),
            ((9, 7), (3, 2)), ((15, 10), (7, 5)), ((10, 7), (4, 2)), ((12, 8), (5, 3)),
            ((13, 9), (6, 4)), ((11, 8), (4, 3)), ((14, 8), (6, 3)), ((10, 6), (4, 2)),
            ((12, 10), (5, 5)), ((15, 9), (7, 4)), ((13, 8), (5, 3)), ((9, 6), (3, 2)),
            ((14, 9), (6, 4)), ((11, 9), (4, 4))
        ]
        ext, inc = huecos[q_idx % len(huecos)]
        area = (ext[0] * ext[1]) - (inc[0] * inc[1])
        ans_str = str(area)
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        op_enum = OperacionEnum.RESTA
        svg_code = fig_compuesta_hueco(ext, inc, unit="cm", color=accent)
        enunciado = f"Calcula el área sombreada del marco restando el hueco interior ({ext[0]}×{ext[1]} cm con hueco de {inc[0]}×{inc[1]} cm).<br/>{svg_code}"
        datos_num = {"exterior": ext, "interior": inc, "area": area}
        falsas = [str((ext[0] * ext[1]) + (inc[0] * inc[1])), str(area + 6), str(max(4, area - 6))]

    elif seccion == 4013:
        # DF: Figuras inscritas y áreas sombreadas exteriores (20 preguntas numéricas únicas)
        lados_cuad = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
        tri_rects = [
            (8, 4), (10, 5), (12, 6), (14, 7), (16, 8),
            (9, 4), (11, 5), (13, 6), (15, 7), (18, 8)
        ]
        tipo_preg = TipoPreguntaEnum.RESPUESTA_NUMERICA
        op_enum = OperacionEnum.RESTA

        if q_idx < len(lados_cuad):
            lado = lados_cuad[q_idx]
            r = lado / 2
            area_cuad = lado * lado
            area_circ = round(3.14 * r * r, 2)
            area_somb = round(area_cuad - area_circ, 2)
            ans_str = f"{area_somb}".replace(".", ",")
            svg_code = fig_inscrita("circulo_en_cuadrado", "circulo", {"lado": lado, "radio": r}, unit="cm", color=accent)
            enunciado = f"Calcula el área de las esquinas sombreadas exteriores (cuadrado de {lado} cm con círculo inscrito de radio {int(r) if r.is_integer() else r} cm, π = 3,14).<br/>{svg_code}"
            datos_num = {"lado": lado, "radio": r, "area_sombreada": area_somb}
        else:
            bw, bh = tri_rects[q_idx - len(lados_cuad)]
            area_rec = bw * bh
            area_tri = (bw * bh) / 2
            area_somb = area_rec - area_tri
            ans_str = str(int(area_somb))
            svg_code = fig_inscrita("triangulo_en_rectangulo", "triangulo", {"base": bw, "altura": bh}, unit="cm", color=accent)
            enunciado = f"Calcula el área de la zona sombreada exterior al triángulo inscrito (rectángulo de {bw}×{bh} cm).<br/>{svg_code}"
            datos_num = {"base": bw, "altura": bh, "area_sombreada": area_somb}

        falsas = []

    # ─────────────────────────────────────────────────────────────────────────
    # DESAFÍO MAESTRO DE FASE 6 (99099: Integrador de los 4 módulos, 24 preguntas)
    # ─────────────────────────────────────────────────────────────────────────
    else: # seccion == 99099
        tipo_preg = TipoPreguntaEnum.MULTIPLE_OPCION
        if q_idx < 6:
            # M1: Propiedades y simetría
            fig_maestro = [
                ("hexágono regular", 6, fig_poligono_regular(6, color=accent)),
                ("pentágono regular", 5, fig_poligono_regular(5, color=accent)),
                ("octágono regular", 8, fig_poligono_regular(8, color=accent)),
                ("triángulo equilátero", 3, fig_poligono_regular(3, color=accent)),
                ("cuadrado", 4, fig_cuadrado(6, unit="cm", color=accent)),
                ("rombo", 2, fig_rombo(8, 6, unit="cm", color=accent)),
            ]
            f_nom, f_ejes, svg_code = fig_maestro[q_idx]
            ans_str = str(f_ejes)
            op_enum = OperacionEnum.SUMA
            enunciado = f"Desafío Maestro: ¿Cuántos ejes de simetría tiene un {f_nom}?<br/>{svg_code}"
            datos_num = {"figura": f_nom, "ejes": f_ejes}
            falsas = [str(f_ejes + 1), str(f_ejes + 2), str(max(0, f_ejes - 1))]
        elif q_idx < 12:
            # M2: Perímetro de compuestas en L
            w1, h1, w2, h2 = [(6, 7, 3, 3), (8, 9, 4, 3), (5, 6, 3, 2), (7, 8, 4, 3), (9, 10, 4, 4), (6, 8, 3, 3)][q_idx - 6]
            perim = 2 * (w1 + w2 + h1)
            ans_str = str(perim)
            op_enum = OperacionEnum.SUMA
            svg_code = fig_L(w1, h1, w2, h2, unit="cm", color=accent)
            enunciado = f"Desafío Maestro: Calcula el perímetro exterior de esta figura en L.<br/>{svg_code}"
            datos_num = {"w1": w1, "h1": h1, "w2": w2, "h2": h2, "perimetro": perim}
            falsas = [str(perim + 3), str(perim - 3), str(perim + 6)]
        elif q_idx < 18:
            # M3: Áreas de triángulos y trapecios
            if q_idx % 2 == 0:
                b, h = [(8, 5), (10, 6), (12, 5)][(q_idx - 12) // 2]
                area = (b * h) // 2
                svg_code = fig_triangulo(b, h, unit="cm", color=accent)
                enunciado = f"Desafío Maestro: Calcula el área de este triángulo (base = {b} cm, altura = {h} cm).<br/>{svg_code}"
                datos_num = {"base": b, "altura": h, "area": area}
            else:
                b_may, b_men, h = [(10, 6, 4), (12, 8, 5), (14, 8, 6)][(q_idx - 13) // 2]
                area = ((b_may + b_men) * h) // 2
                svg_code = fig_trapecio(b_may, b_men, h, unit="cm", color=accent)
                enunciado = f"Desafío Maestro: Calcula el área de este trapecio (B = {b_may} cm, b = {b_men} cm, h = {h} cm).<br/>{svg_code}"
                datos_num = {"B": b_may, "b": b_men, "h": h, "area": area}
            ans_str = str(area)
            op_enum = OperacionEnum.MULTIPLICACION
            falsas = [str(area + 4), str(area - 4), str(area + 8)]
        else:
            # M4: Áreas sombreadas con hueco
            ext, inc = [((12, 9), (5, 4)), ((14, 10), (6, 4)), ((11, 8), (4, 3)), ((15, 10), (7, 5)), ((13, 9), (5, 4)), ((16, 11), (7, 5))][q_idx - 18]
            area = (ext[0] * ext[1]) - (inc[0] * inc[1])
            ans_str = str(area)
            op_enum = OperacionEnum.RESTA
            svg_code = fig_compuesta_hueco(ext, inc, unit="cm", color=accent)
            enunciado = f"Desafío Maestro: Calcula el área sombreada del marco restando el hueco interior.<br/>{svg_code}"
            datos_num = {"exterior": ext, "interior": inc, "area": area}
            falsas = [str((ext[0] * ext[1]) + (inc[0] * inc[1])), str(area + 8), str(max(4, area - 8))]

    # ─────────────────────────────────────────────────────────────────────────
    # Generación de alternativas y contrato final
    # ─────────────────────────────────────────────────────────────────────────
    pista_text = "Analiza las dimensiones dadas y aplica el procedimiento correspondiente a la figura."
    
    if tipo_preg == TipoPreguntaEnum.RESPUESTA_NUMERICA:
        alts = []
        err_dict = {}
    else:
        alts = [{"texto": ans_str, "es_correcta": True, "tipo_error": None, "feedback_error": ""}]
        err_dict = {}
        # Asegurar exactamente 3 alternativas falsas únicas
        falsas_unicas = []
        for f in falsas:
            if f != ans_str and f not in falsas_unicas and len(falsas_unicas) < 3:
                falsas_unicas.append(f)
        while len(falsas_unicas) < 3:
            cand = str(int(ans_str) + len(falsas_unicas) + 2) if ans_str.isdigit() else f"Alternativa {len(falsas_unicas)+2}"
            if cand != ans_str and cand not in falsas_unicas:
                falsas_unicas.append(cand)
        for f_val in falsas_unicas:
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
        "operacion": op_enum,
        "tipo_pregunta": tipo_preg,
        "enunciado": enunciado,
        "respuesta_correcta": ans_str,
        "datos_numericos": {
            **datos_num,
            "plantilla_id": fam_id_str,
            "requiere_figura": True,
            "tipo_visual": "inline_svg",
        },
        "errores_previstos": err_dict,
        "explicacion_paso_a_paso": {
            "titulo": "Resolución del Desafío",
            "pasos": [{"orden": 1, "texto": f"Aplica la fórmula o procedimiento geométrico para obtener {ans_str}."}],
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

        # 3. Siembra de Práctica (M1: 82 preguntas únicas + 11 niveles × 480 = 5.362 preguntas)
        print("Sembrando preguntas de práctica...")
        niveles_practica = [
            (1, 1, 101), (1, 2, 102), (1, 3, 103), (1, 4, 104),
            (2, 1, 201), (2, 2, 202), (2, 3, 203),
            (3, 1, 301), (3, 2, 302), (3, 3, 303), (3, 4, 304), (3, 5, 305),
            (4, 1, 401), (4, 2, 402), (4, 3, 403)
        ]

        # Secciones de M1 con preguntas únicas (sin variantes redundantes)
        M1_UNIQUE_FAMS = {101: 18, 102: 21, 103: 18, 104: 25}

        total_practica = 0
        for mod_id, lvl_id, seccion_code in niveles_practica:
            conf_map = _get_confusiones_map(mod_id)
            num_fams = M1_UNIQUE_FAMS.get(seccion_code, 120)
            num_vars = 1 if seccion_code in M1_UNIQUE_FAMS else 4
            for fam_idx in range(num_fams):
                for var_idx in range(num_vars):
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

        # 4. Siembra de Desafíos (13 bloques = 248 preguntas únicas y pertinentes)
        print("Sembrando preguntas de desafíos...")
        bloques_desafios = [
            (1, 1, 1011), (1, 2, 1012), (1, 3, 1013),
            (2, 1, 2011), (2, 2, 2012), (2, 3, 2013),
            (3, 1, 3011), (3, 2, 3012), (3, 3, 3013),
            (4, 1, 4011), (4, 2, 4012), (4, 3, 4013),
            (1, 4, 99099) # Desafío Mixto de Fase
        ]

        CHALLENGE_COUNTS = {
            1011: 18, 1012: 18, 1013: 20,
            2011: 18, 2012: 18, 2013: 20,
            3011: 18, 3012: 18, 3013: 20,
            4011: 18, 4012: 18, 4013: 20,
            99099: 24,
        }

        total_desafios = 0
        for mod_id, des_idx, seccion_code in bloques_desafios:
            conf_map = _get_confusiones_map(mod_id)
            num_q = CHALLENGE_COUNTS.get(seccion_code, 18)
            for q_idx in range(num_q):
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
                cantidad_requerida=PRACTICE_REQUIRED_CORRECT_ANSWERS,
                porcentaje_aprobacion=100,
                orden_desbloqueo=lvl_id,
                tipo_feedback="feedback_bloqueado",
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
            cantidad_requerida=PRACTICE_REQUIRED_CORRECT_ANSWERS,
            porcentaje_aprobacion=100,
            orden_desbloqueo=0,
            tipo_feedback="feedback_bloqueado",
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
