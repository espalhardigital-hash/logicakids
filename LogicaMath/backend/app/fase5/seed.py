import asyncio
import math
import sys
import random
import json
import traceback
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from sqlalchemy import select, and_, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

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
    IntentoPregunta,
    PoolAsignadoAlumno,
)
from app.fase2.models import NivelTeoria
from app.fase4.theory_examples import obtener_ejemplos_expandidos_fase4

# ID de la Fase 4 en la base de datos
FASE5_ID = 5

# --- DICCIONARIOS DE CONTEXTO FASE 4 ---
NOMBRES = [
    "Lucas", "Sofía", "Mateo", "Valeria", "Diego", "Camila", "Leo", "Emma",
    "Valentina", "Santiago", "Isabella", "Sebastián", "Mariana", "Alejandro",
    "Daniela", "Nicolás", "Gabriela", "Samuel", "Victoria", "Joaquín",
    "Lucía", "Felipe", "Martina", "Tomás", "Elena", "Andrés", "Clara"
]
OBJETOS_FRACC = [
    "pizza", "torta", "barra de chocolate", "cartulina", "lámina",
    "pastel de fresa", "sandía fresca", "tableta de turrón", "hoja de papel",
    "bandera de papel", "mosaico de vidrio", "tablero de madera", "pan de molde",
    "queso redondo", "pie de manzana"
]
COLECCIONES = [
    "tazos", "cartas", "manzanas", "monedas de oro", "figuritas",
    "canicas brillantes", "pegatinas de dinosaurio", "libros de cuentos",
    "conchas de mar", "botones de colores", "estrellas de plástico", "sellos postales"
]
BEBIDAS = [
    "tazas de café", "vasos de jugo", "botellas de agua", "tazas de té",
    "vasos de leche", "tazas de chocolate caliente", "vasos de limonada",
    "batidos de fresa", "copas de helado", "tazas de mate"
]
PINTURAS = [
    "azul", "rojo", "amarillo", "blanco", "verde", "rosa",
    "morado", "naranja", "marrón", "gris", "celeste", "turquesa"
]
COLORES = [
    "rojas", "verdes", "azules", "amarillas", "moradas",
    "rosadas", "naranjas", "blancas", "negras", "marrones"
]

class NivelTeoriaSeederSchema(BaseModel):
    modulo_id: int
    nivel_id: int
    titulo: str
    texto_descubrimiento: str
    diccionario: Dict[str, str]
    advertencia: str
    ejemplos: List[Dict[str, Any]]
    interactivos: List[Dict[str, Any]] = Field(..., min_items=3, max_items=3)

async def clear_fase4_data(session: AsyncSession):
    print("Purging existing Fase 4 data for quick iteration (Overwrite)...")
    
    # Get all question IDs for Phase 4
    result = await session.execute(select(Pregunta.id).where(Pregunta.fase_id == FASE5_ID))
    pregunta_ids_list = result.scalars().all()
    
    # 1. Delete dependent entities first (Intentos, Pools)
    if pregunta_ids_list:
        await session.execute(delete(IntentoPregunta).where(IntentoPregunta.pregunta_id.in_(pregunta_ids_list)))
        await session.execute(delete(Intento).where(Intento.pregunta_id.in_(pregunta_ids_list)))
        await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.pregunta_id.in_(pregunta_ids_list)))
        
    await session.execute(delete(Intento).where(Intento.fase_id == FASE5_ID))
    await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE5_ID))
    
    # 2. Delete Alternativas now that they are no longer referenced by Intentos
    if pregunta_ids_list:
        await session.execute(delete(Alternativa).where(Alternativa.pregunta_id.in_(pregunta_ids_list)))
    
    # 3. Delete main questions
    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE5_ID))
    
    # 4. Delete progress config and theory
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE5_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE5_ID))
    
    await session.commit()
    print("Fase 4 data purged.")

