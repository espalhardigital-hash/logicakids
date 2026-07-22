import asyncio
import random
from sqlalchemy import select, and_, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.db.session import AsyncSessionLocal
from app.models.sql_models import (
    Fase,
    Pregunta,
    Alternativa,
    ConfiguracionProgreso,
    StatusEnum,
    OperacionEnum,
    TipoPreguntaEnum,
    TipoErrorEnum,
    Intento,
    PoolAsignadoAlumno,
)
from app.fase2.models import NivelTeoria, IntentoPregunta, IntentoPaso
from app.fase5.theory_examples import obtener_ejemplos_expandidos_fase5
from app.fase5.svg_helpers import (
    svg_rect, svg_square, svg_triangle_equilateral,
    svg_rect_all_labels, svg_l_shape, svg_polygon_labeled,
    svg_shaded_rect, svg_grid_halves, svg_scale_bar, svg_rect_diagonal
)

from app.utils.graphics_generator import (
    generate_grid_shape_image,
    generate_clean_shape_image,
    generate_irregular_grid_shape_image,
    _generate_random_staircase,
    generate_rectilinear_shape_image,
    _build_step_shape
)
from app.core.storage import storage_service

FASE5_ID = 5

# --- DICCIONARIOS DE CONTEXTO FASE 5 ---
NOMBRES = ["Leo", "Emma", "Thiago", "Mia", "Hugo", "Alba",
           "Nina", "Bruno", "Salma", "Iker", "Zoe", "Dante", "Lía", "Owen"]
ESCENARIOS_P = ["patio", "jardín", "cuadro de pintura", "campo de fútbol",
                "corral", "huerta", "cancha de tenis", "terraza"]
ESCENARIOS_A = ["alfombra", "piscina", "mosaico", "pista de baile",
                "césped artificial", "manta de picnic", "tablero de ajedrez", "toldo"]
ESCENARIOS_E = ["mapa del tesoro", "plano de la ciudad", "maqueta escolar",
                "plano de un parque", "croquis de la casa"]

# Cache en memoria para reutilizar URLs de gráficos generados
_graphic_url_cache: Dict[str, str] = {}

async def clear_fase5_data(session: AsyncSession):
    print("Purging existing Fase 5 data for a clean overwrite...")
    result = await session.execute(select(Pregunta.id, Pregunta.datos_numericos).where(Pregunta.fase_id == FASE5_ID))
    rows = result.all()
    pregunta_ids_list = [r[0] for r in rows]
    
    urls_a_borrar = [
        r[1]["url"] for r in rows
        if r[1] and isinstance(r[1], dict) and r[1].get("url")
    ]
    for url in urls_a_borrar:
        await storage_service.delete_file(url)
    if urls_a_borrar:
        print(f"MinIO: {len(urls_a_borrar)} imágenes huérfanas eliminadas antes de re-sembrar.")
    
    if pregunta_ids_list:
        await session.execute(delete(Alternativa).where(Alternativa.pregunta_id.in_(pregunta_ids_list)))
        res_int_q = await session.execute(select(IntentoPregunta.id).where(IntentoPregunta.pregunta_id.in_(pregunta_ids_list)))
        int_q_ids = res_int_q.scalars().all()
        if int_q_ids:
            await session.execute(delete(IntentoPaso).where(IntentoPaso.intento_pregunta_id.in_(int_q_ids)))
            await session.execute(delete(IntentoPregunta).where(IntentoPregunta.id.in_(int_q_ids)))
            
        await session.execute(delete(Intento).where(Intento.pregunta_id.in_(pregunta_ids_list)))
        await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.pregunta_id.in_(pregunta_ids_list)))
        
    await session.execute(delete(Intento).where(Intento.fase_id == FASE5_ID))
    await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE5_ID))
    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE5_ID))
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE5_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE5_ID))
    await session.commit()
    print("Fase 5 data purged.")