async def seed_teoria_niveles(session: AsyncSession):
    print("Sembrando NivelTeoria para Fase 4...")
    
    niveles_teoria = [
        # --- MÓDULO 1: LA FRACCIÓN VISUAL ---
        # Nivel 1: Lectura y modelado en polígonos simétricos
        {
            "modulo_id": 1,
            "nivel_id": 1,
            "titulo": "Lectura de Fracciones",
            "texto_descubrimiento": "¡Hola, pequeña gran matemática! 🌟 ¿Sabías que los números pueden vestirse de astronautas y partir cosas por la mitad? Las fracciones nos ayudan a representar 'pedacitos' de un total delicioso, como una pizza o un chocolate. En este viaje, el de abajo (Denominador) es el cortador oficial de partes idénticas, y el de arriba (Numerador) es el que cuenta cuántas porciones te vas a comer o pintar. ¡A explorar!",
            "diccionario": {
                "Numerador": "Número de partes coloreadas o seleccionadas de la unidad.",
                "Denominador": "Número total de partes idénticas en las que se divide el todo."
            },
            "advertencia": "El total de partes (pintadas y no pintadas) va abajo. Si una pizza se corta en 8 rebanadas y tomas 3, la fracción es 3/8, no 3/5.",
            "ejemplos": obtener_ejemplos_expandidos_fase4(1, 1),
            "interactivos": [
                {
                    "enunciado": "Un círculo está dividido en 5 partes iguales y 2 están sombreadas. ¿Qué fracción representa? (Escribe en formato N/D)",
                    "respuesta": "2/5",
                    "feedback_acierto": "¡Excelente! 2 partes de un total de 5 se escribe como 2/5.",
                    "feedback_error": "Cuenta todos los sectores para el de abajo (5) y los pintados para el de arriba (2)."
                },
                {
                    "enunciado": "Si pintas 4 partes de un rectángulo de 6 porciones simétricas, ¿qué fracción has coloreado?",
                    "respuesta": "4/6",
                    "feedback_acierto": "¡Muy bien! 4 de 6 porciones se escribe 4/6.",
                    "feedback_error": "El total de divisiones es 6 (denominador) y tomas 4 (numerador)."
                },
                {
                    "enunciado": "Un círculo tiene 4 partes y todas están coloreadas. ¿Qué fracción representa?",
                    "respuesta": "4/4",
                    "feedback_acierto": "¡Correcto! 4/4 es lo mismo que la unidad entera.",
                    "feedback_error": "Si tomas 4 partes de 4 disponibles, la fracción es 4/4."
                }
            ]
        },
        # Nivel 2: Construcción de equivalencias
        {
            "modulo_id": 1,
            "nivel_id": 2,
            "titulo": "Fracciones Equivalentes",
            "texto_descubrimiento": "¡Las fracciones son maestras del disfraz! 🎭 A veces, dos fracciones usan números distintos pero representan exactamente la misma porción o cantidad. A esto lo llamamos **fracciones equivalentes**. ¿La clave? Si multiplicamos o dividimos el numerador (arriba) y el denominador (abajo) por el **mismo número**, creamos un clon equivalente perfecto. En los ejemplos verás cómo 1/3 se convierte en 4/12 cuando dividimos cada franja en 4 partes más pequeñas, o cómo 3/8 se clona en 6/16. También descubrirás figuras hermosas como diamantes y molinillos en hexágonos que muestran cómo 1/2 es exactamente igual a 8/16 o a 6/12.",
            "diccionario": {
                "Amplificación": "Multiplicar numerador y denominador por el mismo número (factor de escala) para obtener una fracción equivalente con más partes.",
                "Equivalencia": "Fracciones con diferentes términos numéricos que ocupan exactamente la misma área o cantidad del todo."
            },
            "advertencia": "¡Cuidado! Un denominador más grande no significa que comas más. Significa que dividiste la unidad en pedazos más pequeños. ¡Por eso 1/8 es más pequeño que 1/2, aunque el 8 sea mayor que el 2!",
            "ejemplos": obtener_ejemplos_expandidos_fase4(1, 2),
            "interactivos": [
                {
                    "enunciado": "Encuentra la fracción equivalente a 1/2 si multiplicamos arriba y abajo por 3. (Formato N/D)",
                    "respuesta": "3/6",
                    "feedback_acierto": "¡Excelente! 1/2 y 3/6 representan exactamente la mitad.",
                    "feedback_error": "Multiplica 1 × 3 y 2 × 3 para encontrar el resultado."
                },
                {
                    "enunciado": "Amplifica 2/3 por un factor de 2. ¿Cuál es el clon equivalente?",
                    "respuesta": "4/6",
                    "feedback_acierto": "¡Bien hecho! 2/3 es equivalente a 4/6.",
                    "feedback_error": "Duplica tanto el numerador (2 × 2) como el denominador (3 × 2)."
                },
                {
                    "enunciado": "¿Qué fracción equivalente a 4/8 se obtiene si dividimos numerador y denominador entre 4?",
                    "respuesta": "1/2",
                    "feedback_acierto": "¡Perfecto! Simplificaste la fracción a su expresión más simple: 1/2.",
                    "feedback_error": "Divide 4 ÷ 4 y 8 ÷ 4."
                }
            ]
        },
        # Nivel 3: Áreas fraccionarias en composiciones geométricas asimétricas
        {
            "modulo_id": 1,
            "nivel_id": 3,
            "titulo": "Áreas y Asimetrías",
            "texto_descubrimiento": "¡Peligro, trampa en el camino! ⚠️ Para poder decir 'esta porción es 1/4' solo contando trozos, todas las divisiones deben ser del mismo tamaño, como los lados de un espejo. Si los cortes son desiguales (asimétricos), no puedes contar a ciegas. Tienes que usar tu súper visión geométrica para cortar mentalmente la figura en cuadritos iguales y descubrir la fracción real.",
            "diccionario": {
                "Simetría": "Porciones de forma y tamaño idénticos.",
                "Asimetría": "Partes de tamaños diferentes. Requiere subdivisión mental para hallar la fracción real."
            },
            "advertencia": "Si una figura está dividida en 4 y una de las partes es gigante, no puedes decir simplemente que cada porción es 1/4. ¡Primero debes igualar las áreas!",
            "ejemplos": obtener_ejemplos_expandidos_fase4(1, 3),
            "interactivos": [
                {
                    "enunciado": "Un cuadrado se divide en 2 rectángulos iguales por la mitad. ¿Qué fracción representa un rectángulo?",
                    "respuesta": "1/2",
                    "feedback_acierto": "¡Muy bien! Cada mitad es 1/2.",
                    "feedback_error": "Al ser dos partes idénticas, cada una representa 1/2."
                },
                {
                    "enunciado": "Un cuadrado de 4x4 cuadraditos tiene 8 pintados. ¿Qué fracción del total está pintada? (Simplificada, ej: 1/2)",
                    "respuesta": "1/2",
                    "feedback_acierto": "¡Exacto! 8 de 16 cuadraditos representa la mitad (1/2).",
                    "feedback_error": "Suma el total de cuadraditos (16) y los coloreados (8). Esto da 8/16, equivalente a 1/2."
                },
                {
                    "enunciado": "Si cortamos un círculo en 4 porciones, pero 2 de ellas son el triple de grandes que las otras, ¿son todas de 1/4?",
                    "respuesta": "no",
                    "feedback_acierto": "¡Correcto! En fracciones, todas las partes deben medir lo mismo.",
                    "feedback_error": "Responde 'sí' o 'no'. Las fracciones exigen que las partes sean exactamente iguales."
                }
            ]
        },
        
        # --- MÓDULO 2: FRACCIÓN DE CANTIDAD ---
        # Nivel 1: Cálculo de porciones unitarias (1/n) sobre grupos
        {
            "modulo_id": 2,
            "nivel_id": 1,
            "titulo": "Porciones de un Grupo",
            "texto_descubrimiento": "¡Las fracciones no solo cortan pizzas, también organizan grupos de juguetes, amigos o monedas! 🪙 Calcular 1/n de un grupo significa repartir tus objetos en n cajas iguales. Lo que quede en una sola caja es la porción unitaria. ¡Repartir es la clave de este truco!",
            "diccionario": {
                "Grupo Finito": "Un conjunto cerrado de unidades u objetos.",
                "Porción Unitaria": "El valor de una de las partes en que se divide el conjunto (1/n)."
            },
            "advertencia": "Para hallar 1/n de un número, simplemente divide el número total entre el denominador n.",
            "ejemplos": obtener_ejemplos_expandidos_fase4(2, 1),
            "interactivos": [
                {
                    "enunciado": "Calcula 1/4 de 16 caramelos.",
                    "respuesta": "4",
                    "feedback_acierto": "¡Correcto! 16 ÷ 4 = 4.",
                    "feedback_error": "Divide 16 entre 4."
                },
                {
                    "enunciado": "Si tienes 15 manzanas y regalas 1/3, ¿cuántas manzanas regalas?",
                    "respuesta": "5",
                    "feedback_acierto": "¡Muy bien! 1/3 de 15 es 5 manzanas.",
                    "feedback_error": "Divide el total de manzanas (15) entre 3."
                },
                {
                    "enunciado": "Calcula 1/5 de 40 monedas.",
                    "respuesta": "8",
                    "feedback_acierto": "¡Excelente! 40 ÷ 5 = 8.",
                    "feedback_error": "Divide 40 entre 5."
                }
            ]
        },
        # Nivel 2: Operador compuesto (m/n de X) y algoritmo de dos pasos
        {
            "modulo_id": 2,
            "nivel_id": 2,
            "titulo": "El Motor de Dos Pasos",
            "texto_descubrimiento": "¡Rumbo a los cálculos avanzados! 🚀 Si te piden 3/4 de 20 manzanas, encendemos el Motor de Dos Pasos:\nPaso 1: Divide tu total (20) entre el de abajo (4) para saber cuántos objetos caben en una caja. (20 ÷ 4 = 5).\nPaso 2: Multiplica el resultado por el de arriba (3) para reunir las cajas que necesitas. (5 × 3 = 15). ¡Listo!",
            "diccionario": {
                "Paso de División": "Dividir el total entre el denominador para armar grupos.",
                "Paso de Multiplicación": "Multiplicar por el numerador para tomar los grupos deseados."
            },
            "advertencia": "Siempre divide primero entre el número de abajo. Si intentas multiplicar primero, obtendrás números gigantescos difíciles de calcular.",
            "ejemplos": obtener_ejemplos_expandidos_fase4(2, 2),
            "interactivos": [
                {
                    "enunciado": "Calcula 3/4 de 24 cartas.",
                    "respuesta": "18",
                    "feedback_acierto": "¡Perfecto! 24 ÷ 4 = 6; luego 6 × 3 = 18.",
                    "feedback_error": "Primero divide 24 entre 4 (da 6), luego multiplica ese 6 por 3."
                },
                {
                    "enunciado": "Un cofre tiene 30 monedas. Tomas 2/3 de ellas. ¿Cuántas monedas tomas?",
                    "respuesta": "20",
                    "feedback_acierto": "¡Brillante! 30 ÷ 3 = 10; luego 10 × 2 = 20.",
                    "feedback_error": "Divide 30 entre 3, y el resultado lo multiplicas por 2."
                },
                {
                    "enunciado": "Calcula 4/5 de 50 tazos.",
                    "respuesta": "40",
                    "feedback_acierto": "¡Impresionante! 50 ÷ 5 = 10; luego 10 × 4 = 40.",
                    "feedback_error": "Divide 50 entre 5 y multiplica por 4."
                }
            ]
        },
        # Nivel 3: Lógica del complemento y deducción del resto
        {
            "modulo_id": 2,
            "nivel_id": 3,
            "titulo": "Lógica del Complemento",
            "texto_descubrimiento": "¡Las mentes ágiles usan atajos mentales! Si sabes que gastas 2/5 de tus ahorros, ¿cuántos te quedan? ¡Pues 3/5! 💡 No necesitas hacer cuentas largas. El total siempre equivale a la unidad completa (5/5). Si restas lo gastado, sabes al instante lo que queda. A esto lo llamamos la lógica del complemento.",
            "diccionario": {
                "Complemento": "La fracción necesaria para alcanzar la unidad entera.",
                "Fracción Restante": "Lo que queda después de restar la porción gastada o perdida."
            },
            "advertencia": "Presta atención a si la pregunta pide 'lo que se gastó' o 'lo que quedó'. ¡Ahí está la trampa!",
            "ejemplos": obtener_ejemplos_expandidos_fase4(2, 3),
            "interactivos": [
                {
                    "enunciado": "Si gastas 3/8 de tu dinero, ¿qué fracción te queda? (Formato N/D)",
                    "respuesta": "5/8",
                    "feedback_acierto": "¡Exacto! 8/8 - 3/8 = 5/8.",
                    "feedback_error": "Resta 3 de los 8 octavos totales para saber cuántos te quedan."
                },
                {
                    "enunciado": "Tenías 30 manzanas y regalaste 1/3. ¿Cuántas manzanas te QUEDAN?",
                    "respuesta": "20",
                    "feedback_acierto": "¡Deducción perfecta! Regalaste 10 (1/3), por lo tanto te quedan 20 (2/3).",
                    "feedback_error": "Calcula 1/3 de 30 (que es 10) y réstaselo al total de 30."
                },
                {
                    "enunciado": "Un tanque de 50 litros vacía 2/5 de su agua. ¿Cuántos litros de agua QUEDAN adentro?",
                    "respuesta": "30",
                    "feedback_acierto": "¡Espectacular! Se vaciaron 20 litros, así que quedan 30.",
                    "feedback_error": "Calcula 2/5 de 50 (que es 20) y réstaselo a los 50 iniciales."
                }
            ]
        },

        # --- MÓDULO 3: PORCENTAJES RÁPIDOS Y PROMEDIOS ---
        # Nivel 1: Mapeo de porcentajes intuitivos: 50%, 25%, 10%
        {
            "modulo_id": 3,
            "nivel_id": 1,
            "titulo": "Porcentajes Intuitivos",
            "texto_descubrimiento": "¡Bienvenida a los súper porcentajes! ⚡ Un porcentaje es solo una fracción elegante que usa el 100 como base. Para calcular rápido, apréndete estos atajos mentales:\n- El 50% es la mitad exacta (divide entre 2).\n- El 25% es una cuarta parte (divide entre 4).\n- El 10% es una décima parte (divide entre 10). ¡Hazlo en segundos!",
            "diccionario": {
                "Porcentaje": "Relación numérica expresada como fracción de 100 partes.",
                "Mapeo Rápido": "50% es dividir entre 2, 25% es dividir entre 4, y 10% es dividir entre 10."
            },
            "advertencia": "Para calcular el 10% de un número terminado en cero, simplemente eliminas el último cero.",
            "ejemplos": obtener_ejemplos_expandidos_fase4(3, 1),
            "interactivos": [
                {
                    "enunciado": "Calcula el 50% de 80.",
                    "respuesta": "40",
                    "feedback_acierto": "¡Excelente! La mitad de 80 es 40.",
                    "feedback_error": "50% significa la mitad. Divide 80 entre 2."
                },
                {
                    "enunciado": "Calcula el 25% de 120.",
                    "respuesta": "30",
                    "feedback_acierto": "¡Muy bien! Una cuarta parte de 120 es 30.",
                    "feedback_error": "25% equivale a dividir entre 4. Divide 120 entre 4."
                },
                {
                    "enunciado": "Calcula el 10% de 450.",
                    "respuesta": "45",
                    "feedback_acierto": "¡Perfecto! Quitamos el cero final y nos queda 45.",
                    "feedback_error": "10% es dividir entre 10. Divide 450 entre 10."
                }
            ]
        },
        # Nivel 2: Lectura e interpretación de gráficos circulares
        {
            "modulo_id": 3,
            "nivel_id": 2,
            "titulo": "Gráficos Circulares",
            "texto_descubrimiento": "¡Los gráficos circulares son pasteles de datos! 🎂 Cada rebanada representa un porcentaje de las preferencias de la gente. La regla de oro de estos gráficos es que, si sumas todas las porciones, el total siempre debe sumar 100%. Si conoces algunas rebanadas, ¡puedes averiguar la que falta restando de 100!",
            "diccionario": {
                "Gráfico Circular": "Diagrama de sectores para visualizar la proporción de cada categoría.",
                "Porcentaje de Sector": "La porción de pastel asignada a cada variable."
            },
            "advertencia": "Lee siempre los porcentajes con cuidado. Si el gráfico completo representa un total de personas, debes aplicar el porcentaje a ese total.",
            "ejemplos": obtener_ejemplos_expandidos_fase4(3, 2),
            "interactivos": [
                {
                    "enunciado": "En una encuesta del 100%, 45% prefiere chocolate, 30% vainilla y el resto frutilla. ¿Qué porcentaje prefiere frutilla?",
                    "respuesta": "25",
                    "feedback_acierto": "¡Correcto! 100% - 45% - 30% = 25%.",
                    "feedback_error": "Suma 45% y 30% y réstale el resultado a 100%."
                },
                {
                    "enunciado": "De un total de 400 personas, el 50% prefiere viajar en auto. ¿Cuántas personas son?",
                    "respuesta": "200",
                    "feedback_acierto": "¡Muy bien! El 50% de 400 es 200.",
                    "feedback_error": "50% es la mitad. Divide 400 entre 2."
                },
                {
                    "enunciado": "Si el 10% de un pastel representa 8 porciones, ¿de cuántas porciones era el pastel completo?",
                    "respuesta": "80",
                    "feedback_acierto": "¡Estupendo! Si 10% es 8, entonces el 100% es 8 × 10 = 80.",
                    "feedback_error": "Multiplica el valor del 10% por 10 para llegar al 100%."
                }
            ]
        },
        # Nivel 3: Comparación de tasas en gráficos de barras
        {
            "modulo_id": 3,
            "nivel_id": 3,
            "titulo": "Gráficos de Barras",
            "texto_descubrimiento": "¡Las barras son edificios de información! 🏢 La altura de cada barra nos dice el valor de una categoría de forma súper visual. Al mirar las alturas, puedes comparar qué barra es la más alta (el ganador), sumar varias barras para hallar un gran total, o restar sus alturas para ver por cuánto le gana una a otra.",
            "diccionario": {
                "Gráfico de Barras": "Diagrama que representa datos mediante columnas rectangulares.",
                "Eje Y": "La escala numérica vertical que define el valor de cada barra."
            },
            "advertencia": "Asegúrate de mirar bien las etiquetas del eje Y para no confundir las líneas de nivel.",
            "ejemplos": obtener_ejemplos_expandidos_fase4(3, 3),
            "interactivos": [
                {
                    "enunciado": "Tres barras marcan: A=100, B=150, C=50. ¿Cuál es el total acumulado entre las tres?",
                    "respuesta": "300",
                    "feedback_acierto": "¡Excelente! 100 + 150 + 50 = 300.",
                    "feedback_error": "Suma los tres valores de forma directa."
                },
                {
                    "enunciado": "Usando las barras anteriores: ¿cuánto más grande es la barra B que la barra C?",
                    "respuesta": "100",
                    "feedback_acierto": "¡Exacto! 150 - 50 = 100.",
                    "feedback_error": "Resta el valor de la barra C (50) de la barra B (150)."
                },
                {
                    "enunciado": "Si sumamos las barras A (100) y C (50), ¿es el total igual a la barra B?",
                    "respuesta": "sí",
                    "feedback_acierto": "¡Bien pensado! 100 + 50 = 150, que es igual a B.",
                    "feedback_error": "Responde 'sí' o 'no'. Compara (100 + 50) con 150."
                }
            ]
        },
        # Nivel 4: El Punto de Equilibrio - Media Aritmética
        {
            "modulo_id": 3,
            "nivel_id": 4,
            "titulo": "La Media Aritmética",
            "texto_descubrimiento": "¡Vamos a nivelar las cosas! ⚖️ Imagina que tienes tres torres de bloques de alturas diferentes y quieres que las tres queden a la misma altura. ¿El secreto? Junta todos los bloques en una gran pila central (Paso 1: Sumar) y luego repártelos en partes iguales entre las 3 torres (Paso 2: Dividir). ¡Eso es el promedio o media aritmética!",
            "diccionario": {
                "Promedio (Media)": "La suma de todos los valores dividida entre la cantidad de valores.",
                "Pila Única": "La suma acumulativa de todos los datos antes de dividir."
            },
            "advertencia": "No olvides realizar la división final. Si solo sumas los números, habrás completado la pila pero no la nivelación.",
            "ejemplos": obtener_ejemplos_expandidos_fase4(3, 4),
            "interactivos": [
                {
                    "enunciado": "Calcula el promedio de las puntuaciones: 4, 8 y 12.",
                    "respuesta": "8",
                    "feedback_acierto": "¡Correcto! (4 + 8 + 12) = 24; luego 24 ÷ 3 = 8.",
                    "feedback_error": "Suma los tres números y divide el resultado entre 3."
                },
                {
                    "enunciado": "Dos amigos gastan R$ 10 y R$ 20. ¿Cuál es el promedio de gasto entre los dos?",
                    "respuesta": "15",
                    "feedback_acierto": "¡Muy bien! (10 + 20) ÷ 2 = 15.",
                    "feedback_error": "Suma los dos gastos (30) y divide entre 2."
                },
                {
                    "enunciado": "En tres días llovió 6 mm, 6 mm y 12 mm. ¿Cuál es el promedio de lluvia diaria?",
                    "respuesta": "8",
                    "feedback_acierto": "¡Brillante! (6 + 6 + 12) = 24; luego 24 ÷ 3 = 8.",
                    "feedback_error": "Suma los milímetros (24) y divide entre los 3 días."
                }
            ]
        },

        # --- MÓDULO 4: RAZÓN Y MEZCLAS ---
        # Nivel 1: Razones simples (a:b) y proporcionalidad directa
        {
            "modulo_id": 4,
            "nivel_id": 1,
            "titulo": "Razones y Proporciones",
            "texto_descubrimiento": "Una **razón** es una comparación matemática entre dos cantidades mediante una división. Nos indica cuántas partes de un elemento se necesitan en relación con otro elemento. Por ejemplo, si una receta de limonada requiere 3 tazas de agua por cada 1 taza de zumo de limón, la razón es **3 a 1 (o 3:1)**.\n---\nPara preparar cantidades más grandes conservando el sabor original, aplicamos una **proporción**. Esto significa multiplicar o dividir ambos términos de la razón por un mismo número, al cual llamamos **factor de escala**. ¡Si duplicas la cantidad de limón, también debes duplicar la de agua para que la mezcla no se arruine!",
            "diccionario": {
                "Razón (a:b)": "La comparación matemática que relaciona dos cantidades e indica cuántas veces una contiene a la otra.",
                "Factor de Escala": "El multiplicador común por el cual aumentamos o disminuimos proporcionalmente todos los elementos de la mezcla."
            },
            "advertencia": "¡Cuidado! Una proporción se amplía multiplicando, nunca sumando. Si la receta es 3:1 y pasas a 2 de limón, debes multiplicar el agua por 2 (3 × 2 = 6). No le sumes simplemente 1.",
            "ejemplos": obtener_ejemplos_expandidos_fase4(4, 1),
            "interactivos": [
                {
                    "enunciado": "La receta es 3 tazas de agua por 1 de limón (3:1). Si pones 3 tazas de limón, ¿cuánta agua necesitas?",
                    "respuesta": "9",
                    "feedback_acierto": "¡Excelente! Multiplicaste la receta por 3. 3 × 3 = 9.",
                    "feedback_error": "Si triplicaste el limón (de 1 a 3), debes triplicar el agua (de 3 a 9)."
                },
                {
                    "enunciado": "Pintura rosa usa 1 litro de rojo por 4 de blanco (1:4). Si pones 2 litros de rojo, ¿cuánto blanco usas?",
                    "respuesta": "8",
                    "feedback_acierto": "¡Perfecto! Duplicaste el rojo, así que duplicas el blanco (4 × 2 = 8).",
                    "feedback_error": "Multiplica el blanco (4) por 2 ya que duplicaste el rojo."
                },
                {
                    "enunciado": "Una masa requiere 1 huevo por 3 tazas de harina. Si usas 9 tazas de harina, ¿cuántos huevos necesitas?",
                    "respuesta": "3",
                    "feedback_acierto": "¡Muy bien! Triplicaste la harina (de 3 a 9), así que necesitas 3 huevos.",
                    "feedback_error": "Divide 9 entre 3 para saber cuántas veces se amplió la receta."
                }
            ]
        },
        # Nivel 2: Reparto proporcional de volúmenes macro
        {
            "modulo_id": 4,
            "nivel_id": 2,
            "titulo": "Reparto de Volúmenes",
            "texto_descubrimiento": "Cuando necesitamos preparar una mezcla a gran escala pero solo conocemos la proporción de sus partes y el **volumen total deseado (volumen macro)**, aplicamos el reparto proporcional. Imagina que para obtener una pintura verde mezclamos 2 litros de azul y 3 de amarillo, lo que produce 5 litros de verde en total (la receta base).\n---\nSi un cliente nos pide 30 litros de verde, el cálculo es simple: primero sumamos las partes para hallar el rendimiento de la receta base (2 + 3 = 5 litros). Luego, dividimos el volumen total pedido entre el volumen de la receta base para obtener el factor de escala (30 ÷ 5 = 6 veces). Finalmente, multiplicamos cada ingrediente por este factor: 2 azul × 6 = 12 litros de azul, y 3 amarillo × 6 = 18 litros de amarillo.",
            "diccionario": {
                "Volumen Macro": "La cantidad total final requerida al juntar todos los componentes de la mezcla.",
                "Receta Base": "La suma de las partes iniciales de cada ingrediente, que indica cuánto produce una sola dosis de la mezcla."
            },
            "advertencia": "Suma primero todas las partes de la receta original para saber el total que rinde. Luego divide el volumen macro entre ese total para hallar tu factor de escala.",
            "ejemplos": obtener_ejemplos_expandidos_fase4(4, 2),
            "interactivos": [
                {
                    "enunciado": "Mezclas 2 litros de azul y 3 de amarillo (5L verde en total). Para hacer 15 litros de verde, ¿cuántos de azul usas?",
                    "respuesta": "6",
                    "feedback_acierto": "¡Muy bien! 15 ÷ 5 = 3 veces la receta. 2 azul × 3 = 6 litros.",
                    "feedback_error": "Divide 15 entre 5 para saber el multiplicador (3). Luego multiplica 2 por 3."
                },
                {
                    "enunciado": "Pintura rosa usa 1 de rojo y 4 de blanco (5L total). Para hacer 25 litros de rosa, ¿cuánto blanco necesitas?",
                    "respuesta": "20",
                    "feedback_acierto": "¡Correcto! 25 ÷ 5 = 5 lotes. 4 blanco × 5 = 20 litros.",
                    "feedback_error": "Divide 25 entre 5 para hallar el lote (5) y multiplica el blanco por 5."
                },
                {
                    "enunciado": "Concreto lleva 3 de arena y 7 de grava (10 en total). Para hacer 30 paladas de mezcla, ¿cuántas son de arena?",
                    "respuesta": "9",
                    "feedback_acierto": "¡Excelente! 30 ÷ 10 = 3 lotes. 3 arena × 3 = 9 paladas.",
                    "feedback_error": "Divide 30 entre 10 (da 3) y multiplica la arena (3) por 3."
                }
            ]
        },
        # Nivel 3: Homogeneización de mezclas complejas
        {
            "modulo_id": 4,
            "nivel_id": 3,
            "titulo": "Mezclas Complejas",
            "texto_descubrimiento": "En muchas mezclas es crucial determinar qué parte del volumen total representa un único ingrediente. Esto nos permite entender la **concentración** o **fracción de mezcla**. Por ejemplo, si mezclas 1 gota de esencia de flores con 4 gotas de alcohol, tendrás 5 gotas de perfume en total. La esencia representa 1 de las 5 partes totales (fracción 1/5).\n---\nSi convertimos esta fracción a porcentaje dividiendo 1 entre 5 y multiplicando por 100, descubrimos que la esencia representa el **20% del volumen total**. El porcentaje nos ayuda a comparar la concentración de diferentes sustancias de forma estandarizada y directa.",
            "diccionario": {
                "Fracción de Mezcla": "La relación matemática entre la cantidad de un ingrediente y el volumen total de la mezcla.",
                "Homogeneidad": "La propiedad por la cual los componentes de una mezcla están distribuidos de forma uniforme en cualquier porción."
            },
            "advertencia": "¡Ojo! La fracción de un ingrediente se calcula dividiendo su porción entre el TOTAL de todas las partes juntas, no entre la cantidad del otro ingrediente.",
            "ejemplos": obtener_ejemplos_expandidos_fase4(4, 3),
            "interactivos": [
                {
                    "enunciado": "Una mezcla tiene 1 parte de concentrado y 9 de agua (10 partes total). ¿Qué porcentaje es de concentrado? (Escribe el número, ej: 10)",
                    "respuesta": "10",
                    "feedback_acierto": "¡Perfecto! 1 de 10 partes equivale al 10%.",
                    "feedback_error": "La fracción es 1/10, multiplica por 100 para hallar el porcentaje."
                },
                {
                    "enunciado": "Un jugo de 200 ml contiene 25% de pulpa. ¿Cuántos ml de pulpa tiene?",
                    "respuesta": "50",
                    "feedback_acierto": "¡Excelente! 25% (un cuarto) de 200 es 50 ml.",
                    "feedback_error": "25% es dividir entre 4. Divide 200 entre 4."
                },
                {
                    "enunciado": "Si en 100 gramos de chocolate hay 10% de leche, ¿cuántos gramos son de chocolate puro?",
                    "respuesta": "90",
                    "feedback_acierto": "¡Brillante! Si 10% es leche, el 90% es chocolate puro. 90 gramos.",
                    "feedback_error": "Resta el 10% de leche (10g) del total de 100g."
                }
            ]
        }
    ]
    
    for t in niveles_teoria:
        # Validate using schema
        NivelTeoriaSeederSchema(**t)
        
        # Check if already exists
        result = await session.execute(
            select(NivelTeoria).where(and_(
                NivelTeoria.fase_id == FASE5_ID,
                NivelTeoria.modulo_id == t["modulo_id"],
                NivelTeoria.nivel_id == t["nivel_id"]
            ))
        )
        existing = result.scalar_one_or_none()
        if not existing:
            nt = NivelTeoria(
                fase_id=FASE5_ID,
                modulo_id=t["modulo_id"],
                nivel_id=t["nivel_id"],
                titulo=t["titulo"],
                texto_descubrimiento=t["texto_descubrimiento"],
                diccionario=t["diccionario"],
                advertencia=t["advertencia"],
                ejemplos=t["ejemplos"],
                interactivos=t["interactivos"]
            )
            session.add(nt)
    await session.commit()
    print("NivelTeoria para Fase 4 insertados exitosamente.")

async def seed_configuracion_progreso(session: AsyncSession):
    print("Sembrando ConfiguracionProgreso para Fase 4...")
    
    # Módulo 1 (La Fracción Visual): 3 niveles de práctica
    # Módulo 2 (Fracción de Cantidad): 3 niveles de práctica
    # Módulo 3 (Porcentajes Rápidos y Promedios): 4 niveles de práctica
    # Módulo 4 (Razón y Mezclas): 3 niveles de práctica
    
    configs = []
    orden = 1
    
    # ── MÓDULOS 1, 2, 4 (3 niveles cada uno) ──
    for m_id in [1, 2, 4]:
        for n_id in range(1, 4):
            configs.append({
                "seccion": m_id * 100 + n_id,
                "operacion": OperacionEnum.MIXTA,
                "cantidad_requerida": 15,
                "porcentaje_aprobacion": 90,
                "orden_desbloqueo": orden,
                "usa_cronometro": False,
                "tiempo_default_segundos": None,
                "tipo_feedback": "detallado"
            })
            orden += 1
            
        # Desafíos
        configs.append({
            "seccion": m_id * 1000 + 11,
            "operacion": OperacionEnum.MIXTA,
            "cantidad_requerida": 20,
            "porcentaje_aprobacion": 90,
            "orden_desbloqueo": orden,
            "usa_cronometro": True,
            "tiempo_default_segundos": 25,
            "tipo_feedback": "simple"
        })
        orden += 1
        configs.append({
            "seccion": m_id * 1000 + 12,
            "operacion": OperacionEnum.MIXTA,
            "cantidad_requerida": 20,
            "porcentaje_aprobacion": 90,
            "orden_desbloqueo": orden,
            "usa_cronometro": True,
            "tiempo_default_segundos": 40,
            "tipo_feedback": "simple"
        })
        orden += 1
        configs.append({
            "seccion": m_id * 1000 + 13,
            "operacion": OperacionEnum.MIXTA,
            "cantidad_requerida": 10,
            "porcentaje_aprobacion": 90,
            "orden_desbloqueo": orden,
            "usa_cronometro": True,
            "tiempo_default_segundos": 50,
            "tipo_feedback": "simple"
        })
        orden += 1

    # ── MÓDULO 3 (4 niveles de práctica) ──
    m_id = 3
    for n_id in range(1, 5):
        configs.append({
            "seccion": m_id * 100 + n_id,
            "operacion": OperacionEnum.MIXTA,
            "cantidad_requerida": 15,
            "porcentaje_aprobacion": 90,
            "orden_desbloqueo": orden,
            "usa_cronometro": False,
            "tiempo_default_segundos": None,
            "tipo_feedback": "detallado"
        })
        orden += 1
        
    # Desafíos Módulo 3
    configs.append({
        "seccion": m_id * 1000 + 11,
        "operacion": OperacionEnum.MIXTA,
        "cantidad_requerida": 20,
        "porcentaje_aprobacion": 90,
        "orden_desbloqueo": orden,
        "usa_cronometro": True,
        "tiempo_default_segundos": 25,
        "tipo_feedback": "simple"
    })
    orden += 1
    configs.append({
        "seccion": m_id * 1000 + 12,
        "operacion": OperacionEnum.MIXTA,
        "cantidad_requerida": 20,
        "porcentaje_aprobacion": 90,
        "orden_desbloqueo": orden,
        "usa_cronometro": True,
        "tiempo_default_segundos": 40,
        "tipo_feedback": "simple"
    })
    orden += 1
    configs.append({
        "seccion": m_id * 1000 + 13,
        "operacion": OperacionEnum.MIXTA,
        "cantidad_requerida": 10,
        "porcentaje_aprobacion": 90,
        "orden_desbloqueo": orden,
        "usa_cronometro": True,
        "tiempo_default_segundos": 50,
        "tipo_feedback": "simple"
    })
    orden += 1

    # Default de la fase
    configs.append({
        "seccion": 0,
        "operacion": OperacionEnum.MIXTA,
        "cantidad_requerida": 15,
        "porcentaje_aprobacion": 90,
        "orden_desbloqueo": 99,
        "usa_cronometro": True,
        "tiempo_default_segundos": 60,
        "tipo_feedback": "simple"
    })

    for c in configs:
        conf = ConfiguracionProgreso(
            fase_id=FASE5_ID,
            seccion=c["seccion"],
            operacion=c["operacion"],
            cantidad_requerida=c["cantidad_requerida"],
            porcentaje_aprobacion=c["porcentaje_aprobacion"],
            orden_desbloqueo=c["orden_desbloqueo"],
            usa_cronometro=c["usa_cronometro"],
            tiempo_default_segundos=c["tiempo_default_segundos"],
            tipo_feedback=c["tipo_feedback"]
        )
        session.add(conf)
        
    await session.commit()
    print("ConfiguracionProgreso Fase 4 insertados exitosamente.")

def _build_rect_half_quarters() -> Dict[str, Any]:
    return {
        "viewBox": "0 0 100 100",
        "sectors": [
            { "id": 1, "weight": 0.5, "points": "0,0 100,0 100,50 0,50", "label": "Mitad superior" },
            { "id": 2, "weight": 0.25, "points": "0,50 50,50 50,100 0,100", "label": "Cuarto inferior izquierdo" },
            { "id": 3, "weight": 0.25, "points": "50,50 100,50 100,100 50,100", "label": "Cuarto inferior derecho" }
        ]
    }