async def seed_teoria_niveles(session: AsyncSession):
    print("Sembrando guión de textos (NivelTeoria) para Fase 5...")
    
    niveles_teoria = [
        # --- MÓDULO 1: Perímetro y Borde ---
        {
            "modulo_id": 1, "nivel_id": 1,
            "titulo": "Conteo directo de unidades lineales",
            "texto_descubrimiento": "¡Hola, exploradora del espacio! 🚀 ¿Sabías que las figuras geométricas tienen 'fronteras'? El perímetro es la suma de todo el borde exterior de una figura.\nImagínate a una pequeña hormiguita caminando justo por la línea más externa de tu dibujo. En este nivel, vas a contar cada rayita de la cuadrícula por la que camina la hormiguita para dar una vuelta completa. ¡Es muy fácil y divertido!",
            "diccionario": {"Perímetro": "Es la suma de las longitudes de todos los lados que forman el borde de una figura.", "Lado": "Cada una de las líneas que forman una figura plana.", "Contorno": "Línea que marca el límite exterior de una figura."},
            "advertencia": "¡Atención, pequeña detective! No vayas a contar las líneas que están adentro del dibujo. A la hormiguita solo le gusta caminar por el borde exterior.",
            "ejemplos": obtener_ejemplos_expandidos_fase5(1, 1),
            "interactivos": [
                {
                    "pregunta": "Un rectángulo tiene lados de 3 y 4 cm. ¿Cuál es su perímetro en cm?<br/>"
                                 "<svg width='260' height='220' viewBox='-15 -15 150 145' style='margin:10px auto; display:block; background:#111827; border:2px solid #E5E7EB; border-radius:12px;'>"
                                 "  <path d='M20,0 V120 M40,0 V120 M60,0 V120 M80,0 V120 M100,0 V120 M0,20 H120 M0,40 H120 M0,60 H120 M0,80 H120 M0,100 H120' stroke='#E5E7EB' stroke-width='1'/>"
                                 "  <rect x='30' y='20' width='60' height='80' fill='#E0F2FE' fill-opacity='0.8' stroke='#1E293B' stroke-width='2'/>"
                                 "  <text x='60' y='14' fill='#FFFFFF' font-size='16' font-weight='bold' text-anchor='middle'>3 cm</text>"
                                 "  <text x='18' y='64' fill='#FFFFFF' font-size='16' font-weight='bold' text-anchor='middle'>4 cm</text>"
                                 "</svg>",
                    "respuesta": "14",
                    "feedback_acierto": "¡Correcto! Sumamos 3 + 4 + 3 + 4 = 14.",
                    "feedback_error": "Recuerda sumar todos los bordes externos: 3+4+3+4."
                },
                {
                    "pregunta": "Un cuadrado tiene un lado que mide 5 cm. Su perímetro es:<br/>"
                                 "<svg width='260' height='220' viewBox='-20 -10 160 140' style='margin:10px auto; display:block; background:#111827; border:2px solid #E5E7EB; border-radius:12px;'>"
                                 "  <path d='M20,0 V120 M40,0 V120 M60,0 V120 M80,0 V120 M100,0 V120 M0,20 H120 M0,40 H120 M0,60 H120 M0,80 H120 M0,100 H120' stroke='#E5E7EB' stroke-width='1'/>"
                                 "  <rect x='10' y='10' width='100' height='100' fill='#E0F2FE' fill-opacity='0.8' stroke='#1E293B' stroke-width='2'/>"
                                 "  <text x='60' y='65' fill='#1E293B' font-size='14' font-weight='bold' text-anchor='middle'>Lado = 5</text>"
                                 "</svg>",
                    "respuesta": "20",
                    "feedback_acierto": "¡Excelente! Los cuatro lados miden 5, así que 5 x 4 = 20.",
                    "feedback_error": "Multiplica el lado por 4 porque un cuadrado tiene 4 lados iguales: 5x4."
                },
                {
                    "pregunta": "El perímetro de un triángulo equilátero con lado de 6 m es:<br/>"
                                 "<svg width='260' height='220' viewBox='-15 -10 150 135' style='margin:10px auto; display:block; background:#111827; border:2px solid #E5E7EB; border-radius:12px;'>"
                                 "  <polygon points='60,20 100,100 20,100' fill='#E0F2FE' fill-opacity='0.8' stroke='#1E293B' stroke-width='2'/>"
                                 "  <text x='60' y='122' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='middle'>6 m</text>"
                                 "  <text x='30' y='65' fill='#1E293B' font-size='18' font-weight='bold' text-anchor='middle'>6 m</text>"
                                 "  <text x='90' y='65' fill='#1E293B' font-size='18' font-weight='bold' text-anchor='middle'>6 m</text>"
                                 "</svg>",
                    "respuesta": "18",
                    "feedback_acierto": "¡Brillante! Sumamos los 3 lados: 6 + 6 + 6 = 18.",
                    "feedback_error": "Suma los tres lados del triángulo: 6+6+6."
                }
            ]
        },
        {
            "modulo_id": 1, "nivel_id": 2,
            "titulo": "Cálculo analítico de perímetros sumando magnitudes",
            "texto_descubrimiento": "¡Ahora vamos a ser ingenieras! 📐 A veces las figuras no están dibujadas sobre una cuadrícula de juego. En ese caso, ¡no podemos contar rayitas! Pero no te preocupes, porque las figuras nos revelan cuánto mide cada uno de sus lados.\nPara hallar el perímetro, solo debemos sumar los números de todos los lados de la figura. ¡Como una gran suma de equipo!",
            "diccionario": {"Lado (Arista)": "El segmento de línea que une dos esquinas de la figura.", "Polígono": "Figura geométrica plana compuesta por una secuencia finita de segmentos rectos.", "Cuadrilátero": "Polígono de cuatro lados."},
            "advertencia": "Asegúrate de sumar absolutamente TODOS los lados. Si dejas un lado olvidado en el camino, ¡el perímetro quedará incompleto!",
            "ejemplos": obtener_ejemplos_expandidos_fase5(1, 2),
            "interactivos": [
                {"pregunta": "Una figura tiene cuatro lados que miden: 2 cm, 3 cm, 2 cm y 3 cm. Perímetro:<br/>" + svg_rect_all_labels(3, 2, unit="cm"), "respuesta": "10", "feedback_acierto": "¡Correcto!", "feedback_error": "Suma: 2+3+2+3."},
                {"pregunta": "Un pentágono irregular tiene 5 lados y cada lado mide 1 m. Perímetro:<br/>" + svg_polygon_labeled([(10, 40), (20, 10), (30, 40), (25, 70), (15, 70)], [(15, 20, "1 m"), (25, 20, "1 m"), (35, 55, "1 m"), (20, 80, "1 m"), (5, 55, "1 m")], unit="m"), "respuesta": "5", "feedback_acierto": "¡Excelente!", "feedback_error": "Suma los cinco lados de 1: 1+1+1+1+1."},
                {"pregunta": "Un rectángulo mide 10 cm de largo y 5 cm de ancho. Perímetro:<br/>" + svg_rect(10, 5, unit="cm"), "respuesta": "30", "feedback_acierto": "¡Brillante!", "feedback_error": "Suma los cuatro lados: 10+5+10+5."}
            ]
        },
        {
            "modulo_id": 1, "nivel_id": 3,
            "titulo": "Conversión de unidades de longitud",
            "texto_descubrimiento": "Las medidas de longitud pueden usar diferentes 'apellidos' según qué tan grandes sean: milímetros (para hormiguitas), centímetros (para lápices), decímetros, metros (para ti) y kilómetros (para autos).\nPara comparar perímetros, necesitamos que todos usen el mismo apellido. ¡Aprenderemos a convertir estas unidades usando una escalera mágica!",
            "diccionario": {"1 metro (m)": "Equivale a 100 centímetros (cm)", "1 kilómetro (km)": "Equivale a 1000 metros (m)", "Unidad de longitud": "Cantidad estandarizada de longitud.", "Escalera de conversión": "Método visual para convertir unidades."},
            "advertencia": "Si vas a un paso más pequeño, multiplicas. Si vas a un paso más grande, divides. ¡Fíjate bien si subes o bajas en la escalera!",
            "ejemplos": obtener_ejemplos_expandidos_fase5(1, 3),
            "interactivos": [
                {"pregunta": "¿Cuántos centímetros hay en 3 metros?<br/>" + svg_rect(3, 1, unit="m"), "respuesta": "300", "feedback_acierto": "¡Correcto! 3 x 100 = 300 cm.", "feedback_error": "Multiplica los metros por 100."},
                {"pregunta": "¿Cuántos metros hay en 5 kilómetros?<br/>" + svg_rect(5, 1, unit="km"), "respuesta": "5000", "feedback_acierto": "¡Excelente! 5 x 1000 = 5000 m.", "feedback_error": "Multiplica los kilómetros por 1000."},
                {"pregunta": "¿Cuántos milímetros hay en 2 centímetros?<br/>" + svg_rect(2, 1, unit="cm"), "respuesta": "20", "feedback_acierto": "¡Brillante! 2 x 10 = 20 mm.", "feedback_error": "Multiplica los centímetros por 10."}
            ]
        },
        # --- MÓDULO 2: Área en Malha ---
        {
            "modulo_id": 2, "nivel_id": 1,
            "titulo": "Conteo analítico de unidades confinadas",
            "texto_descubrimiento": "El área es la medida de la superficie de una figura. Imagina que quieres cubrir el suelo de tu habitación con baldosas.\nEn una cuadrícula, el área nos dice cuántos cuadraditos completos caben adentro de una figura geométrica. Mientras el perímetro mide el borde, el área mide el interior relleno. ¡A contar baldosas!",
            "diccionario": {"Área": "La cantidad de espacio o cuadraditos que caben dentro del contorno de una figura.", "Unidad cuadrada": "Cuadrado cuyos lados miden 1 unidad.", "Base y altura": "Lados perpendiculares de un rectángulo."},
            "advertencia": "No te confundas con el perímetro. Aquí no medimos la frontera, medimos todo lo que está pintado adentro.",
            "ejemplos": obtener_ejemplos_expandidos_fase5(2, 1),
            "interactivos": [
                {"pregunta": "Si un cuadrado mide 4x4 cm, ¿cuál es su área en cm²?<br/>" + svg_shaded_rect(4, 4, unit="cm²"), "respuesta": "16", "feedback_acierto": "¡Correcto! 4 filas de 4 cuadraditos = 16.", "feedback_error": "Multiplica base por altura (4x4) o cuenta todos los cuadros."},
                {"pregunta": "Un rectángulo mide 5 cm de base y 2 cm de altura. Su área en cm² es:<br/>" + svg_shaded_rect(5, 2, unit="cm²"), "respuesta": "10", "feedback_acierto": "¡Excelente! 5 x 2 = 10.", "feedback_error": "Multiplica 5x2."},
                {"pregunta": "Si pinto 3 filas de 3 cuadros (de 1 cm² cada uno), ¿cuál es el área total?<br/>" + svg_shaded_rect(3, 3, unit="cm²"), "respuesta": "9", "feedback_acierto": "¡Brillante!", "feedback_error": "Multiplica 3x3."}
            ]
        },
        {
            "modulo_id": 2, "nivel_id": 2,
            "titulo": "Fusión de sectores triangulares",
            "texto_descubrimiento": "¡A veces las figuras tienen cortes inclinados! Si cortas un cuadrado en diagonal, obtienes dos mitades (triángulos iguales).\nLa regla mágica es: si juntas dos mitades triangulares iguales, ¡hacen exactamente un cuadrado entero! Es como armar un rompecabezas: 1/2 + 1/2 = 1. ¡Une las piezas para contar enteros!",
            "diccionario": {"Fusión de áreas": "Juntar dos mitades de cuadrado para formar una unidad cuadrada entera.", "Diagonal de un cuadrado": "Línea que une dos esquinas opuestas de un cuadrado.", "Triángulo rectángulo": "Triángulo con un ángulo de 90 grados."},
            "advertencia": "¡Cuidado al contar! Agrupa las mitades de dos en dos para formar nuevos enteros y no te quedes a la mitad.",
            "ejemplos": obtener_ejemplos_expandidos_fase5(2, 2),
            "interactivos": [
                {"pregunta": "Si tengo 4 cuadrados enteros de 1 cm² y 2 mitades. Área total en cm²:<br/>" + svg_grid_halves(4, 2, unit="cm²"), "respuesta": "5", "feedback_acierto": "¡Correcto! 4 enteros + 1 entero de las mitades = 5.", "feedback_error": "Las dos mitades forman 1 entero."},
                {"pregunta": "Figura con 0 enteros y 4 mitades de cm². Área en cm²:<br/>" + svg_grid_halves(0, 4, unit="cm²"), "respuesta": "2", "feedback_acierto": "¡Excelente! 4 mitades son 2 enteros.", "feedback_error": "4 mitades divididas entre 2 da 2 enteros."},
                {"pregunta": "Si tengo 10 enteros y 6 mitades, área total en cm²:<br/>" + svg_grid_halves(10, 6, unit="cm²"), "respuesta": "13", "feedback_acierto": "¡Brillante! 6 mitades son 3 enteros.", "feedback_error": "6 mitades son 3 enteros. Suma 10+3."}
            ]
        },
        {
            "modulo_id": 2, "nivel_id": 3,
            "titulo": "Estimación analítica de áreas irregulares",
            "texto_descubrimiento": "Las figuras en la naturaleza (como hojas de árboles o lagunas) son irregulares y no encajan perfecto en la cuadrícula.\nPara calcular su área en mallas densas, contamos todos los cuadrados que están completamente llenos y luego estimamos y sumamos las mitades o esquinas. ¡Una gran aventura de aproximación!",
            "diccionario": {"Área irregular": "Figura que no tiene lados rectos ni formas clásicas predefinidas.", "Aproximación": "Cálculo que no es exacto pero se acerca al valor real.", "Estimación": "Valor aproximado de una cantidad."},
            "advertencia": "Usa una estrategia ordenada: primero marca los enteros y luego combina las fracciones sobrantes.",
            "ejemplos": obtener_ejemplos_expandidos_fase5(2, 3),
            "interactivos": [
                {"pregunta": "¿Cuánto es 8 enteros más 8 mitades en cm²?<br/>" + svg_grid_halves(8, 8, unit="cm²"), "respuesta": "12", "feedback_acierto": "¡Correcto!", "feedback_error": "8 mitades son 4 enteros. 8 + 4 = 12."},
                {"pregunta": "¿Cuánto es 12 enteros más 2 mitades en cm²?<br/>" + svg_grid_halves(12, 2, unit="cm²"), "respuesta": "13", "feedback_acierto": "¡Excelente!", "feedback_error": "2 mitades son 1 entero. 12 + 1 = 13."},
                {"pregunta": "Si un polígono ocupa 5 enteros y 4 mitades, su área en cm² es:<br/>" + svg_grid_halves(5, 4, unit="cm²"), "respuesta": "7", "feedback_acierto": "¡Brillante!", "feedback_error": "4 mitades = 2. 5 + 2 = 7."}
            ]
        },
        # --- MÓDULO 3: Figuras Compuestas y Simetría ---
        {
            "modulo_id": 3, "nivel_id": 1,
            "titulo": "Descomposición estructural de polígonos",
            "texto_descubrimiento": "¡Las figuras compuestas son como castillos armados con bloques simples! Si tienes una figura en forma de 'L', de cruz o de casita, no hay fórmulas directas para ellas.\nPero si las dividimos con una línea imaginaria, podemos separarlas en rectángulos y cuadrados simples. Calculas el área de cada pieza y luego las sumas. ¡Divide y vencerás!",
            "diccionario": {"Descomponer": "Dividir una figura compleja en partes geométricas simples conocidas.", "Figura compuesta": "Figura formada por varias figuras simples.", "Superposición": "Poner una figura sobre otra."},
            "advertencia": "¡Cuidado al dividir! Las partes no deben superponerse (encimarse) ni debes dejar huecos sin contar.",
            "ejemplos": obtener_ejemplos_expandidos_fase5(3, 1),
            "interactivos": [
                {"pregunta": "Un rectángulo de 10 cm² y otro de 8 cm² pegados suman (en cm²):<br/>" + svg_l_shape(5, 2, 4, 2, unit="cm"), "respuesta": "18", "feedback_acierto": "¡Correcto!", "feedback_error": "Suma ambas áreas."},
                {"pregunta": "Figura T compuesta por un techo de 12 m² y una base de 4 m². Área total:<br/>" + svg_l_shape(6, 2, 2, 2, unit="m"), "respuesta": "16", "feedback_acierto": "¡Excelente!", "feedback_error": "Suma 12+4."},
                {"pregunta": "Una 'L' de 15 cm² en el alto y 5 cm² en el piso. Total:<br/>" + svg_l_shape(5, 3, 5, 1, unit="cm"), "respuesta": "20", "feedback_acierto": "¡Brillante!", "feedback_error": "Suma 15+5."}
            ]
        },
        {
            "modulo_id": 3, "nivel_id": 2,
            "titulo": "Análisis de conservación del área mediante Tangram",
            "texto_descubrimiento": "¡El Tangram es un juego mágico chino de 7 piezas! Puedes armar un gato, una casa, un pato o un barco.\nLo fabuloso es que, sin importar la forma que crees, si usas las mismas piezas, ¡el área total de la figura sigue siendo exactamente la misma! El área se conserva porque las piezas no cambian de tamaño al moverlas.",
            "diccionario": {"Conservación del área": "El área de un objeto no cambia cuando este cambia de forma o de posición.", "Tangram": "Juego de 7 piezas que forman un cuadrado.", "Congruencia": "Dos figuras son iguales en forma y tamaño."},
            "advertencia": "Aunque una figura parezca más grande por estar estirada, si usa las mismas piezas, su área sigue siendo igual. ¡No te dejes engañar por el ojo!",
            "ejemplos": obtener_ejemplos_expandidos_fase5(3, 2),
            "interactivos": [
                {"pregunta": "Si un triángulo de 3 cm² se rota, su nueva área es:<br/>" + svg_triangle_equilateral(3, unit="cm"), "respuesta": "3", "feedback_acierto": "¡Correcto! Rotar no cambia el área.", "feedback_error": "Rotar no cambia el área."},
                {"pregunta": "Corto un papel de 10 cm² en dos piezas. ¿Cuánto suman las dos piezas juntas?<br/>" + svg_rect(5, 2, unit="cm"), "respuesta": "10", "feedback_acierto": "¡Excelente! Siguen sumando lo mismo que al principio.", "feedback_error": "Suman lo mismo que el original."},
                {"pregunta": "Armo una casa con un Tangram de 16 cm². El área de la casa es:<br/>" + svg_square(4, unit="cm"), "respuesta": "16", "feedback_acierto": "¡Brillante!", "feedback_error": "El área se conserva al usar todas las piezas."}
            ]
        },
        {
            "modulo_id": 3, "nivel_id": 3,
            "titulo": "Cálculo analítico de áreas sombreadas",
            "texto_descubrimiento": "A veces nos piden el área de una zona pintada que tiene un hueco o agujero adentro (como una dona o un marco de fotos).\nPara resolver esto, usamos la resta geométrica: calculas el área de la figura exterior grande, calculas el área del hueco blanco interior, y las restas. ¡Le quitamos el agujero al total!",
            "diccionario": {"Resta geométrica": "Resta del área total menos el área del hueco blanco.", "Área sombreada": "Parte coloreada de una figura.", "Figura hueca": "Figura con una parte interior vacía."},
            "advertencia": "Asegúrate de calcular primero las dos áreas por separado antes de restarlas.",
            "ejemplos": obtener_ejemplos_expandidos_fase5(3, 3),
            "interactivos": [
                {"pregunta": "Área exterior 50 m², área interior en blanco 10 m². ¿Área pintada en m²?<br/>" + svg_rect(10, 5, unit="m"), "respuesta": "40", "feedback_acierto": "¡Correcto! 50 - 10 = 40.", "feedback_error": "Resta 50 - 10."},
                {"pregunta": "Caja de 100 cm² con agujero de 25 cm². Área restante:<br/>" + svg_square(10, unit="cm"), "respuesta": "75", "feedback_acierto": "¡Excelente!", "feedback_error": "Resta 100 - 25."},
                {"pregunta": "Pared de 20 m² con ventana de 4 m². ¿Área a pintar?<br/>" + svg_rect(5, 4, unit="m"), "respuesta": "16", "feedback_acierto": "¡Brillante!", "feedback_error": "Resta 20 - 4."}
            ]
        },
        {
            "modulo_id": 3, "nivel_id": 4,
            "titulo": "Identificación de Ejes de Simetría",
            "texto_descubrimiento": "¡La simetría es la magia del espejo! Un eje de simetría es una línea que divide una figura exactamente por la mitad.\nSi doblas la figura por esa línea, las dos mitades deben coincidir perfectamente, esquina con esquina. ¡Como tus manos al aplaudir o las alas de una mariposa!",
            "diccionario": {"Eje de simetría": "Línea imaginaria que divide una figura en dos partes iguales que son reflejos una de otra.", "Simetría axial": "Simetría respecto a un eje.", "Reflejo/Espejo": "Imagen que se forma al reflejarse en una superficie."},
            "advertencia": "Algunas figuras parecen simétricas, pero si las doblas a la mitad no coinciden. ¡Verifica el doblez en tu mente!",
            "ejemplos": obtener_ejemplos_expandidos_fase5(3, 4),
            "interactivos": [
                {"pregunta": "¿Cuántos ejes de simetría tiene un círculo (escribe: infinitos)?<br/>" + svg_square(4, unit="cm"), "respuesta": "infinitos", "feedback_acierto": "¡Correcto! El círculo es perfectamente simétrico en cualquier dirección.", "feedback_error": "El círculo es perfectamente simétrico en cualquier diámetro. Escribe 'infinitos'."},
                {"pregunta": "¿Cuántos ejes de simetría tiene un cuadrado perfecto?<br/>" + svg_square(4, unit="cm"), "respuesta": "4", "feedback_acierto": "¡Excelente!", "feedback_error": "Un cuadrado tiene vertical, horizontal y dos diagonales (4 en total)."},
                {"pregunta": "¿Cuántos ejes tiene un triángulo equilátero?<br/>" + svg_triangle_equilateral(3, unit="cm"), "respuesta": "3", "feedback_acierto": "¡Brillante!", "feedback_error": "Desde cada esquina al lado opuesto."}
            ]
        },
        # --- MÓDULO 4: Conversión y Pantallas ---
        {
            "modulo_id": 4, "nivel_id": 1,
            "titulo": "Interpretación de la escala gráfica base",
            "texto_descubrimiento": "¡Los mapas son versiones mini de la vida real! Como no podemos cargar un mapa del tamaño de una ciudad, usamos escalas.\nLa escala gráfica nos dice la correspondencia: por ejemplo, '1 centímetro en el papel representa 10 metros en la realidad'. Así, multiplicando la medida del mapa por el valor de escala, ¡descubrimos distancias reales!",
            "diccionario": {"Escala gráfica": "Barra dividida en segmentos que muestra la relación entre las distancias del plano y las reales.", "Distancia real": "Medida verdadera de un objeto en el mundo real.", "Proporción": "Relación de igualdad entre dos razones."},
            "advertencia": "No olvides multiplicar por la escala. La regla de la escala gráfica siempre funciona multiplicando.",
            "ejemplos": obtener_ejemplos_expandidos_fase5(4, 1),
            "interactivos": [
                {"pregunta": "Escala 1 cm = 10m. Si un borde en el mapa mide 4 cm, ¿cuántos metros son?<br/>" + svg_scale_bar(4, 10, unit="cm"), "respuesta": "40", "feedback_acierto": "¡Correcto! 4 x 10 = 40m.", "feedback_error": "Multiplica 4x10."},
                {"pregunta": "Escala 1 cm = 5km. Viajo 6 cm en el plano. ¿Distancia real en km?<br/>" + svg_scale_bar(6, 5, unit="cm"), "respuesta": "30", "feedback_acierto": "¡Excelente! 6 x 5 = 30km.", "feedback_error": "Multiplica 6x5."},
                {"pregunta": "Escala 1 cm = 2m. Altura de 15 cm en el plano. ¿Altura real en metros?<br/>" + svg_scale_bar(15, 2, unit="cm"), "respuesta": "30", "feedback_acierto": "¡Brillante!", "feedback_error": "Multiplica 15x2."}
            ]
        },
        {
            "modulo_id": 4, "nivel_id": 2,
            "titulo": "Modelado analítico de la diagonal (pantallas)",
            "texto_descubrimiento": "Cuando compramos una pantalla de televisión, de celular o tablet, nos dicen su tamaño en pulgadas (por ejemplo, 32 pulgadas o 50 pulgadas).\n¡Pero esa medida no es el ancho ni el alto! El tamaño de las pantallas siempre se mide en línea recta cruzando desde una esquina hasta la esquina contraria. ¡Eso es la diagonal!\n¿Sabías que existe una fórmula mágica para calcular la diagonal sin medirla directamente? Se llama el Teorema de Pitágoras: si conocemos la base y la altura de un rectángulo, la diagonal al cuadrado es igual a la suma de la base al cuadrado más la altura al cuadrado (diagonal² = base² + altura²). Por ejemplo, si la base mide 3 y la altura mide 4: 3² + 4² = 9 + 16 = 25, y la raíz cuadrada de 25 es 5. ¡La diagonal mide 5!",
            "diccionario": {"Diagonal": "Segmento de recta que une dos vértices (esquinas) no consecutivos de un polígono.", "Teorema de Pitágoras": "En un triángulo rectángulo, el cuadrado de la hipotenusa es la suma de los cuadrados de los catetos.", "Hipotenusa": "El lado más largo de un triángulo rectángulo."},
            "advertencia": "La diagonal siempre es el lado más largo de la pantalla. ¡Es mayor que la base y mayor que la altura!",
            "ejemplos": obtener_ejemplos_expandidos_fase5(4, 2),
            "interactivos": [
                {"pregunta": "Si un monitor se anuncia como '24 pulgadas', ¿qué mide 24 pulgadas? (escribe: la diagonal)<br/>" + svg_rect_diagonal(20, 12, diag_label="24 pulg", unit="pulg"), "respuesta": "la diagonal", "feedback_acierto": "¡Correcto! Se mide en diagonal.", "feedback_error": "Las pantallas se miden en diagonal. Escribe 'la diagonal'."},
                {"pregunta": "En un rectángulo de 3x4, ¿la diagonal mide 5? (Escribe 1 para SÍ, 2 para NO)<br/>" + svg_rect_diagonal(4, 3, diag_label="5", unit="cm"), "respuesta": "1", "feedback_acierto": "¡Excelente!", "feedback_error": "Sí, 3^2 + 4^2 = 5^2. Escribe 1."},
                {"pregunta": "¿Qué es más largo en un TV, la base o la diagonal? (escribe: diagonal)<br/>" + svg_rect_diagonal(16, 9, diag_label="?", unit="cm"), "respuesta": "diagonal", "feedback_acierto": "¡Brillante!", "feedback_error": "La diagonal siempre es la más larga. Escribe 'diagonal'."}
            ]
        },
        {
            "modulo_id": 4, "nivel_id": 3,
            "titulo": "Conversión de unidades de superficie",
            "texto_descubrimiento": "¡Cuidado con las unidades al cuadrado! Cuando medimos área, medimos en dos dimensiones (ancho × alto).\nPor eso, 1 metro lineal son 100 centímetros, ¡pero 1 metro cuadrado (m²) son 100 cm × 100 cm = 10,000 cm²! Para convertir áreas, aplicamos la escala dos veces (la escala al cuadrado). ¡Las superficies crecen muy rápido!",
            "diccionario": {"Metro cuadrado (m²)": "Área de un cuadrado que mide 1 metro de lado (equivalente a 10,000 cm²).", "Centímetro cuadrado (cm²)": "Unidad de área de 1 cm x 1 cm.", "Decímetro cuadrado (dm²)": "Unidad de área de 10 cm x 10 cm."},
            "advertencia": "Confusión clásica: al convertir unidades de área (superficie), recuerda multiplicar por la conversión al cuadrado, no por la lineal.",
            "ejemplos": obtener_ejemplos_expandidos_fase5(4, 3),
            "interactivos": [
                {"pregunta": "¿Cuántos centímetros cuadrados hay en 1 m²?<br/>" + svg_square(1, unit="m"), "respuesta": "10000", "feedback_acierto": "¡Correcto! 100 x 100 = 10,000.", "feedback_error": "Multiplica 100x100 para hallar los cm²."},
                {"pregunta": "Si 1 dm = 10 cm, ¿cuántos cm² hay en 1 dm²?<br/>" + svg_square(1, unit="dm"), "respuesta": "100", "feedback_acierto": "¡Excelente! 10 x 10 = 100.", "feedback_error": "Multiplica 10x10."},
                {"pregunta": "Si 1 m = 10 dm, ¿cuántos dm² hay en 2 m²?<br/>" + svg_rect(2, 1, unit="m"), "respuesta": "200", "feedback_acierto": "¡Brillante! 1 m² = 100 dm², entonces 2 m² = 200 dm².", "feedback_error": "1 m² = 100 dm². Multiplica por 2."}
            ]
        }
    ]
    for data in niveles_teoria:
        nt = NivelTeoria(fase_id=FASE5_ID, **data)
        session.add(nt)