def _build_rect_rows_tenths() -> Dict[str, Any]:
    return {
        "viewBox": "0 0 100 100",
        "sectors": [
            { "id": 1, "weight": 0.2, "points": "0,0 100,0 100,20 0,20", "label": "Fila 1" },
            { "id": 2, "weight": 0.1, "points": "0,20 50,20 50,40 0,40", "label": "Fila 2 Izquierda" },
            { "id": 3, "weight": 0.1, "points": "50,20 100,20 100,40 50,40", "label": "Fila 2 Derecha" },
            { "id": 4, "weight": 0.2, "points": "0,40 100,40 100,60 0,60", "label": "Fila 3" },
            { "id": 5, "weight": 0.1, "points": "0,60 50,60 50,80 0,80", "label": "Fila 4 Izquierda" },
            { "id": 6, "weight": 0.1, "points": "50,60 100,60 100,80 50,80", "label": "Fila 4 Derecha" },
            { "id": 7, "weight": 0.2, "points": "0,80 100,80 100,100 0,100", "label": "Fila 5" }
        ]
    }

def _build_rect_columns_sixths() -> Dict[str, Any]:
    return {
        "viewBox": "0 0 90 90",
        "sectors": [
            { "id": 1, "weight": 0.16666, "points": "0,0 30,0 30,45 0,45", "label": "Columna 1 Superior" },
            { "id": 2, "weight": 0.16666, "points": "0,45 30,45 30,90 0,90", "label": "Columna 1 Inferior" },
            { "id": 3, "weight": 0.16666, "points": "30,0 60,0 60,45 30,45", "label": "Columna 2 Superior" },
            { "id": 4, "weight": 0.16666, "points": "30,45 60,45 60,90 30,90", "label": "Columna 2 Inferior" },
            { "id": 5, "weight": 0.33333, "points": "60,0 90,0 90,90 60,90", "label": "Columna 3" }
        ]
    }

def _build_rect_asymmetric_twelfths() -> Dict[str, Any]:
    return {
        "viewBox": "0 0 90 90",
        "sectors": [
            { "id": 1, "weight": 0.33333, "points": "0,0 30,0 30,90 0,90", "label": "Columna Izquierda Grande (4/12)" },
            { "id": 2, "weight": 0.16666, "points": "30,0 60,0 60,45 30,45", "label": "Columna Central Superior (2/12)" },
            { "id": 3, "weight": 0.16666, "points": "30,45 60,45 60,90 30,90", "label": "Columna Central Inferior (2/12)" },
            { "id": 4, "weight": 0.08333, "points": "60,0 90,0 90,45", "label": "Triángulo Superior-Derecho (1/12)" },
            { "id": 5, "weight": 0.08333, "points": "60,0 90,45 60,45", "label": "Triángulo Central-Derecho Superior (1/12)" },
            { "id": 6, "weight": 0.08333, "points": "60,45 90,45 60,90", "label": "Triángulo Central-Derecho Inferior (1/12)" },
            { "id": 7, "weight": 0.08333, "points": "90,45 90,90 60,90", "label": "Triángulo Inferior-Derecho (1/12)" }
        ]
    }

def _build_rect_columns_tenths() -> Dict[str, Any]:
    return {
        "viewBox": "0 0 100 100",
        "sectors": [
            { "id": 1, "weight": 0.2, "points": "0,0 20,0 20,100 0,100", "label": "Col 1" },
            { "id": 2, "weight": 0.1, "points": "20,0 30,0 30,100 20,100", "label": "Col 2" },
            { "id": 3, "weight": 0.1, "points": "30,0 40,0 40,100 30,100", "label": "Col 3" },
            { "id": 4, "weight": 0.2, "points": "40,0 60,0 60,100 40,100", "label": "Col 4" },
            { "id": 5, "weight": 0.1, "points": "60,0 70,0 70,100 60,100", "label": "Col 5" },
            { "id": 6, "weight": 0.3, "points": "70,0 100,0 100,100 70,100", "label": "Col 6" }
        ]
    }

def _build_rect_asymmetric_tenths() -> Dict[str, Any]:
    return {
        "viewBox": "0 0 100 100",
        "sectors": [
            { "id": 1, "weight": 0.4, "points": "0,0 40,0 40,100 0,100", "label": "Izquierda" },
            { "id": 2, "weight": 0.2, "points": "40,0 60,0 60,100 40,100", "label": "Centro" },
            { "id": 3, "weight": 0.1, "points": "60,0 100,0 100,25 60,25", "label": "Derecha 1" },
            { "id": 4, "weight": 0.1, "points": "60,25 100,25 100,50 60,50", "label": "Derecha 2" },
            { "id": 5, "weight": 0.1, "points": "60,50 100,50 100,75 60,75", "label": "Derecha 3" },
            { "id": 6, "weight": 0.1, "points": "60,75 100,75 100,100 60,100", "label": "Derecha 4" }
        ]
    }

def _build_triangle_medians_6() -> Dict[str, Any]:
    return {
        "viewBox": "0 0 100 100",
        "sectors": [
            { "id": 1, "weight": 0.16666, "points": "50,0 50,57.7 25,43.3", "label": "Sexto superior izquierdo" },
            { "id": 2, "weight": 0.16666, "points": "50,0 50,57.7 75,43.3", "label": "Sexto superior derecho" },
            { "id": 3, "weight": 0.16666, "points": "75,43.3 50,57.7 100,86.6", "label": "Sexto medio derecho" },
            { "id": 4, "weight": 0.16666, "points": "100,86.6 50,57.7 50,86.6", "label": "Sexto inferior derecho" },
            { "id": 5, "weight": 0.16666, "points": "50,86.6 50,57.7 0,86.6", "label": "Sexto inferior izquierdo" },
            { "id": 6, "weight": 0.16666, "points": "0,86.6 50,57.7 25,43.3", "label": "Sexto medio izquierdo" }
        ]
    }

def _build_triangle_midpoints_4() -> Dict[str, Any]:
    return {
        "viewBox": "0 0 100 100",
        "sectors": [
            { "id": 1, "weight": 0.25, "points": "50,0 75,50 25,50", "label": "Triángulo superior" },
            { "id": 2, "weight": 0.25, "points": "25,50 50,100 0,100", "label": "Triángulo inferior izquierdo" },
            { "id": 3, "weight": 0.25, "points": "75,50 100,100 50,100", "label": "Triángulo inferior derecho" },
            { "id": 4, "weight": 0.25, "points": "25,50 75,50 50,100", "label": "Triángulo central invertido" }
        ]
    }

def _build_triangle_asymmetric_complex() -> Dict[str, Any]:
    return {
        "viewBox": "0 0 100 100",
        "sectors": [
            { "id": 1, "weight": 0.125, "points": "50,0 50,50 25,50", "label": "Superior izquierdo" },
            { "id": 2, "weight": 0.125, "points": "50,0 50,50 75,50", "label": "Superior derecho" },
            { "id": 3, "weight": 0.125, "points": "50,50 50,100 25,50", "label": "Centro izquierdo" },
            { "id": 4, "weight": 0.125, "points": "50,50 50,100 75,50", "label": "Centro derecho" },
            { "id": 5, "weight": 0.125, "points": "25,50 0,100 25,100", "label": "Inferior izquierdo exterior" },
            { "id": 6, "weight": 0.125, "points": "25,50 25,100 50,100", "label": "Inferior izquierdo interior" },
            { "id": 7, "weight": 0.125, "points": "75,50 50,100 75,100", "label": "Inferior derecho interior" },
            { "id": 8, "weight": 0.125, "points": "75,50 75,100 100,100", "label": "Inferior derecho exterior" }
        ]
    }

def generate_practice_question_fase4(modulo_id: int, nivel_id: int, fam: int, var: int) -> Dict[str, Any]:
    base_seed = FASE5_ID * 100000 + modulo_id * 1000 + nivel_id * 100 + fam * 10
    seed = base_seed + var * 7919
    rng = random.Random(seed)
    es_espejo = var > 0
    prefix = ""  # Prefijo literal [ESPEJO] eliminado para limpieza visual
    
    nombre = rng.choice(NOMBRES)
    obj_frac = rng.choice(OBJETOS_FRACC)
    coleccion = rng.choice(COLECCIONES)
    bebida = rng.choice(BEBIDAS)
    
    # ── MÓDULO 1: La Fracción Visual ─────────────────────────────────────────
    if modulo_id == 1:
        if nivel_id == 1: # Polígonos Simétricos
            den = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
            num = rng.randint(1, den - 1)
            
            # Variación espejo (var 1 y 3 piden el complemento/fracción restante)
            pedir_complemento = es_espejo and (var % 2 == 1)
            if pedir_complemento:
                num_calc = den - num
                ans = f"{num_calc}/{den}"
            else:
                num_calc = num
                ans = f"{num}/{den}"
            
            # 50% interactivas en familias pares, estáticas en impares
            if fam % 2 == 0:
                if pedir_complemento:
                    enunciado = f"{prefix}{nombre} tiene una {obj_frac} dividida en {den} sectores idénticos. Necesita colorear las partes necesarias para que exactamente la fracción {ans} quede EN BLANCO (sin pintar). ¿Cuántas partes debe pintar?"
                    feedback = f"Para que {ans} quede en blanco, debes dejar exactamente {num_calc} sectores sin pintar de los {den} sectores totales, coloreando los otros {den - num_calc} sectores."
                else:
                    enunciado = f"{prefix}{nombre} necesita colorear la {obj_frac} (dividida en {den} sectores idénticos) para representar la fracción {ans}. Selecciona la cantidad de sectores correspondiente."
                    feedback = f"Haz clic sobre los trozos de la {obj_frac} hasta colorear exactamente {num} de los {den} sectores totales."
                vals = {
                    "tipo_visual": "pizza",
                    "cortes": den,
                    "sombreados": [],
                    "es_interactivo": True
                }
            else:
                if pedir_complemento:
                    enunciado = f"{prefix}Una {obj_frac} de {nombre} está dividida en {den} partes idénticas, y tiene {num} de ellas coloreadas. ¿Qué fracción representa la parte que NO está coloreada (en blanco)?"
                    feedback = f"Cuenta los sectores no sombreados para el de arriba ({num_calc}) y los sectores totales para el de abajo ({den}). El resultado es {ans}."
                else:
                    enunciado = f"{prefix}Identifica qué fracción representa la parte pintada de la {obj_frac} de {nombre}, la cual está dividida en {den} partes idénticas y tiene {num} de ellas coloreadas."
                    feedback = f"Cuenta los trozos sombreados para el numerador ({num}) y los trozos totales para el denominador ({den}). El resultado es {ans}."
                vals = {
                    "tipo_visual": "pizza",
                    "cortes": den,
                    "sombreados": list(range(num)),
                    "es_interactivo": False
                }
                
        elif nivel_id == 2: # Equivalencias
            den_base = rng.choice([2, 3, 4, 5, 6])
            num_base = rng.randint(1, den_base - 1)
            factor = rng.choice([2, 3, 4])
            
            # Variación espejo (var % 2 == 1 pide simplificar en vez de amplificar)
            pedir_simplificar = es_espejo and (var % 2 == 1)
            if pedir_simplificar:
                num_amplificado = num_base * factor
                den_amplificado = den_base * factor
                ans = f"{num_base}/{den_base}"
                enunciado = f"{prefix}{nombre} quiere simplificar la fracción {num_amplificado}/{den_amplificado} dividiendo tanto el numerador como el denominador entre {factor}. ¿Cuál es la nueva fracción equivalente reducida?"
                feedback = f"Divide el numerador ({num_amplificado} ÷ {factor} = {num_base}) y el denominador ({den_amplificado} ÷ {factor} = {den_base}). Obtenemos {ans}."
                vals = {
                    "tipo_visual": "pizza",
                    "cortes": den_amplificado,
                    "sombreados": list(range(num_amplificado)),
                    "es_interactivo": False,
                    "num_base": num_amplificado,
                    "den_base": den_amplificado,
                    "factor": factor
                }
            else:
                num = num_base * factor
                den = den_base * factor
                ans = f"{num}/{den}"
                enunciado = f"{prefix}{nombre} quiere amplificar la fracción {num_base}/{den_base} multiplicando tanto el numerador como el denominador por {factor}. ¿Cuál es la nueva fracción equivalente?"
                feedback = f"Multiplica el de arriba ({num_base} × {factor} = {num}) y el de abajo ({den_base} × {factor} = {den}). Obtenemos {ans}."
                vals = {
                    "tipo_visual": "pizza",
                    "cortes": den_base,
                    "sombreados": list(range(num_base)),
                    "es_interactivo": False,
                    "num_base": num_base,
                    "den_base": den_base,
                    "factor": factor
                }
                
        else: # Asimetría (non_homogeneous_polygon)
            if fam in (1, 2, 3, 4):
                tipo_pregunta = TipoPreguntaEnum.MULTIPLE_OPCION
                
                if fam == 1:
                    frac = "1/2"
                    pregunta_texto = f"{nombre} te muestra cuatro figuras. ¿Cuál de ellas **no** tiene coloreada exactamente la mitad ({frac})?"
                    
                    opt_a = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><polygon points='0,0 12,0 6,12' fill='#85f'/><path d='M6,0v12M0,0L6,12M12,0L6,12' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura está dividida en 4 triángulos iguales y 2 de ellos están coloreados. Esto representa exactamente 2/4, que equivale a la mitad (1/2)."
                    }
                    opt_b = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><polygon points='0,0 5,0 9,12 0,12' fill='#85f'/><path d='M5,0L9,12' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "¡Excelente! Esta figura está dividida por una línea inclinada que no pasa por los puntos simétricos, por lo que las dos partes no son iguales. La parte coloreada no representa la mitad (1/2)."
                    }
                    opt_c = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><polygon points='0,0 12,0 0,12' fill='#85f'/><path d='M0,12L12,0' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura está dividida por su diagonal en dos partes iguales. La mitad está coloreada, lo cual representa exactamente 1/2."
                    }
                    opt_d = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><path d='M0,0L6,6L0,12ZM12,0L6,6L12,12Z' fill='#85f'/><path d='M0,0l12,12M12,0L0,12' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura está dividida por sus diagonales en 4 triángulos iguales. 2 de ellos están coloreados, lo cual es exactamente 2/4, equivalente a 1/2."
                    }
                    
                    correct_opt = opt_b
                    all_opts = [opt_a, opt_b, opt_c, opt_d]
                    
                elif fam == 2:
                    frac = "1/4"
                    pregunta_texto = f"{nombre} te muestra cuatro figuras. ¿Cuál de ellas **no** tiene coloreada exactamente la cuarta parte ({frac})?"
                    
                    opt_a = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><rect y='6' width='4' height='6' fill='#f90'/><path d='M0,6h12M4,6v6M8,6v6' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "¡Excelente! Esta figura está dividida de forma desigual. La parte coloreada representa solo 1/6 del total, no 1/4."
                    }
                    opt_b = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><rect width='6' height='6' fill='#f90'/><path d='M0,6h12M6,0v6' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura está dividida en una mitad superior (que a su vez tiene dos cuartos) y una mitad inferior. El cuadro coloreado es exactamente 1/4 del total."
                    }
                    opt_c = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><polygon points='6,6 12,0 12,12' fill='#f90'/><path d='M0,0l12,12M12,0L0,12' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura está dividida por sus diagonales en 4 partes iguales, y 1 de ellas está coloreada. Esto representa exactamente 1/4."
                    }
                    opt_d = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><path d='M0,0h6L0,6ZM6,0h6v6Z' fill='#f90'/><path d='M6,0L12,6L6,12L0,6Z' fill='none' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura tiene un rombo inscrito que divide el cuadrado de modo que las 4 esquinas equivalen a la mitad del total. Al estar 2 esquinas coloreadas, representan 2/8, que es igual a 1/4."
                    }
                    
                    correct_opt = opt_a
                    all_opts = [opt_a, opt_b, opt_c, opt_d]
                    
                elif fam == 3:
                    frac = "1/8"
                    pregunta_texto = f"{nombre} te muestra cuatro figuras. ¿Cuál de ellas **no** tiene coloreada exactamente la octava parte ({frac})?"
                    
                    opt_a = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><rect width='3' height='6' fill='#38f'/><path d='M0,6h12M3,0v12M6,0v12M9,0v12' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura está dividida en una cuadrícula de 2x4 (8 rectángulos iguales), y 1 de ellos está coloreado. Esto representa exactamente 1/8."
                    }
                    opt_b = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><polygon points='6,0 9,0 9,9 6,6' fill='#38f'/><path d='M0,0l12,12M0,3h3v-3M0,6h6v-6M0,9h9v-9' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "¡Excelente! Las partes de esta figura tienen áreas diferentes debido al corte diagonal irregular. La franja coloreada no representa 1/8 del total."
                    }
                    opt_c = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><polygon points='0,0 0,6 6,6' fill='#38f'/><path d='M0,0l12,12M12,0L0,12M6,0v12M0,6h12' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura está dividida en 8 triángulos iguales. Al tener 1 coloreado, representa exactamente 1/8."
                    }
                    opt_d = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><polygon points='6,0 12,6 6,6' fill='#38f'/><path d='M6,0L12,6L6,12L0,6ZM6,0v12M0,6h12' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura combina un rombo y líneas divisorias de modo que todas las secciones externas e internas tienen la misma área (1/8). El triángulo coloreado representa exactamente 1/8."
                    }
                    
                    correct_opt = opt_b
                    all_opts = [opt_a, opt_b, opt_c, opt_d]
                    
                else:
                    frac = "1/3"
                    pregunta_texto = f"{nombre} te muestra cuatro figuras. ¿Cuál de ellas **no** tiene coloreada exactamente la tercera parte ({frac})?"
                    
                    opt_a = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><path d='M0,0h4v6H0ZM8,6h4v6H8Z' fill='#1c9'/><path d='M0,6h12M4,0v12M8,0v12' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura tiene 6 partes iguales. 2 de ellas están coloreadas. 2/6 es equivalente a 1/3."
                    }
                    opt_b = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><path d='M8,0h4v4h-4ZM4,4h4v4h-4ZM0,8h4v4H0Z' fill='#1c9'/><path d='M0,4h12M0,8h12M4,0v12M8,0v12' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura es una cuadrícula de 9 partes iguales. 3 de ellas están coloreadas. 3/9 es equivalente a 1/3."
                    }
                    opt_c = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><rect width='12' height='4' fill='#1c9'/><path d='M0,4h12M0,8h12' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "Esta figura tiene 3 filas iguales y 1 está coloreada. Esto representa exactamente 1/3."
                    }
                    opt_d = {
                        "texto": "<svg viewBox='0 0 12 12'><rect width='12' height='12' fill='#345' stroke='#fff' stroke-width='0.25'/><polygon points='0,12 12,12 6,7' fill='#1c9'/><path d='M6,0v7M0,12L6,7M12,12L6,7' stroke='#fff' stroke-width='0.25'/></svg>",
                        "feedback_error": "¡Excelente! Esta figura está dividida en tres partes que no tienen la misma área. El triángulo coloreado no representa la tercera parte (1/3)."
                    }
                    
                    correct_opt = opt_d
                    all_opts = [opt_a, opt_b, opt_c, opt_d]

                rotated_opts = []
                for i in range(4):
                    rotated_opts.append(all_opts[(i + var) % 4])
                
                ans = "La figura asimétrica"
                
                vals = {
                    "tipo_visual": None,
                    "es_interactivo": False
                }
                
                explicacion_html = (
                    f"Recuerda que para poder representar una fracción, las partes en las que se divide la unidad deben ser <span style='color:#A855F7'>exactamente iguales</span>.<br>"
                    f"<b>Respuesta correcta:</b> la figura con la asimetría o el área incorrecta."
                )
                
                return {
                    "enunciado": pregunta_texto,
                    "respuesta_correcta": ans,
                    "valores": vals,
                    "explicacion_profunda": explicacion_html,
                    "operacion": "mixta",
                    "tipo_pregunta": tipo_pregunta,
                    "alternativas": [
                        {
                            "texto": opt["texto"], 
                            "feedback_error": opt["feedback_error"],
                            "es_correcta": (opt == correct_opt)
                        }
                        for opt in rotated_opts
                    ]
                }

            # Seleccionar una de las geometrías base de forma aleatoria (original logic)
            geom_type = rng.choice([
                "rect_half_quarters", 
                "rect_rows_tenths", 
                "rect_columns_sixths",
                "rect_asymmetric_twelfths",
                "triangle_medians_6",
                "triangle_midpoints_4",
                "triangle_asymmetric_complex"
            ])
            
            if geom_type == "rect_half_quarters":
                geom_data = _build_rect_half_quarters()
                target_fraction = rng.choice(["1/2", "1/4", "3/4"])
            elif geom_type == "rect_rows_tenths":
                geom_data = _build_rect_rows_tenths()
                target_fraction = rng.choice(["1/2", "1/5", "3/10", "2/5", "3/5"])
            elif geom_type == "rect_columns_sixths":
                geom_data = _build_rect_columns_sixths()
                target_fraction = rng.choice(["1/2", "1/3", "2/3", "1/6", "5/6"])
            elif geom_type == "rect_asymmetric_twelfths":
                geom_data = _build_rect_asymmetric_twelfths()
                target_fraction = rng.choice(["1/12", "5/12", "7/12", "11/12", "1/4", "1/2", "3/4", "1/3", "2/3"])
            elif geom_type == "triangle_medians_6":
                geom_data = _build_triangle_medians_6()
                target_fraction = rng.choice(["1/2", "1/3", "2/3", "1/6", "5/6"])
            elif geom_type == "triangle_midpoints_4":
                geom_data = _build_triangle_midpoints_4()
                target_fraction = rng.choice(["1/2", "1/4", "3/4"])
            else: # triangle_asymmetric_complex
                geom_data = _build_triangle_asymmetric_complex()
                target_fraction = rng.choice(["1/2", "1/4", "3/4", "3/8", "5/8"])
            
            # Lógica de fracción espejo (no simplificada como reto adicional)
            target_fraction_display = target_fraction
            if es_espejo and (var % 2 == 1):
                espejo_map = {
                    "1/2": "2/4",
                    "1/3": "2/6",
                    "1/4": "2/8",
                    "2/3": "4/6",
                    "3/4": "6/8",
                    "1/5": "2/10",
                    "2/5": "4/10",
                    "3/5": "6/10"
                }
                target_fraction_display = espejo_map.get(target_fraction, target_fraction)
            
            # Calcular target_value decimal a partir de target_fraction
            frac_parts = target_fraction.split("/")
            target_value = float(frac_parts[0]) / float(frac_parts[1])
            
            is_triangle = "triangle" in geom_type
            objeto_nombre = "triángulo" if is_triangle else "figura"
            
            enunciado = f"{prefix}{nombre} necesita colorear la fracción **{target_fraction_display}** del {objeto_nombre} que tiene partes de diferentes tamaños. Haz clic en las partes necesarias hasta completar el área exacta requerida."
            feedback = f"Debes seleccionar piezas de manera que la suma de sus áreas sea exactamente igual a {target_fraction_display} del total."
            ans = target_fraction_display
            
            vals = {
                "tipo_visual": "non_homogeneous_polygon",
                "viewBox": geom_data["viewBox"],
                "sectors": geom_data["sectors"],
                "target_value": target_value,
                "target_fraction_text": target_fraction_display,
                "es_interactivo": True
            }
 
    # ── MÓDULO 2: Fracción de Cantidad ───────────────────────────────────────
    elif modulo_id == 2:
        genero_femenino = coleccion in ["cartas", "manzanas", "monedas de oro", "figuritas", "canicas brillantes", "pegatinas de dinosaurio", "conchas de mar", "estrellas de plástico"]
        de_los = "de las" if genero_femenino else "de los"
        cuantos = "¿Cuántas" if genero_femenino else "¿Cuántos"
        le_quedan = "le QUEDAN" if genero_femenino else "le QUEDAN"
 
        if nivel_id == 1: # Porción unitaria (1/n)
            den = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
            mult = rng.randint(2, min(12, 120 // den))  # Garantizar total <= 120
            total = den * mult
            
            # Variación espejo (var % 2 == 1 pide el restante)
            pedir_restante = es_espejo and (var % 2 == 1)
            if pedir_restante:
                ans = total - mult
                enunciado = f"{prefix}Si {nombre} tiene una colección de {total} {coleccion} y regala exactamente 1/{den} del total, ¿{cuantos.lower()} {coleccion} {le_quedan} a {nombre}?"
                feedback = f"Para saber lo que queda, primero calculamos 1/{den} de {total} ({total} ÷ {den} = {mult} regalados). Restamos del total: {total} - {mult} = {ans}."
                nivel_visual = den - 1
            else:
                ans = mult
                enunciado = f"{prefix}Calcula exactamente 1/{den} de la colección de {total} {coleccion} que tiene {nombre}."
                feedback = f"Para hallar 1/{den} de {total}, dividimos el total entre el denominador {den}: {total} ÷ {den} = {ans}."
                nivel_visual = 1
            
            vals = {
                "tipo_visual": "fraction_percentage",
                "total": total,
                "pct": 0,
                "cortes": den,
                "nivel": nivel_visual,
                "es_interactivo": True
            }
            
        elif nivel_id == 2: # Operador compuesto (m/n de X)
            den = rng.choice([3, 4, 5, 6, 8, 10, 12])
            num = rng.randint(2, den - 1)
            mult = rng.randint(2, min(10, 120 // den))  # Garantizar total <= 120
            total = den * mult
            
            # Variación espejo (var % 2 == 1 pide el complemento)
            pedir_complemento = es_espejo and (var % 2 == 1)
            if pedir_complemento:
                comp_num = den - num
                ans = comp_num * mult
                enunciado = f"{prefix}{nombre} tiene {total} {coleccion} y pierde exactamente {num}/{den} de ellos. ¿{cuantos} {coleccion} conserva (le quedan)?"
                feedback = f"Si pierde {num}/{den}, le quedan {comp_num}/{den}. Dividimos el total {total} ÷ {den} = {mult}. Multiplicamos por la parte que le queda: {mult} × {comp_num} = {ans}."
                nivel_visual = comp_num
            else:
                ans = num * mult
                enunciado = f"{prefix}Calcula {num}/{den} {de_los} {total} {coleccion} que encontró {nombre}."
                feedback = f"Primero divide {total} entre el denominador {den} ({total} ÷ {den} = {mult}). Luego multiplica por el numerador {num} ({mult} × {num} = {ans})."
                nivel_visual = num
            
            vals = {
                "tipo_visual": "fraction_percentage",
                "total": total,
                "pct": 0,
                "cortes": den,
                "nivel": nivel_visual,
                "es_interactivo": True
            }
            
        else: # Lógica del complemento
            den = rng.choice([4, 5, 6, 8, 10, 12])
            num = rng.randint(1, den - 2)
            comp_num = den - num
            mult = rng.randint(2, min(10, 120 // den))  # Garantizar total <= 120
            total = den * mult
            
            # Variación espejo (var % 2 == 1 pide la parte regalada en vez de la restante)
            pedir_regalado = es_espejo and (var % 2 == 1)
            if pedir_regalado:
                ans = num * mult
                enunciado = f"{prefix}{nombre} tenía {total} {coleccion} y regaló exactamente {num}/{den} del total. ¿{cuantos} {coleccion} regaló en total?"
                feedback = f"Calculamos {num}/{den} de {total}: dividimos {total} ÷ {den} = {mult}, y multiplicamos {mult} × {num} = {ans}."
                nivel_visual = num
            else:
                ans = comp_num * mult
                enunciado = f"{prefix}{nombre} tenía {total} {coleccion}. Regaló {num}/{den} del total a sus amigos. ¿{cuantos} {coleccion} le QUEDAN a {nombre} en total?"
                feedback = f"Si regaló {num}/{den}, le quedan {comp_num}/{den} del total. Calculamos {comp_num}/{den} de {total} = ({total} ÷ {den}) × {comp_num} = {ans}."
                nivel_visual = comp_num
                
            vals = {
                "tipo_visual": "fraction_percentage",
                "total": total,
                "pct": 0,
                "cortes": den,
                "nivel": nivel_visual,
                "es_interactivo": True
            }
 
    # ── MÓDULO 3: Porcentajes Rápidos y Promedios ────────────────────────────
    elif modulo_id == 3:
        if nivel_id == 1: # Porcentajes intuitivos (50, 25, 10, 75, 20)
            if fam % 2 == 0:
                # Seleccionar una de las geometrías base de forma aleatoria
                geom_type = rng.choice([
                    "rect_half_quarters", 
                    "rect_rows_tenths", 
                    "rect_columns_tenths",
                    "rect_asymmetric_tenths",
                    "triangle_medians_6",
                    "triangle_midpoints_4",
                    "triangle_asymmetric_complex"
                ])
                
                if geom_type == "rect_half_quarters":
                    geom_data = _build_rect_half_quarters()
                    pct = rng.choice([50, 75, 100])
                elif geom_type == "rect_rows_tenths":
                    geom_data = _build_rect_rows_tenths()
                    pct = rng.choice([10, 20, 40, 50, 80, 90, 100])
                elif geom_type == "rect_columns_tenths":
                    geom_data = _build_rect_columns_tenths()
                    pct = rng.choice([10, 20, 40, 50, 80, 90, 100])
                elif geom_type == "rect_asymmetric_tenths":
                    geom_data = _build_rect_asymmetric_tenths()
                    pct = rng.choice([10, 20, 40, 50, 80, 90, 100])
                elif geom_type == "triangle_medians_6":
                    geom_data = _build_triangle_medians_6()
                    pct = rng.choice([50])
                elif geom_type == "triangle_midpoints_4":
                    geom_data = _build_triangle_midpoints_4()
                    pct = rng.choice([50, 75, 100])
                else: # triangle_asymmetric_complex
                    geom_data = _build_triangle_asymmetric_complex()
                    pct = rng.choice([50, 75, 100])
                
                target_value = float(pct) / 100.0
                target_fraction_display = f"{pct}%"
                
                is_triangle = "triangle" in geom_type
                objeto_nombre = "triángulo" if is_triangle else "figura"
                
                enunciado = f"{prefix}{nombre} necesita colorear exactamente el **{target_fraction_display}** del {objeto_nombre} que tiene partes de diferentes tamaños. Haz clic en las partes necesarias hasta completar el área exacta requerida."
                feedback = f"Debes colorear sectores del {objeto_nombre} de manera que la suma de sus áreas represente el {target_fraction_display} del área total."
                ans = target_fraction_display
                
                vals = {
                    "tipo_visual": "non_homogeneous_polygon",
                    "viewBox": geom_data["viewBox"],
                    "sectors": geom_data["sectors"],
                    "target_value": target_value,
                    "target_fraction_text": target_fraction_display,
                    "es_interactivo": True
                }
            else:
                pct = rng.choice([10, 20, 25, 30, 40, 50, 60, 75, 80, 90])
                total = rng.choice([100, 200, 400, 500, 600, 1000])
                ans = (total * pct) // 100
                
                theme = rng.choice(["battery", "download", "tank"])
                pedir_quedan = es_espejo and (var % 2 == 1)
                
                if theme == "battery":
                    unit = "min"
                    if pedir_quedan:
                        pct_comp = 100 - pct
                        ans = total - ans
                        enunciado = f"{prefix}El dispositivo de {nombre} tiene una batería con una capacidad máxima de {total} minutos. Si ya consumió el {pct}% de la carga, ¿cuántos minutos de uso le QUEDAN (que representan el {pct_comp}%)?"
                        feedback = f"Si se gastó el {pct}% de la carga, le queda el {pct_comp}%. Calculamos: {pct_comp}% de {total} = {ans} minutos restantes."
                    else:
                        enunciado = f"{prefix}El dispositivo de {nombre} tiene una batería con una capacidad máxima de {total} minutos. Si actualmente la carga está al {pct}%, ¿cuántos minutos de uso le quedan?"
                        feedback = f"Calculamos el {pct}% de la capacidad total: {pct}% de {total} = {ans} minutos restantes."
                elif theme == "download":
                    unit = "MB"
                    if pedir_quedan:
                        pct_comp = 100 - pct
                        ans = total - ans
                        enunciado = f"{prefix}{nombre} está descargando un videojuego cuyo tamaño total es de {total} MB. Si la descarga ya va por el {pct}%, ¿cuántos MB quedan todavía por descargar (que representan el {pct_comp}%)?"
                        feedback = f"Si ya se descargó el {pct}%, falta el {pct_comp}%. Calculamos: {pct_comp}% de {total} = {ans} MB restantes."
                    else:
                        enunciado = f"{prefix}{nombre} está descargando un videojuego cuyo tamaño total es de {total} MB. Si la descarga ya va por el {pct}%, ¿cuántos MB se han descargado hasta ahora?"
                        feedback = f"Calculamos el {pct}% del tamaño total: {pct}% de {total} = {ans} MB descargados."
                else:  # tank
                    unit = "L"
                    if pedir_quedan:
                        pct_comp = 100 - pct
                        ans = total - ans
                        enunciado = f"{prefix}Un tanque de agua de {nombre} tiene una capacidad de {total} litros. Si se ha vaciado el {pct}% del tanque, ¿cuántos litros de agua QUEDAN adentro (que representan el {pct_comp}%)?"
                        feedback = f"Si se vació el {pct}%, queda el {pct_comp}%. Calculamos: {pct_comp}% de {total} = {ans} litros restantes."
                    else:
                        enunciado = f"{prefix}Un tanque de agua de {nombre} tiene una capacidad de {total} litros. Si el tanque está lleno al {pct}% de su capacidad, ¿cuántos litros de agua tiene adentro?"
                        feedback = f"Calculamos el {pct}% de la capacidad del tanque: {pct}% de {total} = {ans} litros de agua."
                        
                # Helper to find fraction representation
                num_v, den_v = pct, 100
                for d in [2, 4, 5, 10]:
                    v = (pct * d) / 100
                    if v.is_integer():
                        num_v, den_v = int(v), d
                        break
                
                pct_visual = 100 - pct if pedir_quedan else pct
                if pedir_quedan:
                    num_v = den_v - num_v
                    
                vals = {
                    "tipo_visual": "fraction_percentage",
                    "total": total,
                    "pct": pct_visual,
                    "cortes": den_v,
                    "nivel": num_v,
                    "es_interactivo": True
                }
            
        elif nivel_id == 2: # Gráficos circulares
            pct_a = rng.choice([20, 25, 30, 40, 50])
            pct_b = rng.choice([10, 15, 20, 30])
            while pct_a + pct_b >= 90:
                pct_b = rng.choice([10, 15, 20, 30])
            pct_c = 100 - pct_a - pct_b
            c1, c2, c3 = rng.sample(COLORES, 3)
            
            # Variación espejo (var % 2 == 1 pide la suma de dos sectores)
            pedir_suma_sectores = es_espejo and (var % 2 == 1)
            if pedir_suma_sectores:
                ans = pct_a + pct_b
                enunciado = f"{prefix}En un gráfico circular de los dulces favoritos de {nombre}, el {pct_a}% prefiere gomas {c1}, el {pct_b}% prefiere gomas {c2} y el {pct_c}% prefiere gomas {c3}. ¿Qué porcentaje de personas prefiere gomas {c1} O {c2} en total?"
                feedback = f"Sumamos los dos porcentajes para hallar la unión: {pct_a}% + {pct_b}% = {ans}%."
            else:
                ans = pct_c
                enunciado = f"{prefix}En un gráfico circular de los dulces favoritos de {nombre}, el {pct_a}% prefiere gomas {c1}, el {pct_b}% prefiere gomas {c2} y el resto prefiere gomas {c3}. ¿Qué porcentaje representa a las gomas {c3} sabiendo que todo el gráfico suma 100%?"
                feedback = f"La suma de los sectores de un gráfico circular es siempre 100%. Restamos: 100 - {pct_a} - {pct_b} = {ans}%."
                
            vals = {
                "tipo_visual": "pie",
                "es_interactivo": True,
                "pct_a": pct_a,
                "pct_b": pct_b,
                "pct_c": pct_c if not pedir_suma_sectores else ans,
                "categorias": [c1.capitalize(), c2.capitalize(), c3.capitalize()]
            }
            
        elif nivel_id == 3: # Gráficos de barras
            val_a = rng.randint(10, 50) * 10
            val_b = rng.randint(10, 50) * 10
            
            # Variación espejo (var % 2 == 1 pide el total acumulado en vez de diferencia)
            pedir_acumulado = es_espejo and (var % 2 == 1)
            if pedir_acumulado:
                ans = val_a + val_b
                enunciado = f"{prefix}En el torneo escolar, la barra A de {nombre} representa {val_a} puntos y la barra B representa {val_b} puntos. ¿Cuál es el total acumulado de puntos entre ambas barras?"
                feedback = f"Sumamos ambos valores de las barras: {val_a} + {val_b} = {ans} puntos."
            else:
                ans = abs(val_a - val_b)
                enunciado = f"{prefix}En el torneo escolar, la barra A de {nombre} representa {val_a} puntos y la barra B representa {val_b} puntos. ¿Cuál es la diferencia de puntos entre la barra A y la barra B?"
                feedback = f"Restamos ambos valores para hallar la diferencia: |{val_a} - {val_b}| = {ans}."
            vals = {
                "tipo_visual": "bar_chart",
                "val_a": val_a,
                "val_b": val_b,
                "categorias": ["Barra A", "Barra B"]
            }
            
        else: # Media Aritmética
            # Variación espejo (var % 2 == 1 pide el número faltante para alcanzar un promedio)
            pedir_faltante = es_espejo and (var % 2 == 1)
            if pedir_faltante:
                promedio_deseado = rng.randint(4, 10)
                a = rng.randint(2, 12)
                b = rng.randint(2, 12)
                suma_necesaria = promedio_deseado * 3
                c = suma_necesaria - a - b
                while c <= 0 or c > 15:
                    promedio_deseado = rng.randint(4, 10)
                    a = rng.randint(2, 12)
                    b = rng.randint(2, 12)
                    suma_necesaria = promedio_deseado * 3
                    c = suma_necesaria - a - b
                ans = c
                enunciado = f"{prefix}{nombre} quiere obtener una nota promedio de exactamente {promedio_deseado} en sus tres exámenes. Si en los dos primeros exámenes obtuvo notas de {a} y {b}, ¿qué nota debe sacar en el tercer examen?"
                feedback = f"Para que el promedio de 3 notas sea {promedio_deseado}, la suma de las notas debe ser {promedio_deseado} × 3 = {suma_necesaria}. Restamos lo que ya tiene: {suma_necesaria} - {a} - {b} = {ans}."
            else:
                a = rng.randint(2, 10)
                b = rng.randint(3, 12)
                c = rng.randint(1, 15)
                while (a + b + c) % 3 != 0:
                    c = rng.randint(1, 15)
                ans = (a + b + c) // 3
                enunciado = f"{prefix}Las alturas de tres torres de bloques que armó {nombre} son {a}, {b} y {c} bloques. ¿Cuál es la altura promedio al nivelar las tres torres?"
                feedback = f"Suma los tres valores para hacer la pila única ({a} + {b} + {c} = {a+b+c}) y divide el resultado entre 3 ({a+b+c} ÷ 3 = {ans})."
            vals = {
                "tipo_visual": "bar_chart",
                "val_a": a,
                "val_b": b,
                "categorias": ["Torre A", "Torre B"],
                "a": a, "b": b, "c": c
            }
 
    # ── MÓDULO 4: Razón y Mezclas ────────────────────────────────────────────
    else:
        p1, p2 = rng.sample(PINTURAS, 2)
        if nivel_id == 1: # Razones simples
            agua = rng.randint(2, 5)
            limon = 1
            factor = rng.randint(2, 5)
            
            # Variación espejo (var % 2 == 1 pide el ingrediente secundario en vez del primario)
            pedir_secundario = es_espejo and (var % 2 == 1)
            if pedir_secundario:
                ans = factor
                agua_total = agua * factor
                enunciado = f"{prefix}La receta de refresco de {nombre} usa una proporción de {agua} tazas de agua por 1 de jugo concentrado ({agua}:1). Si en una jarra pones {agua_total} tazas de agua, ¿cuántas tazas de jugo concentrado necesitas para conservar el sabor?"
                feedback = f"El agua aumentó {agua_total} ÷ {agua} = {factor} veces. Escalamos el jugo concentrado por el mismo factor: 1 × {factor} = {ans}."
            else:
                ans = agua * factor
                enunciado = f"{prefix}La receta de refresco de {nombre} usa una proporción de {agua} tazas de agua por 1 de jugo concentrado ({agua}:1). Si usas {factor} tazas de jugo concentrado en la jarra, ¿cuántas tazas de agua necesitas para conservar el sabor?"
                feedback = f"El jugo se multiplicó por {factor}. Escala el agua multiplicándola por {factor}: {agua} × {factor} = {ans}."
            vals = {"tipo_visual": "ratio_grid", "agua": agua, "limon": limon, "factor": factor}
            
        elif nivel_id == 2: # Reparto proporcional
            azul = rng.randint(1, 3)
            amarillo = rng.randint(2, 4)
            receta_total = azul + amarillo
            factor = rng.randint(3, 6) # Max 6 para evitar demasiados niveles
            pedido = receta_total * factor
            
            # Variación espejo (var % 2 == 1 pide el amarillo p2 en vez de azul p1)
            pedir_segundo_ing = es_espejo and (var % 2 == 1)
            if pedir_segundo_ing:
                ans = amarillo * factor
                if fam % 2 == 0:
                    enunciado = f"{prefix}{nombre} mezcla {azul}L de pintura {p1} con {amarillo}L de pintura {p2} (total {receta_total}L de mezcla). Representa en la probeta los litros de pintura {p2} requeridos para preparar {pedido}L de la misma mezcla verde."
                    feedback = f"Dividimos el pedido total ({pedido}) entre la receta base ({receta_total}) para hallar el lote: {pedido} ÷ {receta_total} = {factor}. Multiplicamos las partes de {p2} por {factor} ({amarillo} × {factor} = {ans}) e interactuamos con el medidor."
                    vals = {
                        "tipo_visual": "beaker",
                        "cortes": azul * factor + amarillo * factor,
                        "nivel": 0,
                        "es_interactivo": True,
                        "azul": azul,
                        "amarillo": amarillo,
                        "pedido": pedido
                    }
                else:
                    enunciado = f"{prefix}{nombre} mezcla {azul} litros de {p1} con {amarillo} litros de {p2} (haciendo {receta_total} litros en total). Para preparar {pedido} litros de la misma pintura, ¿cuántos litros de {p2} necesita?"
                    feedback = f"Divide el pedido total ({pedido}) entre la receta base ({receta_total}) para hallar el lote: {pedido} ÷ {receta_total} = {factor} veces. Multiplicamos la porción de {p2}: {amarillo} × {factor} = {ans}."
                    vals = {
                        "tipo_visual": "beaker",
                        "cortes": azul * factor + amarillo * factor,
                        "nivel": 0,
                        "es_interactivo": False,
                        "azul": azul,
                        "amarillo": amarillo,
                        "pedido": pedido
                    }
            else:
                ans = azul * factor
                if fam % 2 == 0:
                    enunciado = f"{prefix}{nombre} mezcla {azul}L de pintura {p1} con {amarillo}L de pintura {p2} (total {receta_total}L de mezcla). Representa en la probeta los litros de pintura {p1} requeridos para preparar {pedido}L de la misma mezcla."
                    feedback = f"Dividimos el pedido total ({pedido}) entre la receta base ({receta_total}) para hallar el lote: {pedido} ÷ {receta_total} = {factor}. Multiplicamos las partes de {p1} por {factor} ({azul} × {factor} = {ans}) e interactuamos con el medidor."
                    vals = {
                        "tipo_visual": "beaker",
                        "cortes": azul * factor + amarillo * factor,
                        "nivel": 0,
                        "es_interactivo": True,
                        "azul": azul,
                        "amarillo": amarillo,
                        "pedido": pedido
                    }
                else:
                    enunciado = f"{prefix}{nombre} mezcla {azul} litros de {p1} con {amarillo} litros de {p2} (haciendo {receta_total} litros en total). Para preparar {pedido} litros de la misma pintura, ¿cuántos litros de {p1} necesita?"
                    feedback = f"Divide el pedido total ({pedido}) entre la receta base ({receta_total}) para hallar el lote: {pedido} ÷ {receta_total} = {factor} veces. Multiplica el {p1}: {azul} × {factor} = {ans}."
                    vals = {
                        "tipo_visual": "beaker",
                        "cortes": azul * factor + amarillo * factor,
                        "nivel": 0,
                        "es_interactivo": False,
                        "azul": azul,
                        "amarillo": amarillo,
                        "pedido": pedido
                    }
            
        else: # Mezclas complejas
            ess = 1
            alc = rng.choice([3, 4, 9])
            total = ess + alc
            
            # Variación espejo (var % 2 == 1 pide el porcentaje de alcohol en vez de esencia)
            pedir_pct_alc = es_espejo and (var % 2 == 1)
            if pedir_pct_alc:
                ans = (alc * 100) // total
                if fam % 2 == 0:
                    enunciado = f"{prefix}El perfume de {nombre} mezcla {ess} parte de esencia con {alc} partes de alcohol (total {total} partes). Representa las partes de alcohol interactuando con la probeta y escribe qué porcentaje representa del volumen total."
                    feedback = f"El alcohol representa {alc} de un total de {total} partes ({alc}/{total}). Registra {alc} niveles en la probeta, e introduce el porcentaje: ({alc} ÷ {total}) × 100 = {ans}%."
                    vals = {
                        "tipo_visual": "beaker",
                        "cortes": total,
                        "nivel": 0,
                        "es_interactivo": True,
                        "ess": ess,
                        "alc": alc,
                        "total": total
                    }
                else:
                    enunciado = f"{prefix}{nombre} creó un perfume mezclando {ess} parte de esencia por {alc} partes de alcohol (haciendo {total} partes en total). ¿Qué porcentaje del volumen representa el alcohol en este perfume?"
                    feedback = f"La fracción de alcohol es {alc} de {total} partes totales ({alc}/{total}). Multiplicamos por 100 para hallar el porcentaje: ({alc} ÷ {total}) × 100 = {ans}%."
                    vals = {
                        "tipo_visual": "beaker",
                        "cortes": total,
                        "nivel": 0,
                        "es_interactivo": False,
                        "ess": ess,
                        "alc": alc,
                        "total": total
                    }
            else:
                ans = (ess * 100) // total
                if fam % 2 == 0:
                    enunciado = f"{prefix}El perfume de {nombre} mezcla {ess} parte de esencia con {alc} partes de alcohol (total {total} partes). Representa las partes de esencia interactuando con la probeta y escribe qué porcentaje representa del volumen total."
                    feedback = f"La esencia representa 1 de un total de {total} partes (1/{total}). Haz clic en el primer nivel de la probeta para representarlo, e introduce el porcentaje correspondiente: 100 ÷ {total} = {ans}%."
                    vals = {
                        "tipo_visual": "beaker",
                        "cortes": total,
                        "nivel": 0,
                        "es_interactivo": True,
                        "ess": ess,
                        "alc": alc,
                        "total": total
                    }
                else:
                    enunciado = f"{prefix}{nombre} creó un perfume mezclando {ess} parte de esencia por {alc} partes de alcohol (haciendo {total} partes en total). ¿Qué porcentaje representa la esencia en este perfume?"
                    feedback = f"La fracción de esencia es 1 de {total} partes totales (1/{total}). Multiplicamos por 100 para hallar el porcentaje: 100 ÷ {total} = {ans}%."
                    vals = {
                        "tipo_visual": "beaker",
                        "cortes": total,
                        "nivel": 0,
                        "es_interactivo": False,
                        "ess": ess,
                        "alc": alc,
                        "total": total
                    }

    explicacion_html = (
        f"Recuerda seguir el orden pedagógico del Tutor Invisible:<br>"
        f"<b>Demostración:</b> {feedback}<br>"
        f"<b>Resultado esperado:</b> <span style='color:#A855F7'>{ans}</span>"
    )

    return {
        "enunciado": enunciado,
        "respuesta_correcta": str(ans),
        "valores": vals,
        "explicacion_profunda": explicacion_html,
        "operacion": "mixta"
    }

async def seed_preguntas_practica(session: AsyncSession):
    print("Generando pool de Práctica Libre de Fase 4 (15 familias por nivel)...")
    
    # 4 módulos
    modulos_niveles = {1: 3, 2: 3, 3: 4, 4: 3}
    for modulo_id, max_niv in modulos_niveles.items():
        for nivel_id in range(1, max_niv + 1):
            seccion = modulo_id * 100 + nivel_id
            
            # Generar 15 familias de preguntas por nivel
            for fam in range(1, 16):
                padre_id = f"f4_m{modulo_id}_l{nivel_id}_fam_{fam:03d}"
                
                for var in range(4):
                    q_data = generate_practice_question_fase4(modulo_id, nivel_id, fam, var)
                    datos_numericos = {
                        "es_espejo": var > 0,
                        "variante": var,
                        **q_data.get("valores", {})
                    }
                    
                    tipo_pregunta = q_data.get("tipo_pregunta", TipoPreguntaEnum.RESPUESTA_NUMERICA)
                    pregunta = Pregunta(
                        fase_id=FASE5_ID,
                        seccion=seccion,
                        operacion=OperacionEnum.MIXTA,
                        tipo_pregunta=tipo_pregunta,
                        enunciado=q_data["enunciado"],
                        respuesta_correcta=q_data["respuesta_correcta"],
                        estructura_padre_id=padre_id,
                        datos_numericos=datos_numericos,
                        explicacion_paso_a_paso={
                            "html": q_data["explicacion_profunda"]
                        },
                        estado=StatusEnum.ACTIVO
                    )
                    session.add(pregunta)
                    await session.flush()
                    
                    if tipo_pregunta == TipoPreguntaEnum.MULTIPLE_OPCION and "alternativas" in q_data:
                        for o_idx, opt in enumerate(q_data["alternativas"]):
                            es_correcta = opt.get("es_correcta", (opt["texto"] == q_data["respuesta_correcta"]))
                            alt = Alternativa(
                                pregunta_id=pregunta.id,
                                texto=opt["texto"],
                                es_correcta=es_correcta,
                                orden=o_idx + 1,
                                tipo_error=TipoErrorEnum.CALCULO if not es_correcta else None,
                                feedback_error=opt.get("feedback_error") if not es_correcta else None
                            )
                            session.add(alt)
            print(f"  Módulo {modulo_id} Nivel {nivel_id} (15 familias × 4 variantes) insertados.")
            await session.flush()
            
    await session.commit()
    print("Pool de Práctica Libre de Fase 4 insertado.")

def _add_distractor(errores_previstos: Dict[str, str], ans: str, value: int, msg: str):
    """
    Agrega un distractor a errores_previstos evitando que coincida numéricamente
    con la respuesta correcta (puede pasar por coincidencia según los valores
    aleatorios elegidos para la pregunta).
    """
    v = value
    if str(v) == str(ans):
        v = value + 1 if value > 0 else value + 2
    errores_previstos[str(v)] = msg


def generate_challenge_question_fase4(modulo_id: int, desafio_id: int, idx: int) -> Dict[str, Any]:
    seed = FASE5_ID * 1000000 + modulo_id * 10000 + desafio_id * 1000 + idx
    rng = random.Random(seed)
    
    # Múltiple opción para Desafíos 11 y 12. Evocación pura para 13.
    tipo = TipoPreguntaEnum.MULTIPLE_OPCION if desafio_id in (11, 12) else TipoPreguntaEnum.RESPUESTA_NUMERICA
    
    vals = {}
    errores_previstos = {}
    
    nombre = rng.choice(NOMBRES)
    coleccion = rng.choice(COLECCIONES)
    bebida = rng.choice(BEBIDAS)
    
    if modulo_id == 1:
        den = rng.choice([4, 5, 8, 10])
        num = rng.randint(1, den - 1)
        ans = f"{num}/{den}"
        c1, c2 = rng.sample(COLORES, 2)
        enunciado = f"Un azulejo cuadrado está dividido en {den} tiras del mismo tamaño y {num} de ellas son de color {c1}. ¿Qué fracción representa el color {c1}?"
        vals = {"tipo_visual": "pizza", "cortes": den, "sombreados": list(range(num)), "es_interactivo": False}
        errores_previstos[f"{den}/{num}"] = "Invertiste el orden de los términos. El total de divisiones siempre va abajo (denominador)."
        errores_previstos[f"{num}"] = "Escribiste solo el número de partes pintadas, pero recuerda que una fracción se compone de numerador y denominador en formato N/D."
        errores_previstos[f"{num}/{den-num}"] = "Escribiste la relación entre pintadas y no pintadas. El denominador de abajo debe ser el total de partes en que se divide la figura."
        
    elif modulo_id == 2:
        den = rng.choice([3, 4, 5, 8])
        num = rng.randint(1, den - 1)
        mult = rng.randint(2, 6)
        total = den * mult
        ans = str(num * mult)
        enunciado = f"En una caja de herramientas con {total} tornillos, {nombre} usó exactamente {num}/{den} del total. ¿Cuántos tornillos utilizó?"
        vals = {"total": total, "num": num, "den": den}
        errores_previstos[str(total * num)] = "Multiplicaste por el numerador directamente sin dividir. Primero debes dividir el total entre el denominador."
        if num > 1:
            errores_previstos[str(total // den)] = "Calculaste solo 1 parte (fracción unitaria). Te falta multiplicar por el numerador."
        else:
            errores_previstos[str(total - 1)] = "Restaste 1 en vez de calcular la fracción del total."
        if num * 2 != den:
            errores_previstos[str(total - int(ans))] = "Calculaste la cantidad que le queda en el vaso (el complemento). Presta atención a si la pregunta pide lo que se usó o lo que queda."
        else:
            errores_previstos[str(total // 2 - 1)] = "Calculaste incorrectamente la mitad de los elementos."
        
    elif modulo_id == 3:
        categoria = idx % 4
        if categoria == 0:  # Porcentajes intuitivos
            pct = rng.choice([10, 20, 25, 30, 40, 50, 60, 75, 80, 90])
            total = rng.choice([100, 200, 400, 500, 600, 1000])
            ans = str((total * pct) // 100)
            
            theme = rng.choice(["battery", "download", "tank"])
            
            if theme == "battery":
                unit = "min"
                enunciado = f"El dispositivo de {nombre} tiene una batería con una capacidad máxima de {total} minutos. Si la carga está al {pct}%, ¿cuántos minutos de uso le quedan?"
            elif theme == "download":
                unit = "MB"
                enunciado = f"{nombre} está descargando un archivo de {total} MB en total. Si la descarga ya va por el {pct}%, ¿cuántos MB se han descargado hasta ahora?"
            else:  # tank
                unit = "L"
                enunciado = f"Un tanque de agua de {nombre} tiene una capacidad de {total} litros. Si el tanque está lleno al {pct}% de su capacidad, ¿cuántos litros de agua tiene adentro?"
                
            vals = {
                "tipo_visual": "contextual_bar",
                "total": total,
                "pct": pct,
                "theme": theme,
                "unit": unit
            }
            
            ans_val = int(ans)
            comp_val = total - ans_val
            if pct != 50:
                errores_previstos[str(comp_val)] = "Calculaste el complemento (lo que falta o se gastó). Relee la pregunta con atención."
                errores_previstos[str(total)] = "Ese es el valor total original, no la porción del porcentaje solicitado."
                errores_previstos[str(ans_val // 2)] = "Calculaste la mitad de la porción correcta."
            else:
                errores_previstos[str(ans_val // 2)] = "Calculaste el 25% (la cuarta parte) en lugar del 50% (la mitad)."
                errores_previstos[str(total)] = "Ese es el valor total original, no la porción del porcentaje solicitado."
            
        elif categoria == 1:  # Gráficos circulares
            pct_a = rng.choice([20, 25, 30, 40, 50])
            pct_b = rng.choice([10, 15, 20, 30])
            while pct_a + pct_b >= 90:
                pct_b = rng.choice([10, 15, 20, 30])
            pct_c = 100 - pct_a - pct_b
            ans = str(pct_c)
            c1, c2, c3 = rng.sample(COLORES, 3)
            enunciado = f"En un gráfico circular sobre las mascotas de la escuela de {nombre}, el {pct_a}% son perros ({c1}), el {pct_b}% son gatos ({c2}) y el resto son pájaros ({c3}). ¿Qué porcentaje de pájaros ({c3}) hay en total?"
            vals = {
                "tipo_visual": "pie",
                "es_interactivo": False,
                "pct_a": pct_a,
                "pct_b": pct_b,
                "pct_c": pct_c,
                "categorias": [c1.capitalize(), c2.capitalize(), c3.capitalize()]
            }
            if pct_a + pct_b != pct_c:
                errores_previstos[str(pct_a + pct_b)] = "Sumaste los porcentajes de perros y gatos, pero queremos el porcentaje restante de pájaros."
            else:
                errores_previstos[str(pct_a)] = "Ese es el porcentaje del sector de perros, no del de pájaros."
            errores_previstos[str(100 - pct_a)] = "Olvidaste restar el porcentaje de gatos del total."
            
        elif categoria == 2:  # Gráficos de barras
            val_a = rng.randint(1, 10) * 10
            val_b = rng.randint(1, 10) * 10
            ans = str(abs(val_a - val_b))
            enunciado = f"En la biblioteca de {nombre}, el gráfico de barras muestra que el estante A tiene {val_a} libros y el estante B tiene {val_b} libros. ¿Cuál es la diferencia de libros entre el estante A y el estante B?"
            vals = {
                "tipo_visual": "bar_chart",
                "val_a": val_a,
                "val_b": val_b,
                "categorias": ["Estante A", "Estante B"]
            }
            errores_previstos[str(val_a + val_b)] = "Sumaste la cantidad de libros de ambos estantes. La pregunta pide la diferencia."
            if abs(val_a - val_b) != val_a:
                errores_previstos[str(val_a)] = "Ese es solo el valor del estante A."
            else:
                errores_previstos[str(val_a * 2)] = "Multiplicaste la cantidad de un estante por 2."
            

            
        else:  # Media Aritmética
            a = rng.randint(2, 10)
            b = rng.randint(3, 12)
            c = rng.randint(1, 15)
            while (a + b + c) % 3 != 0:
                c = rng.randint(1, 15)
            ans = str((a + b + c) // 3)
            enunciado = f"En sus tres alcancías, {nombre} tiene R$ {a}, R$ {b} y R$ {c}. ¿Cuál es la cantidad promedio de dinero por alcancía si reparte el dinero equitativamente?"
            vals = {"a": a, "b": b, "c": c}
            errores_previstos[str(a + b + c)] = "Solo sumaste la cantidad total de dinero, pero debes dividirlo entre las 3 alcancías."
            if (a + b + c) // 3 != a + b:
                errores_previstos[str(a + b)] = "Sumaste solo los dos primeros valores de dinero."
            else:
                errores_previstos[str(a + b + c + 3)] = "Calculaste incorrectamente la suma total."
            
    else: # Módulo 4
        categoria = idx % 3
        if categoria == 0:
            # Razones simples
            solvente = rng.randint(2, 6)
            factor = rng.choice([2, 3, 4, 5])
            ans = str(solvente * factor)
            
            theme = rng.choice(["perfume", "jugo", "limonada"])
            if theme == "perfume":
                enunciado = f"Un perfume requiere {solvente} partes de solvente por 1 parte de fragancia. Si {nombre} elabora un frasco usando {factor} partes de fragancia, ¿cuánto solvente lleva para mantener la razón?"
            elif theme == "jugo":
                enunciado = f"Una receta de jugo usa {solvente} tazas de agua por 1 de concentrado. Si {nombre} usa {factor} tazas de concentrado, ¿cuántas tazas de agua necesita?"
            else:
                enunciado = f"Para la limonada, se usan {solvente} limones por 1 litro de agua. Si {nombre} prepara la bebida con {factor} litros de agua, ¿cuántos limones exprimirá?"
                
            vals = {}
            if not (solvente == 2 and factor == 2):
                _add_distractor(errores_previstos, ans, solvente + factor, "Sumaste los ingredientes. Las proporciones se mantienen multiplicando, no sumando.")
            _add_distractor(errores_previstos, ans, factor, "Escribiste solo el factor de multiplicación.")
            _add_distractor(errores_previstos, ans, solvente, "Esa es la cantidad de la receta básica para 1 parte.")
            
        elif categoria == 1:
            # Reparto de volúmenes
            ing1 = rng.randint(1, 3)
            ing2 = rng.randint(2, 5)
            receta = ing1 + ing2
            factor = rng.randint(3, 8)
            pedido = receta * factor
            ans = str(ing1 * factor)
            
            theme = rng.choice(["pintura", "concreto"])
            if theme == "pintura":
                enunciado = f"{nombre} mezcla {ing1}L de azul y {ing2}L de amarillo (haciendo {receta}L en total). Para preparar {pedido}L de la misma pintura, ¿cuántos litros de azul necesita?"
            else:
                enunciado = f"Para el concreto, {nombre} mezcla {ing1} de cemento y {ing2} de arena ({receta} en total). Para hacer {pedido} unidades de mezcla, ¿cuánto cemento usa?"
                
            vals = {}
            _add_distractor(errores_previstos, ans, pedido // receta, "Calculaste cuántas veces se multiplica la receta (el factor), no la cantidad del ingrediente.")
            _add_distractor(errores_previstos, ans, ing2 * factor, "Calculaste la cantidad del otro ingrediente.")
            _add_distractor(errores_previstos, ans, pedido - ing1, "Restaste en lugar de usar proporciones.")
            
        else:
            # Porcentajes en mezclas
            ess = 1
            alc = rng.choice([3, 4, 9, 19, 24])
            total = ess + alc
            
            ans = str((ess * 100) // total)
            
            enunciado = f"{nombre} creó una mezcla con {ess} parte de ingrediente activo y {alc} partes de base (haciendo {total} partes en total). ¿Qué porcentaje representa el ingrediente activo en esta mezcla?"
            
            vals = {}
            _add_distractor(errores_previstos, ans, (alc * 100) // total, "Calculaste el porcentaje de la base, no del ingrediente activo.")
            _add_distractor(errores_previstos, ans, 100 // alc, "Dividiste entre la base en lugar del total de partes.")
        
    # Ningún distractor previsto debe coincidir con la respuesta correcta
    # (puede ocurrir por coincidencia numérica según los valores aleatorios elegidos).
    errores_previstos = {k: v for k, v in errores_previstos.items() if k != str(ans)}

    return {
        "enunciado": enunciado,
        "respuesta_correcta": str(ans),
        "valores": vals,
        "errores_previstos": errores_previstos,
        "tipo_pregunta": tipo,
        "operacion": "mixta"
    }

async def seed_preguntas_desafios(session: AsyncSession):
    print("Generando pool de Desafíos de Fase 4 (30 preguntas por desafío)...")
    
    # 4 módulos, cada uno con 3 desafíos (11, 12, 13)
    for modulo_id in range(1, 5):
        for desafio_id in (11, 12, 13):
            seccion = modulo_id * 1000 + desafio_id
            
            for idx in range(1, 31):
                q_data = generate_challenge_question_fase4(modulo_id, desafio_id, idx)
                
                datos_numericos = {
                    "es_desafio": True,
                    "indice": idx,
                    **q_data.get("valores", {})
                }
                
                pregunta = Pregunta(
                    fase_id=FASE5_ID,
                    seccion=seccion,
                    operacion=OperacionEnum.MIXTA,
                    tipo_pregunta=q_data["tipo_pregunta"],
                    enunciado=q_data["enunciado"],
                    respuesta_correcta=q_data["respuesta_correcta"],
                    estructura_padre_id=f"f4_m{modulo_id}_d{desafio_id}_q_{idx:03d}",
                    datos_numericos=datos_numericos,
                    errores_previstos=q_data.get("errores_previstos", {}),
                    explicacion_paso_a_paso={
                        "html": f"<b>Resolución de Desafío:</b> La respuesta correcta es {q_data['respuesta_correcta']}."
                    },
                    estado=StatusEnum.ACTIVO
                )
                session.add(pregunta)
                await session.flush()
                
                # Seeding alternativas for multiple choice challenges
                if q_data["tipo_pregunta"] == TipoPreguntaEnum.MULTIPLE_OPCION:
                    correct_val = q_data["respuesta_correcta"]
                    # Los distractores sembrados en errores_previstos pueden coincidir
                    # accidentalmente con la respuesta correcta (ver seed corregido en
                    # generate_challenge_question_fase4); se filtran antes de usarlos
                    # para no generar 2 alternativas marcadas como correctas.
                    incorrect_choices = [
                        v for v in q_data.get("errores_previstos", {}).keys()
                        if v != correct_val
                    ]

                    rng = random.Random(FASE5_ID * 100000 + seccion * 100 + idx)
                    
                    while len(incorrect_choices) < 3:
                        if "/" in correct_val:
                            n_str, d_str = correct_val.split("/")
                            n, d = int(n_str), int(d_str)
                            dist_n = max(1, n + rng.choice([-1, 1, 2]))
                            dist_d = max(2, d + rng.choice([-1, 1, 2]))
                            val = f"{dist_n}/{dist_d}"
                        else:
                            c_val = int(correct_val)
                            dist = c_val + rng.choice([-2, -1, 1, 2, 5, 10])
                            val = str(max(0, dist))
                        
                        if val != correct_val and val not in incorrect_choices:
                            incorrect_choices.append(val)
                            
                    choices = list(incorrect_choices[:3]) + [correct_val]
                    rng.shuffle(choices)
                    
                    for o_idx, opt in enumerate(choices):
                        error_msg = q_data.get("errores_previstos", {}).get(opt, "Esa alternativa es incorrecta. Vuelve a calcular.")
                        
                        alt = Alternativa(
                            pregunta_id=pregunta.id,
                            texto=opt,
                            es_correcta=(opt == correct_val),
                            orden=o_idx + 1,
                            tipo_error=TipoErrorEnum.CALCULO if opt != correct_val else None,
                            feedback_error=error_msg if opt != correct_val else None
                        )
                        session.add(alt)
            print(f"  Módulo {modulo_id} Desafío {desafio_id} (30 preguntas) insertadas.")
            await session.flush()
            
    await session.commit()
    print("Pool de Desafíos de Fase 4 insertado.")

async def run_fase4_seed():
    print("Iniciando inyección de Fase 4 en base de datos...")
    async with AsyncSessionLocal() as session:
        # Clear existing Fase 4 entries to prevent duplicates
        await clear_fase4_data(session)
        
        # 1. Seed Theory content
        await seed_teoria_niveles(session)
        
        # 2. Seed configs
        await seed_configuracion_progreso(session)
        
        # 3. Seed practice questions
        await seed_preguntas_practica(session)
        
        # 4. Seed challenges
        await seed_preguntas_desafios(session)
        
    print("Fase 4 seeded successfully!")

if __name__ == "__main__":
    asyncio.run(run_fase4_seed())