def _deduplicate_alts(alts: list, correct: str, rng: random.Random) -> list:
    try:
        correct_num = int(correct)
    except ValueError:
        seen = set()
        result = []
        for alt in alts:
            if alt in seen:
                new_alt = alt + "_"
                while new_alt in seen:
                    new_alt += "_"
                result.append(new_alt)
                seen.add(new_alt)
            else:
                result.append(alt)
                seen.add(alt)
        return result

    seen = set()
    result = []
    for alt in alts:
        if alt == correct:
            if alt in seen:
                val = correct_num + rng.choice([2, 3, 5, -2, -3])
                while str(val) in seen or val <= 0 or val == correct_num:
                    val += rng.choice([1, 2, -1, -2])
                result.append(str(val))
                seen.add(str(val))
            else:
                result.append(alt)
                seen.add(alt)
        else:
            try:
                alt_num = int(alt)
                if alt_num == correct_num or str(alt_num) in seen:
                    val = correct_num + rng.choice([2, 3, 5, 7, -2, -3, -5])
                    while str(val) in seen or val <= 0 or val == correct_num:
                        val += rng.choice([1, 2, -1, -2])
                    result.append(str(val))
                    seen.add(str(val))
                else:
                    result.append(alt)
                    seen.add(alt)
            except ValueError:
                if alt in seen:
                    new_alt = alt + "_"
                    while new_alt in seen:
                        new_alt += "_"
                    result.append(new_alt)
                    seen.add(new_alt)
                else:
                    result.append(alt)
                    seen.add(alt)
    return result

async def _gen_fase5_pool(rng: random.Random, mod_id: int, lvl_id: int) -> dict:
    res = await _gen_fase5_pool_raw(rng, mod_id, lvl_id)
    if "alts" in res and "respuesta_correcta" in res:
        res["alts"] = _deduplicate_alts(res["alts"], res["respuesta_correcta"], rng)
    return res

async def _gen_fase5_pool_raw(rng: random.Random, mod_id: int, lvl_id: int) -> dict:
    nombre = rng.choice(NOMBRES)
    errores_previstos = {}

    if mod_id == 1:
        # Perímetro
        if lvl_id == 1:
            variant = rng.choice(["clean_rect", "grid", "irregular"])
            if variant == "irregular":
                target_area = rng.randint(6, 15)
                cells, ans = _generate_random_staircase(rng, 6, 6, target_area)
                ans_str = str(ans)
                color = rng.choice([(255,182,193,180), (144,238,144,180), (173,216,230,180), (221,160,221,180), (255,200,100,180)])
                unidad = rng.choice(["cm", "m", "mm"])
                
                cache_key = f"irreg_p_{target_area}_{ans}_{unidad}_6x6"
                if cache_key in _graphic_url_cache:
                    url = _graphic_url_cache[cache_key]
                else:
                    img_bytes = generate_irregular_grid_shape_image(cells, grid_size=(6, 6), fill_color=color)
                    url = await storage_service.upload_question_graphic(img_bytes, f"irreg_p_{target_area}_{ans}_{unidad}_v3.png")
                    _graphic_url_cache[cache_key] = url
                
                errores_previstos[str(target_area)] = "Calculaste el área contando los cuadraditos por dentro en lugar del perímetro (el contorno)."
                enunciado = f"Si el lado de cada cuadradito representa 1 {unidad}, cuenta las unidades del borde de la figura sombreada para hallar su perímetro en {unidad}."
                expl = f"Al contar los lados exteriores que limitan con el fondo blanco, obtenemos {ans} {unidad} de perímetro."
                return {
                    "enunciado": enunciado,
                    "datos_numericos": {"tipo_visual": "imagen", "url": url},
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": expl,
                    "alts": [ans_str, str(target_area), str(ans+2), str(ans-2)]
                }
            else:
                a = rng.randint(3, 8)
                b = rng.randint(3, 8)
                ans = 2 * (a + b)
                ans_str = str(ans)
                escenario = rng.choice(ESCENARIOS_P)
                
                if variant == "clean_rect":
                    cache_key = f"clean_p_{a}_{b}"
                    if cache_key in _graphic_url_cache:
                        url = _graphic_url_cache[cache_key]
                    else:
                        img_bytes = generate_clean_shape_image("rectangle", {"base": a, "height": b}, "m")
                        url = await storage_service.upload_question_graphic(img_bytes, f"clean_p_{a}_{b}_v2.png")
                        _graphic_url_cache[cache_key] = url
                else:
                    cache_key = f"grid_p_{a}_{b}"
                    if cache_key in _graphic_url_cache:
                        url = _graphic_url_cache[cache_key]
                    else:
                        vertices = [(1, 1), (1 + a, 1), (1 + a, 1 + b), (1, 1 + b)]
                        labels = {(0, 1): f"{a} u", (1, 2): f"{b} u"}
                        img_bytes = generate_grid_shape_image(vertices, grid_size=(max(10, a + 3), max(10, b + 3)), fill_color=(224, 247, 250, 150), outline_color=(30, 30, 30, 255), labels=labels)
                        url = await storage_service.upload_question_graphic(img_bytes, f"grid_p_{a}_{b}_v4.png")
                        _graphic_url_cache[cache_key] = url
                
                errores_previstos[str(a*b)] = "Calculaste el área (base por altura) en lugar del perímetro (sumar los bordes)."
                errores_previstos[str(a+b)] = "Solo sumaste dos lados. Recuerda que un rectángulo tiene 4 lados."
                
                unidad = rng.choice(["cm", "m"])
                templates = [
                    f"{nombre} quiere cercar su {escenario} rectangular. En la figura, los lados miden {a} y {b} {unidad}. Calcula el perímetro total en {unidad}.",
                    f"{nombre} dibujó un {escenario} con dimensiones {a} y {b} {unidad}. ¿Cuántos {unidad} mide todo el contorno?",
                    f"Una hormiguita camina por todo el borde de un {escenario} rectangular de {a}x{b} {unidad}. ¿Cuántos {unidad} recorrió la hormiguita?"
                ]
                enunciado = rng.choice(templates)
                
                return {
                    "enunciado": enunciado,
                    "datos_numericos": {"tipo_visual": "imagen", "url": url},
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": f"Sumamos los 4 lados del rectángulo: {a} + {b} + {a} + {b} = {ans} {unidad}.",
                    "alts": [ans_str, str(a*b), str(a+b), str(ans+4)]
                }
            
        elif lvl_id == 2:
            # Suma de magnitudes (polígonos sin cuadrícula)
            variant = rng.choice(["text", "rectilinear"])
            if variant == "rectilinear":
                unidad = rng.choice(["cm", "m", "mm"])
                segments, ans = _build_step_shape(rng, unit_label=unidad)
                ans_str = str(ans)
                cache_key = f"rect_p_{ans}_{segments[0][2]}_{unidad}"
                if cache_key in _graphic_url_cache:
                    url = _graphic_url_cache[cache_key]
                else:
                    img_bytes = generate_rectilinear_shape_image(segments, fill_color=(255, 235, 156, 180), outline_color=(30, 30, 30, 255))
                    url = await storage_service.upload_question_graphic(img_bytes, f"rect_p_{ans}_{segments[0][2]}_{unidad}_v2.png")
                    _graphic_url_cache[cache_key] = url
                
                errores_previstos[str(ans - int(segments[0][4].split()[0]))] = "Olvidaste sumar uno de los lados exteriores."
                _reg = rng.choice(["terreno", "jardín", "corral", "piscina", "sello de goma", "galleta", "parcela", "letrero"])
                enunciado = rng.choice([
                    f"{nombre} quiere poner una cerca alrededor de un {_reg} con esta forma (mira la imagen). Suma todos los lados del borde: ¿cuál es el perímetro total en {unidad}?",
                    f"Suma todas las medidas del borde de este {_reg} para hallar el perímetro total en {unidad}.",
                    f"Una hormiga recorre todo el contorno de este {_reg} (ver figura). ¿Cuántos {unidad} caminó en total?",
                ])
                expl = f"Sumamos todos los lados exteriores que muestran las cotas: el total es {ans} {unidad}."
                
                return {
                    "enunciado": enunciado,
                    "datos_numericos": {"tipo_visual": "imagen", "url": url},
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": expl,
                    "alts": [ans_str, str(ans - int(segments[0][4].split()[0])), str(ans + 2), str(ans - 2)]
                }
            else:
                a = rng.randint(4, 10)
                b = rng.randint(4, 10)
                c = rng.randint(4, 10)
                d = rng.randint(4, 10)
                ans = a + b + c + d
                ans_str = str(ans)
                
                errores_previstos[str(a+b+c)] = "Te faltó sumar uno de los lados. Un cuadrilátero tiene 4 lados."
                errores_previstos[str(ans - d)] = "Olvidaste sumar el último lado en el perímetro."
                
                unidad = rng.choice(["cm", "m", "mm"])
                svg_quad = (
                    f"<svg width='240' height='200' viewBox='-10 -10 260 220' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                    f"  <polygon points='30,160 210,160 190,40 50,40' fill='#E0F2FE' fill-opacity='0.7' stroke='#1E293B' stroke-width='2.5'/>"
                    f"  <text x='120' y='178' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='middle'>{a} {unidad}</text>"
                    f"  <text x='215' y='110' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='start'>{b} {unidad}</text>"
                    f"  <text x='120' y='26' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='middle'>{c} {unidad}</text>"
                    f"  <text x='15' y='110' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='end'>{d} {unidad}</text>"
                    f"</svg>"
                )
                
                templates = [
                    f"{nombre} tiene una mesa con forma de cuadrilátero irregular cuyos lados miden {a}, {b}, {c} y {d} {unidad}. ¿Cuál es el perímetro de la mesa?<br/>{svg_quad}",
                    f"El patio de la escuela de {nombre} tiene forma de cuadrilátero con lados de {a}, {b}, {c} y {d} {unidad}. ¿Cuánto mide su contorno por completo?<br/>{svg_quad}",
                    f"{nombre} está diseñando un cartel con lados de {a}, {b}, {c} y {d} {unidad}. ¿Cuánto mide el contorno del cartel?<br/>{svg_quad}"
                ]
                enunciado = rng.choice(templates)
                
                return {
                    "enunciado": enunciado,
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": f"Sumamos todos los lados del cuadrilátero: {a} + {b} + {c} + {d} = {ans} {unidad}.",
                    "alts": [ans_str, str(a+b+c), str(ans+5), str(ans-5)]
                }
            
        else:
            # Conversión de unidades lineales
            case = rng.choice([1, 2, 3])
            if case == 1:
                a = rng.randint(2, 6)
                b = rng.randint(10, 50)
                ans = 2 * (a * 100 + b)
                ans_str = str(ans)
                # SVG rectángulo con etiquetas de unidades mixtas
                svg_conv = (
                    f"<svg width='240' height='160' viewBox='-10 -10 280 180' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                    f"  <rect x='30' y='30' width='180' height='100' fill='#FEF9C3' fill-opacity='0.8' stroke='#1E293B' stroke-width='2.5'/>"
                    f"  <text x='120' y='18' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='middle'>{a} m</text>"
                    f"  <text x='220' y='84' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='start'>{b} cm</text>"
                    f"  <text x='120' y='152' fill='#FFFFFF' font-size='16' text-anchor='middle' fill-opacity='0.7'>(Convertir a cm)</text>"
                    f"</svg>"
                )
                templates = [
                    f"Un terreno rectangular mide {a} metros de largo y {b} centímetros de ancho. ¿Cuál es su perímetro en centímetros?<br/>{svg_conv}",
                    f"Para un marco, {nombre} usa un listón de {a} metros de largo y {b} centímetros de ancho. ¿Cuál es el perímetro en centímetros?<br/>{svg_conv}",
                    f"Una alfombra rectangular tiene {a} metros de largo y {b} centímetros de ancho. ¿Cuánto mide su contorno en centímetros?<br/>{svg_conv}"
                ]
                expl = f"Convertimos {a} m a {a*100} cm. Luego sumamos los 4 lados: {a*100} + {b} + {a*100} + {b} = {ans} cm."
            elif case == 2:
                a = rng.randint(3, 8)
                b = rng.randint(5, 25)
                ans = 2 * (a * 10 + b)
                ans_str = str(ans)
                svg_conv = (
                    f"<svg width='240' height='160' viewBox='-10 -10 280 180' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                    f"  <rect x='30' y='30' width='180' height='100' fill='#FEF9C3' fill-opacity='0.8' stroke='#1E293B' stroke-width='2.5'/>"
                    f"  <text x='120' y='18' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='middle'>{a} m</text>"
                    f"  <text x='220' y='84' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='start'>{b} dm</text>"
                    f"  <text x='120' y='152' fill='#FFFFFF' font-size='16' text-anchor='middle' fill-opacity='0.7'>(Convertir a dm)</text>"
                    f"</svg>"
                )
                templates = [
                    f"La mesa de {nombre} mide {a} metros de largo y {b} decímetros de ancho. ¿Cuál es su perímetro en decímetros?<br/>{svg_conv}",
                    f"Una pizarra rectangular mide {a} metros de base y {b} decímetros de altura. ¿Cuál es su perímetro en decímetros?<br/>{svg_conv}",
                    f"{nombre} tiene un huerto rectangular de {a} metros de largo por {b} decímetros de ancho. ¿Cuánto mide su contorno en decímetros?<br/>{svg_conv}"
                ]
                expl = f"Convertimos {a} m a {a*10} dm. Luego sumamos los 4 lados: {a*10} + {b} + {a*10} + {b} = {ans} dm."
            else:
                a = rng.randint(1, 4)
                b = rng.randint(100, 800)
                ans = 2 * (a * 1000 + b)
                ans_str = str(ans)
                svg_conv = (
                    f"<svg width='240' height='160' viewBox='-10 -10 280 180' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                    f"  <rect x='30' y='30' width='180' height='100' fill='#FEF9C3' fill-opacity='0.8' stroke='#1E293B' stroke-width='2.5'/>"
                    f"  <text x='120' y='18' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='middle'>{a} km</text>"
                    f"  <text x='220' y='84' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='start'>{b} m</text>"
                    f"  <text x='120' y='152' fill='#FFFFFF' font-size='16' text-anchor='middle' fill-opacity='0.7'>(Convertir a m)</text>"
                    f"</svg>"
                )
                templates = [
                    f"Un parque rectangular tiene {a} kilómetros de largo y {b} metros de ancho. ¿Cuál es su perímetro total en metros?<br/>{svg_conv}",
                    f"Una pista de atletismo rectangular mide {a} km de largo y {b} metros de ancho. ¿Cuál es el perímetro en metros?<br/>{svg_conv}",
                    f"{nombre} da una vuelta completa a un campo de {a} km de largo y {b} metros de ancho. ¿Cuántos metros recorrió?<br/>{svg_conv}"
                ]
                expl = f"Convertimos {a} km a {a*1000} m. Luego sumamos los 4 lados: {a*1000} + {b} + {a*1000} + {b} = {ans} metros."
                
            enunciado = rng.choice(templates)
            errores_previstos[str(a+b)] = "Debes convertir las unidades para que sean iguales antes de sumar los 4 lados."
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "alts": [ans_str, str(a+b), str(ans + 20), str(ans - 20)]
            }

    elif mod_id == 2:
        # Área
        if lvl_id == 1:
            variant = rng.choice(["clean_rect", "grid", "irregular"])
            if variant == "irregular":
                target_area = rng.randint(8, 20)
                cells, perim = _generate_random_staircase(rng, 6, 6, target_area)
                ans_str = str(target_area)
                color = rng.choice([(255,182,193,180), (144,238,144,180), (173,216,230,180), (221,160,221,180), (255,200,100,180)])
                unidad = rng.choice(["cm", "m", "mm"])
                
                cache_key = f"irreg_a_{target_area}_{perim}_{unidad}_6x6"
                if cache_key in _graphic_url_cache:
                    url = _graphic_url_cache[cache_key]
                else:
                    img_bytes = generate_irregular_grid_shape_image(cells, grid_size=(6, 6), fill_color=color)
                    url = await storage_service.upload_question_graphic(img_bytes, f"irreg_a_{target_area}_{perim}_{unidad}_v3.png")
                    _graphic_url_cache[cache_key] = url
                
                errores_previstos[str(perim)] = "Calculaste el perímetro (contar el borde) en lugar del área (contar los cuadraditos de adentro)."
                enunciado = f"Si cada cuadradito representa 1 {unidad}², cuenta los cuadraditos sombreados para hallar el área total de la figura en {unidad}²."
                expl = f"Al contar cada cuadradito que está pintado por dentro, obtenemos un total de {target_area} {unidad}²."
                return {
                    "enunciado": enunciado,
                    "datos_numericos": {"tipo_visual": "imagen", "url": url},
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": expl,
                    "alts": [ans_str, str(perim), str(target_area+2), str(target_area-2)]
                }
            else:
                a = rng.randint(3, 7)
                b = rng.randint(3, 7)
                ans = a * b
                ans_str = str(ans)
                escenario = rng.choice(ESCENARIOS_A)
                unidad = rng.choice(["cm", "m"])
                
                if variant == "clean_rect":
                    cache_key = f"clean_a_{a}_{b}_{unidad}"
                    if cache_key in _graphic_url_cache:
                        url = _graphic_url_cache[cache_key]
                    else:
                        img_bytes = generate_clean_shape_image("rectangle", {"base": a, "height": b}, unidad)
                        url = await storage_service.upload_question_graphic(img_bytes, f"clean_a_{a}_{b}_{unidad}_v2.png")
                        _graphic_url_cache[cache_key] = url
                else:
                    cache_key = f"grid_a_{a}_{b}_{unidad}"
                    if cache_key in _graphic_url_cache:
                        url = _graphic_url_cache[cache_key]
                    else:
                        vertices = [(1, 1), (1 + a, 1), (1 + a, 1 + b), (1, 1 + b)]
                        labels = {(0, 1): f"{a} {unidad}", (1, 2): f"{b} {unidad}"}
                        img_bytes = generate_grid_shape_image(vertices, grid_size=(max(10, a + 3), max(10, b + 3)), fill_color=(224, 247, 250, 150), outline_color=(30, 30, 30, 255), labels=labels)
                        url = await storage_service.upload_question_graphic(img_bytes, f"grid_a_{a}_{b}_{unidad}_v4.png")
                        _graphic_url_cache[cache_key] = url
                
                errores_previstos[str(2*(a+b))] = "Calculaste el perímetro (sumar bordes) en lugar del área (multiplicar dimensiones)."
                errores_previstos[str(a+b)] = "Sumaste la base y la altura en lugar de multiplicarlas."
                
                templates = [
                    f"{nombre} necesita cubrir su {escenario} rectangular con baldosas. La base mide {a} {unidad} y la altura {b} {unidad}. Calcula el área total en {unidad}².",
                    f"En una cuadrícula donde cada cuadro es 1 {unidad}², {nombre} pintó un {escenario} rectangular de {a} {unidad} de base y {b} {unidad} de altura. ¿Cuántos {unidad}² pintó en total?",
                    f"{nombre} colocó tapetes de 1 {unidad}² para cubrir un piso rectangular de {a} {unidad} de base por {b} {unidad} de altura. ¿Cuántos tapetes utilizó en total?"
                ]
                enunciado = rng.choice(templates)
                
                return {
                    "enunciado": enunciado,
                    "datos_numericos": {"tipo_visual": "imagen", "url": url},
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": f"Multiplicamos base por altura: {a} × {b} = {ans} {unidad}².",
                    "alts": [ans_str, str(2*(a+b)), str(a+b), str(ans+3)]
                }
            
        elif lvl_id == 2:
            # Fusión de sectores triangulares
            enteros = rng.randint(2, 10)
            mitades = rng.choice([2, 4, 6, 8])
            ans = enteros + mitades // 2
            ans_str = str(ans)
            
            errores_previstos[str(enteros + mitades)] = "Sumaste las mitades como si fueran cuadrados enteros. Recuerda que 2 mitades forman 1 entero."
            errores_previstos[str(enteros)] = "Olvidaste sumar las mitades triangulares al área total."
            
            # SVG: cuadrícula mostrando cuadrados enteros + triángulos mitad
            cols = min(enteros + mitades, 6)
            svg_rows = []
            count_ent = 0
            count_mit = 0
            svg_cells = ""
            cx, cy, cs = 20, 20, 28
            col_i = 0
            row_i = 0
            for _ in range(enteros):
                if col_i >= cols:
                    col_i = 0
                    row_i += 1
                x = cx + col_i * cs
                y = cy + row_i * cs
                svg_cells += f"<rect x='{x}' y='{y}' width='{cs}' height='{cs}' fill='#BAE6FD' stroke='#64748B' stroke-width='1'/>"
                col_i += 1
            for _ in range(mitades):
                if col_i >= cols:
                    col_i = 0
                    row_i += 1
                x = cx + col_i * cs
                y = cy + row_i * cs
                svg_cells += f"<polygon points='{x},{y} {x+cs},{y} {x+cs},{y+cs}' fill='#FCA5A5' stroke='#64748B' stroke-width='1'/>"
                col_i += 1
            grid_w = cols * cs + cx * 2
            grid_h = (row_i + 1) * cs + cy * 2
            svg_tri = (
                f"<svg width='240' height='{min(180, grid_h+30)}' viewBox='-5 -5 {grid_w+10} {grid_h+20}' "
                f"style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                f"{svg_cells}"
                f"<text x='{grid_w//2}' y='{grid_h+12}' fill='#FFFFFF' font-size='15' text-anchor='middle'>"
                f"🔵={enteros} enteros  🔴={mitades} mitades</text>"
                f"</svg>"
            )
            
            unidad = rng.choice(["cm", "m"])
            templates = [
                f"Una figura en la cuadrícula (donde cada cuadrado es 1 {unidad}²) de {nombre} tiene {enteros} cuadrados enteros pintados de color y {mitades} mitades triangulares. ¿Cuál es el área total en {unidad}²?<br/>{svg_tri}",
                f"{nombre} diseñó un mosaico con {enteros} cuadros enteros de 1 {unidad}² y {mitades} mitades de cuadro. ¿Cuánto mide el área de todo el mosaico en {unidad}²?<br/>{svg_tri}",
                f"Calcula el área total en {unidad}² si la figura tiene {enteros} cuadros enteros y {mitades} pedazos que son exactamente la mitad de un cuadro.<br/>{svg_tri}"
            ]
            enunciado = rng.choice(templates)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": f"Cada 2 mitades forman 1 entero: {mitades} mitades = {mitades//2} enteros. Sumamos con los {enteros} enteros: {enteros} + {mitades//2} = {ans} {unidad}².",
                "alts": [ans_str, str(enteros+mitades), str(enteros), str(ans+2)]
            }
            
        else:
            variant = rng.choice(["l_shape_clean", "rectilinear", "text"])
            unidad = rng.choice(["cm", "m"])
            if variant == "l_shape_clean":
                w1 = rng.randint(2, 5)
                h1 = rng.randint(4, 8)
                w2 = rng.randint(3, 6)
                h2 = rng.randint(2, 4)
                if h1 <= h2: h1 = h2 + 2
                ans = w1 * h1 + w2 * h2
                ans_str = str(ans)
                
                cache_key = f"clean_l_{w1}_{h1}_{w2}_{h2}_{unidad}"
                if cache_key in _graphic_url_cache:
                    url = _graphic_url_cache[cache_key]
                else:
                    dims = {"w1": w1, "h1": h1, "w2": w2, "h2": h2}
                    img_bytes = generate_clean_shape_image("l_shape", dims, unidad)
                    url = await storage_service.upload_question_graphic(img_bytes, f"clean_l_{w1}_{h1}_{w2}_{h2}_{unidad}_v2.png")
                    _graphic_url_cache[cache_key] = url
                    
                errores_previstos[str(w1*h1)] = "Solo calculaste el área de la parte vertical de la L."
                errores_previstos[str(w2*h2)] = "Solo calculaste el área de la base horizontal de la L."
                
                _reg = rng.choice(["terreno", "cartel", "recorte de cartón", "sticker", "parche de tela", "adorno", "mosaico especial", "plano"])
                enunciado = rng.choice([
                    f"{nombre} tiene un {_reg} con forma de L (mira la imagen). Divídelo en dos rectángulos y suma sus áreas: ¿cuál es el área total en {unidad}²?",
                    f"Observa este {_reg} en forma de L. Divide la figura en dos rectángulos para hallar su área total en {unidad}².",
                    f"El {_reg} de {nombre} tiene forma de L. Sepáralo mentalmente en dos rectángulos y calcula el área total en {unidad}².",
                ])
                expl = f"Dividimos la figura en dos rectángulos: ({w1} × {h1}) y ({w2} × {h2}). Sumamos: {w1*h1} + {w2*h2} = {ans} {unidad}²."
                
                return {
                    "enunciado": enunciado,
                    "datos_numericos": {"tipo_visual": "imagen", "url": url},
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": expl,
                    "alts": [ans_str, str(w1*h1), str(w2*h2), str(ans+5)]
                }
            elif variant == "rectilinear":
                segments, perim = _build_step_shape(rng, unit_label=unidad)
                # area = w1*h1 + w1*h2 + w2*h2 = w1*(h1+h2) + w2*h2 (from generator logic)
                # Let's extract dimensions: (0, h1+h2, w1+w2, h1+h2), so total width is w1+w2, left height is h1+h2
                w_total = int(segments[0][4].split()[0])
                h1 = int(segments[1][4].split()[0])
                w2 = int(segments[2][4].split()[0])
                h2 = int(segments[3][4].split()[0])
                w1 = int(segments[4][4].split()[0])
                h_total = int(segments[5][4].split()[0])
                
                ans = w1 * h_total + w2 * h2
                ans_str = str(ans)
                
                cache_key = f"rect_a_{ans}_{perim}_{unidad}"
                if cache_key in _graphic_url_cache:
                    url = _graphic_url_cache[cache_key]
                else:
                    img_bytes = generate_rectilinear_shape_image(segments, fill_color=(255, 235, 156, 180), outline_color=(30, 30, 30, 255))
                    url = await storage_service.upload_question_graphic(img_bytes, f"rect_a_{ans}_{perim}_{unidad}_v2.png")
                    _graphic_url_cache[cache_key] = url
                
                errores_previstos[str(perim)] = "Calculaste el perímetro (sumar los bordes) en lugar del área."
                
                _reg = rng.choice(["terreno", "cartel", "recorte de cartón", "sticker", "parche de tela", "adorno", "azulejo", "plano"])
                enunciado = rng.choice([
                    f"{nombre} tiene un {_reg} con esta forma escalonada (mira la imagen). Divídelo en dos rectángulos simples y calcula su área total en {unidad}².",
                    f"Divide este {_reg} escalonado en dos rectángulos para calcular el área total en {unidad}².",
                    f"El {_reg} de {nombre} tiene forma escalonada. Sepáralo en rectángulos, suma las áreas y da el área total en {unidad}².",
                ])
                expl = f"La separamos en un rectángulo de {w1}×{h_total} y otro de {w2}×{h2}. Sumamos: {w1*h_total} + {w2*h2} = {ans} {unidad}²."
                
                return {
                    "enunciado": enunciado,
                    "datos_numericos": {"tipo_visual": "imagen", "url": url},
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": expl,
                    "alts": [ans_str, str(perim), str(ans+2), str(ans-2)]
                }
            else:
                a = rng.randint(2, 5)
                b = rng.randint(2, 5)
                c = rng.randint(2, 4)
                d = rng.randint(2, 4)
                ans = a * b + c * d
                ans_str = str(ans)
                
                errores_previstos[str(a*b)] = "Solo calculaste el área de la primera sección."
                errores_previstos[str(c*d)] = "Solo calculaste el área de la segunda sección."
                
                # SVG: figura en L compuesta de dos rectángulos etiquetados
                s = 20  # escala de celda
                r1w, r1h = a * s, b * s
                r2w, r2h = c * s, d * s
                total_w = max(r1w, r2w) + 60
                total_h = r1h + r2h + 20
                svg_l = (
                    f"<svg width='220' height='{min(200, total_h+50)}' viewBox='-10 -10 {total_w+20} {total_h+40}' "
                    f"style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                    f"  <rect x='10' y='10' width='{r1w}' height='{r1h}' fill='#BAE6FD' fill-opacity='0.8' stroke='#1E293B' stroke-width='2'/>"
                    f"  <text x='{10+r1w//2}' y='{10+r1h//2}' fill='#1E293B' font-size='16' font-weight='bold' text-anchor='middle' dominant-baseline='middle'>{a}×{b} {unidad}</text>"
                    f"  <rect x='10' y='{10+r1h}' width='{r2w}' height='{r2h}' fill='#BBF7D0' fill-opacity='0.8' stroke='#1E293B' stroke-width='2'/>"
                    f"  <text x='{10+r2w//2}' y='{10+r1h+r2h//2}' fill='#1E293B' font-size='16' font-weight='bold' text-anchor='middle' dominant-baseline='middle'>{c}×{d} {unidad}</text>"
                    f"</svg>"
                )
                
                templates = [
                    f"Una figura en forma de L se compone de dos rectángulos: uno mide {a}×{b} {unidad} y el otro {c}×{d} {unidad}. ¿Cuál es el área total en {unidad}²?<br/>{svg_l}",
                    f"El jardín de {nombre} se compone de dos secciones rectangulares unidas: una de {a}×{b} {unidad} y otra de {c}×{d} {unidad}. ¿Cuál es el área total del jardín en {unidad}²?<br/>{svg_l}",
                    f"Para una maqueta, {nombre} unió una placa de {a}×{b} {unidad} con otra de {c}×{d} {unidad}. ¿Cuál es el área total en {unidad}²?<br/>{svg_l}"
                ]
                enunciado = rng.choice(templates)
                
                return {
                    "enunciado": enunciado,
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": f"Calculamos el área de ambas partes y las sumamos: ({a} × {b}) + ({c} × {d}) = {a*b} + {c*d} = {ans} {unidad}².",
                    "alts": [ans_str, str(a*b), str(c*d), str(ans+5)]
                }

    elif mod_id == 3:
        # Figuras compuestas
        if lvl_id == 4: # Simetría
            # Expandimos a más figuras con SVGs ilustrativos
            # SVGs LIMPIOS (sin dibujar los ejes): antes algunas figuras (cuadrado, rombo,
            # rectángulo) mostraban TODOS sus ejes como líneas punteadas → la respuesta era
            # solo "contar las líneas". Ahora se muestra la figura sola y el alumno razona.
            figs_data = [
                ("rectángulo", 2, "<rect x='40' y='50' width='120' height='70' fill='#BAE6FD' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
                ("cuadrado", 4, "<rect x='50' y='40' width='100' height='100' fill='#BBF7D0' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
                ("triángulo equilátero", 3, "<polygon points='100,25 170,145 30,145' fill='#FCA5A5' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
                ("triángulo isósceles", 1, "<polygon points='100,25 160,145 40,145' fill='#FDE68A' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
                ("rombo", 2, "<polygon points='100,25 170,85 100,145 30,85' fill='#C4B5FD' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
                ("pentágono regular", 5, "<polygon points='100,25 168,73 142,150 58,150 32,73' fill='#BAE6FD' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
                ("hexágono regular", 6, "<polygon points='100,25 160,58 160,122 100,155 40,122 40,58' fill='#BBF7D0' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
                ("trapecio isósceles", 1, "<polygon points='60,45 140,45 170,135 30,135' fill='#FCA5A5' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
                ("letra L", 0, "<polygon points='40,30 78,30 78,98 140,98 140,140 40,140' fill='#93C5FD' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
                ("círculo", -1, "<circle cx='100' cy='90' r='62' fill='#FBCFE8' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
                ("estrella de 5 puntas", 5, "<polygon points='100,25 116,72 166,72 126,102 141,150 100,120 59,150 74,102 34,72 84,72' fill='#FDE68A' fill-opacity='0.85' stroke='#1E293B' stroke-width='2.5'/>"),
            ]
            fig_choice = rng.choice(figs_data)
            fig, ejes, svg_shape = fig_choice
            # El círculo tiene infinitos ejes de simetría → respuesta de texto.
            ans_str = "infinitos" if ejes == -1 else str(ejes)

            errores_previstos["0"] = "Esa figura sí tiene ejes de simetría (excepto la letra L). Imagina doblarla por la mitad."

            svg_sym = (
                f"<svg width='200' height='180' viewBox='0 0 200 180' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                f"{svg_shape}"
                f"</svg>"
            )
            
            templates = [
                f"En la clase de arte, {nombre} dibujó un {fig}. ¿Cuántos ejes de simetría tiene esta figura?<br/>{svg_sym}",
                f"{nombre} dobló un dibujo de un {fig} buscando líneas donde las dos mitades coincidan. ¿Cuántas líneas encontró?<br/>{svg_sym}",
                f"Si miras un dibujo de un {fig} en el espejo, ¿cuántos ejes de simetría diferentes tiene?<br/>{svg_sym}"
            ]
            enunciado = rng.choice(templates)
            
            # Distractores distintos garantizados (antes ["ans","0","1","6"] repetía
            # cuando la respuesta era 0, 1 o 6).
            _pool = ["0", "1", "2", "3", "4", "5", "6", "infinitos"]
            _distract = [x for x in _pool if x != ans_str]
            rng.shuffle(_distract)
            expl_txt = (f"El círculo tiene infinitos ejes de simetría: cualquier diámetro lo parte en dos mitades iguales."
                        if ans_str == "infinitos" else f"Un {fig} tiene exactamente {ejes} ejes de simetría.")
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl_txt,
                "alts": [ans_str] + _distract[:3]
            }
        elif lvl_id == 1:
            variant = rng.choice(["text", "rectilinear"])
            if variant == "rectilinear":
                unidad = rng.choice(["cm", "m"])
                segments, perim = _build_step_shape(rng, unit_label=unidad)
                w_total = int(segments[0][4].split()[0])
                h1 = int(segments[1][4].split()[0])
                w2 = int(segments[2][4].split()[0])
                h2 = int(segments[3][4].split()[0])
                w1 = int(segments[4][4].split()[0])
                h_total = int(segments[5][4].split()[0])
                
                ans = w1 * h_total + w2 * h2
                ans_str = str(ans)
                
                cache_key = f"rect_decomp_a_{ans}_{perim}_{unidad}"
                if cache_key in _graphic_url_cache:
                    url = _graphic_url_cache[cache_key]
                else:
                    img_bytes = generate_rectilinear_shape_image(segments, fill_color=(255, 235, 156, 180), outline_color=(30, 30, 30, 255))
                    url = await storage_service.upload_question_graphic(img_bytes, f"rect_decomp_a_{ans}_{perim}_{unidad}_v2.png")
                    _graphic_url_cache[cache_key] = url
                
                errores_previstos[str(perim)] = "Calculaste el perímetro (sumar los bordes) en lugar del área."
                
                _reg = rng.choice(["terreno", "cartel", "recorte de cartón", "sticker", "parche de tela", "adorno", "azulejo", "plano"])
                enunciado = rng.choice([
                    f"{nombre} tiene un {_reg} con esta forma escalonada (mira la imagen). Divídelo en dos rectángulos simples y calcula su área total en {unidad}².",
                    f"Divide este {_reg} escalonado en dos rectángulos para calcular el área total en {unidad}².",
                    f"El {_reg} de {nombre} tiene forma escalonada. Sepáralo en rectángulos, suma las áreas y da el área total en {unidad}².",
                ])
                expl = f"La separamos en un rectángulo de {w1}×{h_total} y otro de {w2}×{h2}. Sumamos: {w1*h_total} + {w2*h2} = {ans} {unidad}²."
                
                return {
                    "enunciado": enunciado,
                    "datos_numericos": {"tipo_visual": "imagen", "url": url},
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": expl,
                    "alts": [ans_str, str(perim), str(ans+2), str(ans-2)]
                }
            else:
                a = rng.randint(15, 50)
                b = rng.randint(10, 40)
                ans = a + b
                ans_str = str(ans)
                unidad = rng.choice(["cm", "m"])
                
                errores_previstos[str(abs(a-b))] = "Restaste las áreas. Al unir figuras para formar una más grande, sus áreas deben sumarse."
                
                # SVG: dos rectángulos apilados con sus áreas etiquetadas
                svg_stack = (
                    f"<svg width='200' height='180' viewBox='-10 -10 220 200' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                    f"  <rect x='20' y='10' width='160' height='70' fill='#BAE6FD' fill-opacity='0.8' stroke='#1E293B' stroke-width='2'/>"
                    f"  <text x='100' y='50' fill='#1E293B' font-size='18' font-weight='bold' text-anchor='middle' dominant-baseline='middle'>Área = {a} {unidad}²</text>"
                    f"  <rect x='20' y='80' width='160' height='70' fill='#BBF7D0' fill-opacity='0.8' stroke='#1E293B' stroke-width='2'/>"
                    f"  <text x='100' y='120' fill='#1E293B' font-size='18' font-weight='bold' text-anchor='middle' dominant-baseline='middle'>Área = {b} {unidad}²</text>"
                    f"  <text x='100' y='168' fill='#FFFFFF' font-size='16' text-anchor='middle'>Área total = {a} + {b}</text>"
                    f"</svg>"
                )
                
                templates = [
                    f"{nombre} construyó una figura compuesta por dos rectángulos pegados: el superior tiene un área de {a} {unidad}² y el inferior tiene un área de {b} {unidad}². ¿Cuál es el área total en {unidad}²?<br/>{svg_stack}",
                    f"Una placa metálica se descompone en un cuadrado de área {a} {unidad}² y un rectángulo de área {b} {unidad}² colocados uno al lado del otro. ¿Cuál es el área total de la placa en {unidad}²?<br/>{svg_stack}",
                    f"Para hacer un diseño, {nombre} pegó dos cartulinas, una de área {a} {unidad}² y otra de área {b} {unidad}². ¿Cuál es el área total ocupada en {unidad}²?<br/>{svg_stack}"
                ]
                enunciado = rng.choice(templates)
                
                return {
                    "enunciado": enunciado,
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": f"Sumamos el área de ambas partes descompuestas: {a} + {b} = {ans} {unidad}².",
                    "alts": [ans_str, str(abs(a-b)), str(a*2), str(ans-5)]
                }
        elif lvl_id == 2:
            # Conservación de áreas (Tangram)
            total = rng.randint(12, 40)
            ans = total
            ans_str = str(ans)
            unidad = rng.choice(["cm", "m"])
            
            errores_previstos[str(total*2)] = "El área se conserva. Mover o reorganizar las piezas no aumenta el tamaño de la figura."
            errores_previstos[str(total//2)] = "El área se conserva. Cortar o rotar piezas sin quitar ninguna mantiene la superficie total."
            
            # SVG: Tangram simplificado con piezas de colores y flecha de transformación
            svg_tangram = (
                f"<svg width='260' height='130' viewBox='-5 -5 270 140' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                f"  <rect x='10' y='10' width='60' height='60' fill='#BAE6FD' fill-opacity='0.8' stroke='#1E293B' stroke-width='1.5'/>"
                f"  <polygon points='70,10 130,10 130,70' fill='#BBF7D0' fill-opacity='0.8' stroke='#1E293B' stroke-width='1.5'/>"
                f"  <polygon points='70,10 70,70 130,70' fill='#FCA5A5' fill-opacity='0.8' stroke='#1E293B' stroke-width='1.5'/>"
                f"  <text x='70' y='85' fill='#FFFFFF' font-size='16' text-anchor='middle'>Área = {total} {unidad}²</text>"
                f"  <text x='155' y='45' fill='#FFFFFF' font-size='18' text-anchor='middle'>→</text>"
                f"  <polygon points='175,70 205,10 235,70' fill='#FDE68A' fill-opacity='0.8' stroke='#1E293B' stroke-width='1.5'/>"
                f"  <rect x='175' y='70' width='60' height='30' fill='#C4B5FD' fill-opacity='0.8' stroke='#1E293B' stroke-width='1.5'/>"
                f"  <text x='205' y='118' fill='#FFFFFF' font-size='16' text-anchor='middle'>¿Área?</text>"
                f"</svg>"
            )
            
            templates = [
                f"Si {nombre} usa todas las piezas de un Tangram con área total de {total} {unidad}² para armar la figura de un gato, ¿cuál es el área del gato en {unidad}²?<br/>{svg_tangram}",
                f"{nombre} tiene un cuadrado de papel con área de {total} {unidad}² y lo corta en 4 partes. Si vuelve a armar un barco con esas piezas sin encimarlas, ¿cuál es el área total del barco en {unidad}²?<br/>{svg_tangram}",
                f"Un rompecabezas de área {total} {unidad}² es desarmado por {nombre} para formar una estrella usando todas las piezas. ¿Cuál es el área de la estrella en {unidad}²?<br/>{svg_tangram}"
            ]
            enunciado = rng.choice(templates)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": f"Por el principio de conservación de área, cambiar la forma o posición de las piezas no altera el área total: sigue siendo {ans} {unidad}².",
                "alts": [ans_str, str(total*2), str(total//2), str(total+5)]
            }
        else:
            variant = rng.choice(["text", "u_shape"])
            if variant == "u_shape":
                w = rng.randint(6, 10)
                h = rng.randint(5, 8)
                t = rng.randint(2, 3) # thickness
                unidad = rng.choice(["cm", "m"])
                
                segments = [
                    (0, h, w, h, f"{w} {unidad}"), # bottom
                    (w, h, w, 0, f"{h} {unidad}"), # right outer
                    (w, 0, w-t, 0, f"{t} {unidad}"), # top right
                    (w-t, 0, w-t, h-t, f"{h-t} {unidad}"), # inner right
                    (w-t, h-t, t, h-t, f"{w-2*t} {unidad}"), # inner bottom
                    (t, h-t, t, 0, f"{h-t} {unidad}"), # inner left
                    (t, 0, 0, 0, f"{t} {unidad}"), # top left
                    (0, 0, 0, h, f"{h} {unidad}") # left outer
                ]
                ans = w * h - (w - 2*t) * (h - t)
                ans_str = str(ans)
                
                cache_key = f"u_shape_a_{w}_{h}_{t}_{unidad}"
                if cache_key in _graphic_url_cache:
                    url = _graphic_url_cache[cache_key]
                else:
                    img_bytes = generate_rectilinear_shape_image(segments, fill_color=(255, 182, 193, 180), outline_color=(30, 30, 30, 255))
                    url = await storage_service.upload_question_graphic(img_bytes, f"u_shape_{w}_{h}_{t}_{unidad}_v2.png")
                    _graphic_url_cache[cache_key] = url
                
                errores_previstos[str(w*h)] = "Calculaste el área del rectángulo exterior completo sin restarle el hueco blanco."
                
                _obj = rng.choice(["una herradura", "un portarretratos", "un molde de galleta", "una pieza de rompecabezas", "un imán de nevera", "una placa metálica"])
                enunciado = rng.choice([
                    f"{nombre} recortó {_obj} con forma de U (en color) y un hueco blanco en el medio. Calcula el área sombreada en {unidad}². (Pista: área grande − hueco).",
                    f"Calcula el área sombreada (de color) de esta figura en forma de U en {unidad}². Pista: área del rectángulo grande menos el hueco blanco.",
                    f"La figura en U de {nombre} tiene una parte de color y un hueco blanco. ¿Cuál es el área sombreada en {unidad}²? (Resta el hueco al total).",
                ])
                expl = f"El rectángulo exterior es de {w}×{h} = {w*h} {unidad}². El hueco blanco es de ({w-2*t})×({h-t}) = {(w-2*t)*(h-t)} {unidad}². Restamos: {w*h} - {(w-2*t)*(h-t)} = {ans} {unidad}²."
                
                return {
                    "enunciado": enunciado,
                    "datos_numericos": {"tipo_visual": "imagen", "url": url},
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": expl,
                    "alts": [ans_str, str(w*h), str(ans+5), str(ans-5)]
                }
            else:
                ext = rng.randint(40, 100)
                int_h = rng.randint(5, 25)
                ans = ext - int_h
                ans_str = str(ans)
                unidad = rng.choice(["cm", "m"])
                
                errores_previstos[str(ext+int_h)] = "Sumaste las áreas. Recuerda que el hueco interior debe RESTARSE."
                
                # SVG: marco exterior con hueco interior
                svg_frame = (
                    f"<svg width='200' height='180' viewBox='-10 -10 220 200' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                    f"  <rect x='10' y='10' width='180' height='140' fill='#BAE6FD' fill-opacity='0.7' stroke='#1E293B' stroke-width='2.5'/>"
                    f"  <rect x='50' y='40' width='100' height='80' fill='#FFFFFF' stroke='#1E293B' stroke-width='2' stroke-dasharray='5,3'/>"
                    f"  <text x='100' y='28' fill='#1E293B' font-size='18' font-weight='bold' text-anchor='middle'>Ext = {ext} {unidad}²</text>"
                    f"  <text x='100' y='83' fill='#64748B' font-size='16' font-weight='bold' text-anchor='middle'>hueco</text>"
                    f"  <text x='100' y='97' fill='#64748B' font-size='16' text-anchor='middle'>{int_h} {unidad}²</text>"
                    f"  <text x='100' y='165' fill='#FFFFFF' font-size='16' text-anchor='middle'>Sombreado = {ext} - {int_h}</text>"
                    f"</svg>"
                )
                
                templates = [
                    f"{nombre} construyó un marco rectangular con área exterior de {ext} {unidad}² y hueco interior de {int_h} {unidad}² para colocar una foto. ¿Cuál es el área sombreada del marco en {unidad}²?<br/>{svg_frame}",
                    f"Una pared rectangular tiene un área de {ext} {unidad}². Si {nombre} coloca una ventana que ocupa {int_h} {unidad}², ¿cuál es el área de la pared alrededor de la ventana en {unidad}²?<br/>{svg_frame}",
                    f"En una tarjeta rectangular de área {ext} {unidad}², {nombre} recortó un cuadrado interior de área {int_h} {unidad}². ¿Qué área de cartulina quedó en {unidad}²?<br/>{svg_frame}"
                ]
                enunciado = rng.choice(templates)
                
                return {
                    "enunciado": enunciado,
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": f"Restamos el área interior (hueco) del área total exterior: {ext} - {int_h} = {ans} unidades cuadradas.",
                    "alts": [ans_str, str(ext+int_h), str(ans+5), str(ans-5)]
                }
    else:
        # Escala, diagonal y superficie
        if lvl_id == 1:
            scale = rng.choice([2, 5, 10, 20])
            u = rng.randint(3, 12)
            ans = u * scale
            ans_str = str(ans)
            escenario_e = rng.choice(ESCENARIOS_E)
            unidad = rng.choice(["cm", "mm"])
            
            errores_previstos[str(u+scale)] = "Sumaste la medida con la escala. Debes multiplicar para aplicar la escala."
            
            # SVG: mapa simplificado con regla de escala y segmento medido
            bar_w = u * 12
            svg_scale = (
                f"<svg width='240' height='160' viewBox='-10 -10 260 180' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                f"  <rect x='10' y='10' width='220' height='120' fill='#FEF3C7' fill-opacity='0.4' rx='6'/>"
                f"  <line x1='20' y1='70' x2='{20+bar_w}' y2='70' stroke='#1E293B' stroke-width='3' stroke-linecap='round'/>"
                f"  <line x1='20' y1='60' x2='20' y2='80' stroke='#1E293B' stroke-width='2'/>"
                f"  <line x1='{20+bar_w}' y1='60' x2='{20+bar_w}' y2='80' stroke='#1E293B' stroke-width='2'/>"
                f"  <text x='{20+bar_w//2}' y='58' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='middle'>{u} {unidad}</text>"
                f"  <rect x='20' y='90' width='80' height='20' fill='#FDE68A' rx='3' stroke='#92400E' stroke-width='1'/>"
                f"  <text x='60' y='104' fill='#92400E' font-size='15' font-weight='bold' text-anchor='middle'>1 {unidad} = {scale}</text>"
                f"  <text x='130' y='104' fill='#FFFFFF' font-size='16' text-anchor='start'>→ × {scale}</text>"
                f"  <text x='120' y='130' fill='#FFFFFF' font-size='16' text-anchor='middle'>Real = {u} × {scale} = ?</text>"
                f"</svg>"
            )
            
            templates = [
                f"{nombre} observa un {escenario_e} con escala 1 {unidad} = {scale} {unidad} reales. Una calle mide {u} {unidad} en el plano. ¿Cuál es su longitud real en {unidad}?<br/>{svg_scale}",
                f"En el {escenario_e} de {nombre}, la escala indica que 1 {unidad} del dibujo son {scale} {unidad} de la realidad. Una ruta mide {u} {unidad} en el plano. ¿Cuál es la distancia real en {unidad}?<br/>{svg_scale}",
                f"La maqueta de {nombre} tiene escala 1 : {scale}. Un edificio mide {u} {unidad} en la maqueta. ¿Cuál es su altura real en {unidad}?<br/>{svg_scale}"
            ]
            enunciado = rng.choice(templates)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": f"Multiplicamos las unidades del plano por la escala: {u} × {scale} = {ans}.",
                "alts": [ans_str, str(u+scale), str(ans+u), str(ans-scale)]
            }
        elif lvl_id == 2:
            # Modelado de diagonal / TV (con opción de Pitágoras)
            # Antes: 3/4 de las preguntas eran la MISMA idea conceptual ("se mide en
            # diagonal") y Pitágoras solo tenía 3 ternas. Ahora: 40% conceptual con
            # objetos y tamaños variados, 60% cálculo de Pitágoras con 10 ternas.
            case = rng.choice([1, 2, 3, 4, 5])
            # SVG TV/pantalla con diagonal destacada
            svg_tv = (
                "<svg width='240' height='170' viewBox='-10 -10 260 190' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                "  <rect x='20' y='20' width='200' height='120' rx='8' fill='#1E293B' stroke='#64748B' stroke-width='2'/>"
                "  <rect x='30' y='28' width='180' height='104' rx='4' fill='#0EA5E9' fill-opacity='0.2'/>"
                "  <line x1='30' y1='28' x2='210' y2='132' stroke='#F59E0B' stroke-width='3' stroke-linecap='round'/>"
                "  <text x='128' y='82' fill='#F59E0B' font-size='18' font-weight='bold' transform='rotate(-30 128 82)'>diagonal</text>"
                "  <text x='120' y='158' fill='#475569' font-size='16' text-anchor='middle'>← base →</text>"
                "</svg>"
            )
            if case in (1, 2):
                objeto = rng.choice(["un televisor", "un celular", "una tableta", "un monitor de PC",
                                     "una laptop", "una consola portátil", "un marco de foto digital"])
                pulg = rng.choice([6, 8, 10, 13, 15, 24, 27, 32, 42, 50, 55, 65])
                ans_str = "la diagonal"
                templates = [
                    f"Cuando {nombre} compra {objeto} de {pulg} pulgadas, ¿qué línea de la pantalla mide exactamente esas {pulg} pulgadas?<br/>{svg_tv}",
                    f"{objeto.capitalize()} se anuncia con pantalla de {pulg} pulgadas. ¿Qué parte de la pantalla corresponde a esa medida?<br/>{svg_tv}",
                    f"El tamaño de {objeto} es {pulg} pulgadas. {nombre} sabe que ese valor es la medida de:<br/>{svg_tv}",
                ]
                enunciado = rng.choice(templates)
                return {
                    "enunciado": enunciado,
                    "respuesta_correcta": ans_str,
                    "errores_previstos": {"la base": "El tamaño en pulgadas NO es la base, es la línea que cruza en diagonal.",
                                          "la altura": "El tamaño en pulgadas NO es la altura, es la diagonal."},
                    "expl": "El tamaño de las pantallas se mide en pulgadas a lo largo de su diagonal (esquina a esquina).",
                    "alts": ["la diagonal", "la base", "la altura", "el perímetro"]
                }
            else:
                # Caso Pitágoras: 10 ternas pitagóricas, base/altura intercambiables.
                triplet = rng.choice([
                    (3, 4, 5), (6, 8, 10), (9, 12, 15), (12, 16, 20), (15, 20, 25),
                    (5, 12, 13), (8, 15, 17), (7, 24, 25), (10, 24, 26), (18, 24, 30),
                ])
                a, b, ans = triplet
                if rng.random() < 0.5:
                    a, b = b, a  # intercambia base y altura para más variedad visual
                ans_str = str(ans)
                unidad = rng.choice(["cm", "m", "pulg"])
                # SVG rectángulo con catetos y diagonal etiquetados
                scale_svg = min(100 // max(a, b), 16)
                rw, rh = a * scale_svg, b * scale_svg
                svg_pyt = (
                    f"<svg width='220' height='160' viewBox='-10 -10 {rw+80} {rh+80}' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                    f"  <rect x='10' y='10' width='{rw}' height='{rh}' fill='#E0F2FE' fill-opacity='0.8' stroke='#1E293B' stroke-width='2'/>"
                    f"  <line x1='10' y1='10' x2='{10+rw}' y2='{10+rh}' stroke='#F59E0B' stroke-width='2.5' stroke-dasharray='5,3'/>"
                    f"  <text x='{10+rw//2}' y='{10+rh+18}' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='middle'>{a} {unidad}</text>"
                    f"  <text x='{10+rw+12}' y='{10+rh//2}' fill='#FFFFFF' font-size='18' font-weight='bold' text-anchor='start'>{b} {unidad}</text>"
                    f"  <text x='{10+rw//2+8}' y='{10+rh//2-8}' fill='#F59E0B' font-size='16' font-weight='bold' text-anchor='middle' transform='rotate({int(45)} {10+rw//2+8} {10+rh//2-8})'>d=?</text>"
                    f"</svg>"
                )
                objeto = rng.choice(["una pantalla rectangular", "una tableta", "un monitor", "un televisor",
                                     "una ventana rectangular", "un cuadro", "una pancarta", "un tablero"])
                templates = [
                    f"{nombre} mide la base ({a} {unidad}) y la altura ({b} {unidad}) de {objeto}. ¿Cuál es su diagonal en {unidad}?<br/>{svg_pyt}",
                    f"{objeto.capitalize()} tiene base de {a} {unidad} y altura de {b} {unidad}. ¿Cuánto mide su diagonal en {unidad}?<br/>{svg_pyt}",
                    f"Para {objeto} con base {a} {unidad} y altura {b} {unidad}, {nombre} calcula la medida diagonal. ¿Cuál es?<br/>{svg_pyt}",
                ]
                enunciado = rng.choice(templates)
                errores_previstos[str(a+b)] = "Sumaste la base y la altura. La diagonal se calcula con Pitágoras (a² + b² = c²), no sumando."
                dedup_alts = list(dict.fromkeys([ans_str, str(a+b), str(ans+2), str(max(a,b)+1), str(ans-1)]))
                return {
                    "enunciado": enunciado,
                    "respuesta_correcta": ans_str,
                    "errores_previstos": errores_previstos,
                    "expl": f"Usamos Pitágoras: {a}² + {b}² = {a*a} + {b*b} = {a*a+b*b}. La raíz cuadrada de {a*a+b*b} es {ans} {unidad}.",
                    "alts": dedup_alts[:4]
                }
        else:
            # Conversión de unidades de superficie
            case = rng.choice([1, 2, 3])
            m2 = rng.randint(1, 8)
            # SVG: cuadrado con conversión de unidades de superficie
            svg_m2 = (
                f"<svg width='240' height='160' viewBox='-10 -10 260 180' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                f"  <rect x='20' y='15' width='100' height='100' fill='#BAE6FD' fill-opacity='0.7' stroke='#1E293B' stroke-width='2'/>"
                f"  <text x='70' y='15' fill='#FFFFFF' font-size='16' text-anchor='middle'>1 m</text>"
                f"  <text x='15' y='68' fill='#FFFFFF' font-size='16' text-anchor='middle' transform='rotate(-90 15 68)'>1 m</text>"
                f"  <text x='70' y='72' fill='#1E293B' font-size='14' font-weight='bold' text-anchor='middle'>1 m²</text>"
                f"  <text x='145' y='68' fill='#FFFFFF' font-size='22' text-anchor='middle'>=</text>"
                f"  <text x='200' y='55' fill='#0EA5E9' font-size='18' font-weight='bold' text-anchor='middle'>10,000</text>"
                f"  <text x='200' y='72' fill='#0EA5E9' font-size='16' text-anchor='middle'>cm²</text>"
                f"  <text x='200' y='90' fill='#94A3B8' font-size='15' text-anchor='middle'>(100cm × 100cm)</text>"
                f"</svg>"
            )
            if case == 1:
                ans = m2 * 10000
                ans_str = str(ans)
                templates = [
                    f"{nombre} quiere saber: ¿Cuántos cm² equivalen a {m2} m²?<br/>{svg_m2}",
                    f"Un piso de {m2} m² es remodelado por {nombre}. ¿A cuántos cm² equivale?<br/>{svg_m2}",
                    f"Para cubrir {m2} m² con mosaicos, {nombre} necesita saber cuántos cm² son. ¿Cuál es la conversión?<br/>{svg_m2}"
                ]
                expl = f"Como 1 m² = 10,000 cm², multiplicamos {m2} × 10,000 = {ans} cm²."
                alts = [ans_str, str(m2*100), str(m2*1000), str(m2*100000)]
            elif case == 2:
                svg_dm2 = (
                    f"<svg width='240' height='160' viewBox='-10 -10 260 180' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                    f"  <rect x='20' y='15' width='100' height='100' fill='#BBF7D0' fill-opacity='0.7' stroke='#1E293B' stroke-width='2'/>"
                    f"  <text x='70' y='13' fill='#FFFFFF' font-size='16' text-anchor='middle'>1 dm</text>"
                    f"  <text x='15' y='68' fill='#FFFFFF' font-size='16' text-anchor='middle' transform='rotate(-90 15 68)'>1 dm</text>"
                    f"  <text x='70' y='72' fill='#1E293B' font-size='14' font-weight='bold' text-anchor='middle'>1 dm²</text>"
                    f"  <text x='145' y='68' fill='#FFFFFF' font-size='22' text-anchor='middle'>=</text>"
                    f"  <text x='200' y='55' fill='#4ADE80' font-size='18' font-weight='bold' text-anchor='middle'>100</text>"
                    f"  <text x='200' y='72' fill='#4ADE80' font-size='16' text-anchor='middle'>cm²</text>"
                    f"  <text x='200' y='90' fill='#94A3B8' font-size='15' text-anchor='middle'>(10cm × 10cm)</text>"
                    f"</svg>"
                )
                ans = m2 * 100
                ans_str = str(ans)
                templates = [
                    f"Una alfombra de {m2} dm² va a ser cortada por {nombre}. ¿A cuántos cm² equivale?<br/>{svg_dm2}",
                    f"¿Cuántos centímetros cuadrados hay en {m2} dm²?<br/>{svg_dm2}",
                    f"{nombre} pinta una tarjeta de {m2} dm². ¿Cuál es su área en cm²?<br/>{svg_dm2}"
                ]
                expl = f"Como 1 dm² = 100 cm², multiplicamos {m2} × 100 = {ans} cm²."
                alts = [ans_str, str(m2*10), str(m2*1000), str(m2*10000)]
            else:
                svg_m2dm2 = (
                    f"<svg width='240' height='160' viewBox='-10 -10 260 180' style='margin:8px auto;display:block;background:#111827;border:1.5px solid #E5E7EB;border-radius:10px;'>"
                    f"  <rect x='20' y='15' width='100' height='100' fill='#FEF9C3' fill-opacity='0.7' stroke='#1E293B' stroke-width='2'/>"
                    f"  <text x='70' y='13' fill='#FFFFFF' font-size='16' text-anchor='middle'>1 m</text>"
                    f"  <text x='15' y='68' fill='#FFFFFF' font-size='16' text-anchor='middle' transform='rotate(-90 15 68)'>1 m</text>"
                    f"  <text x='70' y='72' fill='#1E293B' font-size='14' font-weight='bold' text-anchor='middle'>1 m²</text>"
                    f"  <text x='145' y='68' fill='#FFFFFF' font-size='22' text-anchor='middle'>=</text>"
                    f"  <text x='200' y='55' fill='#FBBF24' font-size='18' font-weight='bold' text-anchor='middle'>100</text>"
                    f"  <text x='200' y='72' fill='#FBBF24' font-size='16' text-anchor='middle'>dm²</text>"
                    f"  <text x='200' y='90' fill='#94A3B8' font-size='15' text-anchor='middle'>(10dm × 10dm)</text>"
                    f"</svg>"
                )
                ans = m2 * 100
                ans_str = str(ans)
                templates = [
                    f"{nombre} compró un terreno de {m2} m². ¿A cuántos dm² equivale?<br/>{svg_m2dm2}",
                    f"¿Cuántos dm² equivalen a {m2} m²?<br/>{svg_m2dm2}",
                    f"Un jardín rectangular mide {m2} m². ¿A cuántos dm² equivale para {nombre}?<br/>{svg_m2dm2}"
                ]
                expl = f"Como 1 m² = 100 dm², multiplicamos {m2} × 100 = {ans} dm²."
                alts = [ans_str, str(m2*10), str(m2*1000), str(m2*10000)]
                
            enunciado = rng.choice(templates)
            errores_previstos[str(m2*100)] = "Multiplicaste por 100 como si fuera longitud lineal. En área (m² a cm²) debes multiplicar por 100x100 (10,000)."
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "alts": alts
            }

async def seed_practica_pool(session: AsyncSession):
    print("Sembrando pool de práctica Fase 5...")
    sections = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 2), (2, 3),
        (3, 1), (3, 2), (3, 3), (3, 4),
        (4, 1), (4, 2), (4, 3)
    ]
    
    for mod_id, lvl_id in sections:
        seccion_id = mod_id * 100 + lvl_id
        for i in range(120):
            rng = random.Random(FASE5_ID * 100000 + seccion_id * 1000 + i)
            q_data = await _gen_fase5_pool(rng, mod_id, lvl_id)
            
            
            datos_finales = {"fase5": True}
            if "datos_numericos" in q_data:
                datos_finales.update(q_data["datos_numericos"])

            # BUG CRÍTICO (mismo patrón que Fase 6/7/8): el progreso de práctica libre
            # cuenta familias vía COUNT(DISTINCT estructura_padre_id), pero antes esta
            # columna quedaba NULL en las 1560 preguntas de práctica → COUNT(DISTINCT NULL)=0
            # → el nivel NUNCA llegaba a 100% (BD: 0 aprobados históricos en toda la Fase 5;
            # el "PROGRESO 0/10" de la captura del usuario era justamente esto). Cada pregunta
            # ya es única (seed determinístico por índice) → familia propia de 1 miembro.
            estructura_padre_id = f"f5_m{mod_id}_l{lvl_id}_q{i:03d}"

            # Si la respuesta es de TEXTO (p.ej. "la diagonal", "infinitos"), debe ser
            # opción múltiple: el teclado numérico del frontend no permite escribir texto
            # (bug preexistente: la sección 402 tenía 56 preguntas "la diagonal" imposibles
            # de responder). El desafío ya hacía esta distinción; la práctica no.
            _resp = q_data["respuesta_correcta"]
            _es_numerica = _resp.lstrip('-').replace('.', '', 1).replace(',', '', 1).isdigit()
            _tipo = TipoPreguntaEnum.RESPUESTA_NUMERICA if _es_numerica else TipoPreguntaEnum.MULTIPLE_OPCION

            p = Pregunta(
                fase_id=FASE5_ID, seccion=seccion_id, estructura_padre_id=estructura_padre_id,
                operacion=OperacionEnum.MIXTA,
                tipo_pregunta=_tipo, enunciado=q_data["enunciado"],
                respuesta_correcta=q_data["respuesta_correcta"], datos_numericos=datos_finales,
                errores_previstos=q_data.get("errores_previstos", {}),
                explicacion_paso_a_paso={"titulo": "Resolución", "pasos": [{"orden": 1, "texto": q_data["expl"]}]},
                estado=StatusEnum.ACTIVO
            )
            for idx, alt in enumerate(q_data["alts"]):
                is_correct = (alt == q_data["respuesta_correcta"])
                error_msg = q_data.get("errores_previstos", {}).get(alt, "Esa alternativa es incorrecta.") if not is_correct else None
                p.alternativas.append(Alternativa(texto=alt, es_correcta=is_correct, orden=idx+1, tipo_error=TipoErrorEnum.CALCULO if not is_correct else None, feedback_error=error_msg))
            session.add(p)
    await session.commit()

async def seed_preguntas_desafios(session: AsyncSession):
    print("Sembrando pool de Desafíos de Fase 5 (30 preguntas por desafío)...")
    for modulo_id in range(1, 5):
        for desafio_id in (11, 12, 13):
            seccion_id = modulo_id * 1000 + desafio_id
            
            for idx in range(1, 31):
                rng = random.Random(FASE5_ID * 1000000 + seccion_id * 1000 + idx)
                lvl_id_desafio = desafio_id - 10
                q_data = await _gen_fase5_pool(rng, modulo_id, lvl_id_desafio)
                
                tipo_pregunta = TipoPreguntaEnum.MULTIPLE_OPCION if desafio_id in (11, 12) else TipoPreguntaEnum.RESPUESTA_NUMERICA
                # Bug: antes forzaba "la diagonal" (respuesta de TEXTO) a RESPUESTA_NUMERICA,
                # imposible de escribir en el teclado numérico. Cualquier respuesta no numérica
                # debe ser opción múltiple.
                _resp_d = q_data["respuesta_correcta"]
                if not _resp_d.lstrip('-').replace('.', '', 1).replace(',', '', 1).isdigit():
                    tipo_pregunta = TipoPreguntaEnum.MULTIPLE_OPCION
                
                datos_finales = {"es_desafio": True}
                if "datos_numericos" in q_data:
                    datos_finales.update(q_data["datos_numericos"])
                
                p = Pregunta(
                    fase_id=FASE5_ID, seccion=seccion_id, operacion=OperacionEnum.MIXTA,
                    tipo_pregunta=tipo_pregunta, enunciado=q_data["enunciado"],
                    respuesta_correcta=q_data["respuesta_correcta"], datos_numericos=datos_finales,
                    errores_previstos=q_data.get("errores_previstos", {}),
                    explicacion_paso_a_paso={"titulo": "Desafío", "pasos": [{"orden": 1, "texto": q_data["expl"]}]},
                    estado=StatusEnum.ACTIVO
                )
                
                if tipo_pregunta == TipoPreguntaEnum.MULTIPLE_OPCION:
                    for idx_alt, alt in enumerate(q_data["alts"]):
                        is_correct = (alt == q_data["respuesta_correcta"])
                        error_msg = q_data.get("errores_previstos", {}).get(alt, "Esa alternativa es incorrecta.") if not is_correct else None
                        p.alternativas.append(Alternativa(texto=alt, es_correcta=is_correct, orden=idx_alt+1, tipo_error=TipoErrorEnum.CALCULO if not is_correct else None, feedback_error=error_msg))
                session.add(p)
    await session.commit()
async def seed_configuracion_progreso(session: AsyncSession):
    print("Sembrando configuraciones de progreso Fase 5...")
    
    # 1. Configuración por defecto de la Fase
    config_def = ConfiguracionProgreso(
        fase_id=FASE5_ID, seccion=0, operacion=OperacionEnum.MIXTA,
        cantidad_requerida=15, porcentaje_aprobacion=90, orden_desbloqueo=99,
        tipo_feedback="simple", usa_cronometro=True, tiempo_default_segundos=60
    )
    session.add(config_def)
    
    # 2. Configuraciones de Niveles de Práctica Libre
    sections = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 2), (2, 3),
        (3, 1), (3, 2), (3, 3), (3, 4),
        (4, 1), (4, 2), (4, 3)
    ]
    for mod_id, lvl_id in sections:
        seccion_id = mod_id * 100 + lvl_id
        config = ConfiguracionProgreso(
            fase_id=FASE5_ID, seccion=seccion_id, operacion=OperacionEnum.MIXTA,
            cantidad_requerida=10, porcentaje_aprobacion=80, orden_desbloqueo=seccion_id,
            tipo_feedback="completo", usa_cronometro=False, tiempo_default_segundos=0
        )
        session.add(config)
        
    # 3. Configuraciones de Desafíos por Módulo
    for mod_id in range(1, 5):
        # Desafío 11
        config_11 = ConfiguracionProgreso(
            fase_id=FASE5_ID, seccion=mod_id * 1000 + 11, operacion=OperacionEnum.MIXTA,
            cantidad_requerida=20, porcentaje_aprobacion=90, orden_desbloqueo=mod_id * 1000 + 11,
            tipo_feedback="simple", usa_cronometro=True, tiempo_default_segundos=25
        )
        session.add(config_11)
        # Desafío 12
        config_12 = ConfiguracionProgreso(
            fase_id=FASE5_ID, seccion=mod_id * 1000 + 12, operacion=OperacionEnum.MIXTA,
            cantidad_requerida=20, porcentaje_aprobacion=90, orden_desbloqueo=mod_id * 1000 + 12,
            tipo_feedback="simple", usa_cronometro=True, tiempo_default_segundos=40
        )
        session.add(config_12)
        # Desafío 13
        config_13 = ConfiguracionProgreso(
            fase_id=FASE5_ID, seccion=mod_id * 1000 + 13, operacion=OperacionEnum.MIXTA,
            cantidad_requerida=10, porcentaje_aprobacion=90, orden_desbloqueo=mod_id * 1000 + 13,
            tipo_feedback="simple", usa_cronometro=True, tiempo_default_segundos=50
        )
        session.add(config_13)
        
    await session.commit()

async def run_fase5_seed():
    print("=" * 60)
    print("Iniciando inyección de datos semilla de Fase 5...")
    from app.seed import should_seed_phase, update_seed_version, SEED_VERSIONS
    async with AsyncSessionLocal() as session:
        if not await should_seed_phase(session, "fase_5", FASE5_ID):
            return
        
        res = await session.execute(select(Fase).where(Fase.id == FASE5_ID))
        if not res.scalar_one_or_none():
            fase = Fase(id=FASE5_ID, nombre="Geometría Plana y Medidas", descripcion="Desarrollar la comprensión del espacio bidimensional mediante el análisis visual y la conservación de la superficie.", orden=5, estado=StatusEnum.ACTIVO)
            session.add(fase)
            await session.flush()
            
        await clear_fase5_data(session)
        await seed_teoria_niveles(session)
        await seed_configuracion_progreso(session)
        await seed_practica_pool(session)
        await seed_preguntas_desafios(session)
        await update_seed_version(session, "fase_5", SEED_VERSIONS.get("fase_5", "20260603_v1"))
        await session.commit()
    print("Fase 5 inyectada con éxito!")

if __name__ == "__main__":
    asyncio.run(run_fase5_seed())

