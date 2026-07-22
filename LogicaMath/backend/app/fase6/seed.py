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
from app.fase6.theory_examples import obtener_ejemplos_expandidos_fase6

from app.utils.graphics_generator import generate_isometric_cubes_image, generate_thermometer_image
from app.core.storage import storage_service

FASE6_ID = 6

# --- DICCIONARIOS DE CONTEXTO FASE 6 ---
NOMBRES = ["Lucas", "Sofía", "Mateo", "Valeria", "Diego", "Camila",
           "Emilia", "Bruno", "Renata", "Tomás", "Isabela", "Joaquín", "Antonella", "Facundo"]
CONTENEDORES = ["caja de juguetes", "caja de cartón", "cofre del tesoro", "baúl",
                "acuario vacío", "caja de mudanza", "estuche de herramientas", "nevera portátil"]
LIQUIDOS = ["piscina inflable", "tanque de reserva", "recipiente de cristal",
            "bidón de agua", "pecera gigante", "cisterna del jardín", "termo industrial"]
MASAS = ["bolsa de manzanas", "saco de papas", "paquete de arroz", "caja de herramientas",
         "costal de harina", "mochila cargada", "bulto de naranjas", "caja de libros"]
TEMPERATURAS = ["laboratorio", "clima de la ciudad", "experimento de química", "refrigerador",
                "invernadero", "horno de la cocina", "cámara frigorífica", "termómetro del jardín"]

# Objetos reales de la vida cotidiana que tienen la forma de cada poliedro (M1L1).
# Conectan el cuerpo geométrico abstracto de la figura con algo que el niño conoce,
# generando variedad REAL de situaciones (no solo cambio de nombre).
_POLIEDRO_OBJETOS = {
    "cubo": ["un dado", "un cubo de hielo", "una caja de regalo cúbica", "un cubo de Rubik",
             "un dado de espuma gigante", "un cubo mágico", "una caja de dados"],
    "prisma rectangular": ["una caja de zapatos", "un ladrillo", "una caja de cereal", "un libro grueso",
                           "un acuario", "una barra de jabón", "un contenedor de plástico", "un borrador de pizarra"],
    "pirámide cuadrangular": ["una pirámide de Egipto", "el techo de una torre", "una carpa piramidal",
                              "un pisapapeles de cristal", "una campana de circo"],
    "prisma triangular": ["una tienda de campaña", "un prisma de vidrio que forma un arcoíris",
                          "una barra de chocolate triangular", "una rampa de skate", "un atril de madera"],
}

# Escenarios/objetos para el conteo de cubos unitarios (M3L1). El detalle del
# material o del tipo de construcción cambia la SITUACIÓN presentada al alumno.
CONSTRUCCIONES_CUBOS = ["torre", "muro", "pila", "castillo de bloques", "escultura", "pirámide escalonada", "plataforma"]
MATERIALES_CUBOS = ["de madera", "de plástico", "de colores", "magnéticos", "de goma espuma", "de cristal"]

# Cache en memoria para reutilizar URLs de gráficos generados
_graphic_url_cache: Dict[str, str] = {}

async def clear_fase6_data(session: AsyncSession):
    print("Purging existing Fase 6 data for a clean overwrite...")
    result = await session.execute(select(Pregunta.id).where(Pregunta.fase_id == FASE6_ID))
    pregunta_ids_list = result.scalars().all()
    
    if pregunta_ids_list:
        await session.execute(delete(Alternativa).where(Alternativa.pregunta_id.in_(pregunta_ids_list)))
        res_int_q = await session.execute(select(IntentoPregunta.id).where(IntentoPregunta.pregunta_id.in_(pregunta_ids_list)))
        int_q_ids = res_int_q.scalars().all()
        if int_q_ids:
            await session.execute(delete(IntentoPaso).where(IntentoPaso.intento_pregunta_id.in_(int_q_ids)))
            await session.execute(delete(IntentoPregunta).where(IntentoPregunta.id.in_(int_q_ids)))
            
        await session.execute(delete(Intento).where(Intento.pregunta_id.in_(pregunta_ids_list)))
        await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.pregunta_id.in_(pregunta_ids_list)))
        
    await session.execute(delete(Intento).where(Intento.fase_id == FASE6_ID))
    await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE6_ID))
    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE6_ID))
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE6_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE6_ID))
    await session.commit()
    print("Fase 6 data purged.")

async def seed_teoria_niveles(session: AsyncSession):
    print("Sembrando guión de textos (NivelTeoria) para Fase 6...")
    
    niveles_teoria = [
        # --- MÓDULO 1: Reconocimiento 3D ---
        {
            "modulo_id": 1, "nivel_id": 1,
            "titulo": "Identificación de poliedros",
            "texto_descubrimiento": "¡Hola, campeona del espacio 3D! 🌌 Hasta ahora hemos jugado en papel plano (2D), pero hoy daremos el gran salto a las tres dimensiones. Los poliedros son cuerpos sólidos que tienen volumen (ocupan un lugar real en tu habitación).\nTienen tres partes clave:\n1. Caras: las paredes planas.\n2. Vértices: las esquinitas puntiagudas.\n3. Aristas: las líneas rectas donde se juntan las caras. ¡Como los bordes de una caja de regalo!",
            "diccionario": {"Vértice": "Esquina donde se unen tres o más aristas.", "Cara": "Superficie plana del poliedro.", "Arista": "Línea de unión donde se juntan dos caras contiguas."},
            "advertencia": "No vayas a confundir aristas con caras. Por ejemplo, un cubo tiene 6 caras pero ¡12 aristas! Contemos con cuidado.",
            "ejemplos": obtener_ejemplos_expandidos_fase6(1, 1),
            "interactivos": [
                {"pregunta": "¿Cuántas caras tiene un cubo regular?", "respuesta": "6", "feedback_acierto": "¡Correcto! Base, tapa y 4 lados.", "feedback_error": "Cuenta las superficies del dado: 6 en total."},
                {"pregunta": "¿Cuántos vértices tiene un cubo?", "respuesta": "8", "feedback_acierto": "¡Excelente! 4 esquinas arriba y 4 abajo.", "feedback_error": "Cuenta las esquinitas: 4 superiores y 4 inferiores."},
                {"pregunta": "¿Cuántas aristas tiene un cubo?", "respuesta": "12", "feedback_acierto": "¡Brillante! 4 arriba, 4 abajo y 4 columnas verticales.", "feedback_error": "Cuenta los bordes lineales: 12 en total."}
            ]
        },
        {
            "modulo_id": 1, "nivel_id": 2,
            "titulo": "Detección de bloques ocultos",
            "texto_descubrimiento": "¡Hora de usar la visión de rayos X en tu mente! 🕵️‍♀️ Cuando dibujamos bloques apilados en 3D, algunos cubos quedan escondidos detrás o debajo de otros.\nRecuerda la ley física: un bloque que está arriba no puede flotar mágicamente en el aire; necesita que haya bloques en el suelo y en los pisos de abajo para sostenerlo. ¡Tu misión es contar los bloques visibles y deducir cuántos están ocultos!",
            "diccionario": {"Perspectiva isométrica": "Dibujo técnico en 2D que representa un objeto 3D visto desde un ángulo."},
            "advertencia": "Mira con atención la altura. Si un cubo está en el nivel 3 (tercer piso), significa que obligatoriamente hay 2 cubos escondidos abajo sosteniéndolo.",
            "ejemplos": obtener_ejemplos_expandidos_fase6(1, 2),
            "interactivos": [
                {"pregunta": "Si ves un bloque a una altura de 3 niveles, ¿cuántos bloques hay en su columna completa?", "respuesta": "3", "feedback_acierto": "¡Correcto! El de arriba y los 2 de base.", "feedback_error": "Incluye el que ves y los que lo sostienen en los niveles inferiores."},
                {"pregunta": "En una estructura en forma de cruz, el bloque central está en el nivel 2. ¿Cuántos bloques ocultos hay debajo?", "respuesta": "1", "feedback_acierto": "¡Excelente! El primer nivel sostiene al segundo.", "feedback_error": "El nivel 1 sostiene al nivel 2."},
                {"pregunta": "Si cuento 5 bloques en total pero solo veo 4, ¿cuántos están ocultos?", "respuesta": "1", "feedback_acierto": "¡Brillante! Restamos 5 - 4 = 1.", "feedback_error": "Resta el total menos los visibles."}
            ]
        },
        {
            "modulo_id": 1, "nivel_id": 3,
            "titulo": "Asociación de moldes desplegados",
            "texto_descubrimiento": "¡Imagínate desarmar una caja de cartón por sus uniones y extenderla sobre la mesa! Eso es un molde desplegado.\nNos dice cómo se ve una figura tridimensional abierta y aplanada en dos dimensiones. En este nivel, vas a aprender a doblar mentalmente los moldes planos para descubrir qué cuerpo 3D se forma. ¡Es como doblar origami!",
            "diccionario": {"Molde desplegado": "La representación plana de las caras conectadas de un cuerpo tridimensional antes de plegarse."},
            "advertencia": "Al plegar, comprueba que las caras no choquen o se encimen. Si dos cuadrados se doblan al mismo lugar, ¡el molde no se cerrará correctamente!",
            "ejemplos": obtener_ejemplos_expandidos_fase6(1, 3),
            "interactivos": [
                {"pregunta": "¿Cuántos cuadrados debe tener un molde para formar un cubo cerrado?", "respuesta": "6", "feedback_acierto": "¡Correcto! Un cubo tiene 6 caras.", "feedback_error": "El cubo tiene 6 caras."},
                {"pregunta": "Si un molde tiene 5 caras, ¿formará un cubo cerrado? (1 para SÍ, 2 para NO)", "respuesta": "2", "feedback_acierto": "¡Excelente! Faltará una tapa.", "feedback_error": "Responde 2. Faltará una cara para cerrar el cubo."},
                {"pregunta": "Un molde de cilindro tiene 2 círculos y un...", "respuesta": "rectángulo", "feedback_acierto": "¡Brillante!", "feedback_error": "El tubo curvo se estira como un rectángulo."}
            ]
        },
        # --- MÓDULO 2: Patrones de Crecimiento ---
        {
            "modulo_id": 2, "nivel_id": 1,
            "titulo": "Análisis de sucesiones espaciales",
            "texto_descubrimiento": "¡Las figuras también pueden crecer de forma inteligente! 📈 Un patrón geométrico es una serie de construcciones que se expanden siguiendo una regla fija.\nPor ejemplo, si la Etapa 1 tiene 1 bloque y la Etapa 2 tiene 3 bloques, la regla es sumarle 2 bloques en cada paso. Si sigues esa regla, ¡puedes adivinar el futuro de la figura en la Etapa 4!",
            "diccionario": {"Sucesión espacial": "Grupo ordenado de formas geométricas que crecen con un patrón regular."},
            "advertencia": "Descubre primero el secreto: compara la Etapa 2 con la Etapa 1. ¿Cuántos bloques se añadieron? ¡Ese es el ritmo de crecimiento!",
            "ejemplos": obtener_ejemplos_expandidos_fase6(2, 1),
            "interactivos": [
                {"pregunta": "Si el patrón es 1, 3, 5, 7. ¿Cuántos bloques en la etapa 5?", "respuesta": "9", "feedback_acierto": "¡Correcto! Sumamos 2 al anterior.", "feedback_error": "Suma 2 al 7."},
                {"pregunta": "Si en etapa 1 hay 2 bloques, en etapa 2 hay 4 y en etapa 3 hay 6. ¿Regla? (escribe: suma 2)", "respuesta": "suma 2", "feedback_acierto": "¡Excelente! Aumenta en 2.", "feedback_error": "Aumenta en 2. Escribe 'suma 2'."},
                {"pregunta": "Patrón: 2, 5, 8. Siguiente número:", "respuesta": "11", "feedback_acierto": "¡Brillante!", "feedback_error": "Suma 3."}
            ]
        },
        {
            "modulo_id": 2, "nivel_id": 2,
            "titulo": "Conteo volumétrico estratificado",
            "texto_descubrimiento": "¡Para contar grandes pilas de bloques sin perder la cabeza, usamos pisos! 🏢\nEl conteo estratificado es una técnica de ingenieras que consiste en contar los bloques capa por capa horizontal (los estratos), de arriba hacia abajo. Luego, sumas las cantidades de cada capa. ¡Así ningún cubo oculto en el centro se te escapará!",
            "diccionario": {"Estrato": "Capa o piso de bloques a una misma altura en la construcción."},
            "advertencia": "Cuenta el piso de arriba primero, luego el del medio, y al final la base. ¡Apunta y suma ordenadamente!",
            "ejemplos": obtener_ejemplos_expandidos_fase6(2, 2),
            "interactivos": [
                {"pregunta": "Piso inferior 9, piso medio 4, piso superior 1. Total:", "respuesta": "14", "feedback_acierto": "¡Correcto! 9+4+1 = 14.", "feedback_error": "Suma 9+4+1."},
                {"pregunta": "Edificio de 3 pisos, 4 bloques por piso. Total:", "respuesta": "12", "feedback_acierto": "¡Excelente!", "feedback_error": "Multiplica 4x3."},
                {"pregunta": "Capa 1: 5 bloques, Capa 2: 3 bloques. Total:", "respuesta": "8", "feedback_acierto": "¡Brillante!", "feedback_error": "Suma 5+3."}
            ]
        },
        {
            "modulo_id": 2, "nivel_id": 3,
            "titulo": "Generalización algebraica",
            "texto_descubrimiento": "¡Imagina que te piden contar los bloques de la Etapa 100! Dibujarlo tardaría horas.\nAquí es donde brilla la generalización algebraica: creamos una fórmula matemática mágica usando la letra 'N' (que representa el número de etapa). Al reemplazar N por la etapa deseada, ¡la fórmula calcula la respuesta al instante!",
            "diccionario": {"Generalización": "Encontrar la fórmula o regla matemática que describe cómo se comporta una serie infinita."},
            "advertencia": "Fíjate muy bien en la regla. Si la regla es N + 4 y te piden la etapa 10, la cuenta es 10 + 4. ¡Reemplaza la N con cuidado!",
            "ejemplos": obtener_ejemplos_expandidos_fase6(2, 3),
            "interactivos": [
                {"pregunta": "Regla: Nx3. ¿Etapa 4?", "respuesta": "12", "feedback_acierto": "¡Correcto! 4x3 = 12.", "feedback_error": "Multiplica 4x3."},
                {"pregunta": "Regla: NxN. ¿Etapa 5?", "respuesta": "25", "feedback_acierto": "¡Excelente!", "feedback_error": "Multiplica 5x5."},
                {"pregunta": "Regla: N+4. ¿Etapa 10?", "respuesta": "14", "feedback_acierto": "¡Brillante!", "feedback_error": "Suma 10+4."}
            ]
        },
        # --- MÓDULO 3: Cubos Unitarios ---
        {
            "modulo_id": 3, "nivel_id": 1,
            "titulo": "Modelado del concepto de volumen (u³)",
            "texto_descubrimiento": "El volumen es la cantidad de espacio tridimensional que ocupa un cuerpo. ¡Cuánto lugar ocupa en el mundo!\nPara medir volumen, usamos cubos unitarios de 1x1x1 (u³). El volumen de una caja nos dice cuántos de estos cubitos idénticos caben guardados adentro. ¡Contemos cubos para descubrir el volumen!",
            "diccionario": {"Unidad cúbica (u³)": "Un cubo de medida estándar 1 de ancho, 1 de largo y 1 de alto que sirve para contar volumen."},
            "advertencia": "Recuerda que cuentas volumen en 3D (largo × ancho × alto). No vayas a contar solo las caras visibles, ¡incluye todo lo de adentro!",
            "ejemplos": obtener_ejemplos_expandidos_fase6(3, 1),
            "interactivos": [
                {"pregunta": "Si apilo 4 cubos en el suelo y luego pongo 4 cubos encima. Volumen total:", "respuesta": "8", "feedback_acierto": "¡Correcto!", "feedback_error": "Suma 4+4."},
                {"pregunta": "Una línea de 5 cubos, repetida 2 veces. Volumen:", "respuesta": "10", "feedback_acierto": "¡Excelente!", "feedback_error": "Multiplica 5x2."},
                {"pregunta": "Tres columnas de 3 cubos. Volumen:", "respuesta": "9", "feedback_acierto": "¡Brillante!", "feedback_error": "Multiplica 3x3."}
            ]
        },
        {
            "modulo_id": 3, "nivel_id": 2,
            "titulo": "Cálculo analítico formal de prismas",
            "texto_descubrimiento": "¡Ahora usaremos el superpoder de multiplicar! ⚡ Contar cubito por cubito en una caja grande es muy tardado.\nPara calcular el volumen de un prisma rectangular (como una caja de zapatos), usamos la fórmula matemática oficial: Volumen = Largo × Ancho × Alto. ¡Multiplicas las tres dimensiones y listo!",
            "diccionario": {"Prisma rectangular": "Cuerpo geométrico de caras planas con base rectangular."},
            "advertencia": "Asegúrate de multiplicar las tres dimensiones: base × fondo × altura. ¡No te saltes ninguna!",
            "ejemplos": obtener_ejemplos_expandidos_fase6(3, 2),
            "interactivos": [
                {"pregunta": "Caja de largo 5, ancho 2, alto 2. Volumen:", "respuesta": "20", "feedback_acierto": "¡Correcto! 5 x 2 x 2 = 20.", "feedback_error": "Multiplica largo x ancho x alto (5x2x2)."},
                {"pregunta": "Cubo de lado 3. Volumen:", "respuesta": "27", "feedback_acierto": "¡Excelente! 3 x 3 x 3 = 27.", "feedback_error": "Multiplica 3x3x3."},
                {"pregunta": "Habitación 4x4x3. Volumen:", "respuesta": "48", "feedback_acierto": "¡Brillante!", "feedback_error": "Multiplica 4x4x3."}
            ]
        },
        {
            "modulo_id": 3, "nivel_id": 3,
            "titulo": "Relación entre volumen cúbico y líquidos",
            "texto_descubrimiento": "¡Los cubos y los líquidos son mejores amigos! 💧 Existe una equivalencia directa entre el volumen y la capacidad de líquido.\nUn decímetro cúbico (dm³) es un cubo de 10x10x10 cm. Si lo llenas de agua, cabe exactamente un Litro (L) de líquido. ¡1 dm³ = 1 Litro! Y un centímetro cúbico (cm³) equivale a 1 mililitro (mL).",
            "diccionario": {"1 decímetro cúbico (dm³)": "Equivale exactamente a 1 Litro (L).", "1 centímetro cúbico (cm³)": "Equivale exactamente a 1 mililitro (mL)."},
            "advertencia": "¡Cuidado! Un metro cúbico (m³) es enorme. Contiene exactamente 1000 Litros de agua, no solo uno.",
            "ejemplos": obtener_ejemplos_expandidos_fase6(3, 3),
            "interactivos": [
                {"pregunta": "Un recipiente tiene 10 dm³. ¿Cuántos Litros de agua contiene?", "respuesta": "10", "feedback_acierto": "¡Correcto!", "feedback_error": "1 dm³ es igual a 1 Litro."},
                {"pregunta": "Una botella tiene 500 cm³. ¿Cuántos mL tiene?", "respuesta": "500", "feedback_acierto": "¡Excelente!", "feedback_error": "1 cm³ es igual a 1 mL."},
                {"pregunta": "Un tanque de 1 m³. ¿Cuántos Litros?", "respuesta": "1000", "feedback_acierto": "¡Brillante! Contiene 1000 L.", "feedback_error": "1 m³ contiene 1000 Litros."}
            ]
        },
        # --- MÓDULO 4: Medidas de Masa y Temperatura ---
        {
            "modulo_id": 4, "nivel_id": 1,
            "titulo": "Balanzas y Termómetros",
            "texto_descubrimiento": "¡En el laboratorio usamos herramientas! 🌡️ Las balanzas miden la masa (el peso de las cosas) y los termómetros miden qué tan caliente o frío está algo.\nPara pesos, 1 kilogramo (kg) equivale a 1000 gramos (g). Para temperaturas cotidianas, usamos la escala de grados Celsius (°C). ¡A aprender estas conversiones!",
            "diccionario": {"Kilogramo (kg)": "Unidad de masa (peso) que equivale a 1000 gramos.", "Grados Celsius (°C)": "Unidad de medida de la temperatura."},
            "advertencia": "Presta mucha atención a la unidad física de la pregunta: ¿kg o gramos?",
            "ejemplos": obtener_ejemplos_expandidos_fase6(4, 1),
            "interactivos": [
                {"pregunta": "¿Cuántos gramos hay en 3 kg?", "respuesta": "3000", "feedback_acierto": "¡Correcto! 3 x 1000 = 3000g.", "feedback_error": "Multiplica 3x1000."},
                {"pregunta": "Medio kilo (0,5 kg) son cuántos gramos:", "respuesta": "500", "feedback_acierto": "¡Excelente!", "feedback_error": "La mitad de 1000 es 500."},
                {"pregunta": "Si un termómetro sube de 10° a 25°, aumentó:", "respuesta": "15", "feedback_acierto": "¡Brillante! 25 - 10 = 15.", "feedback_error": "Resta la temperatura final menos la inicial: 25 - 10."}
            ]
        },
        {
            "modulo_id": 4, "nivel_id": 2,
            "titulo": "Variaciones térmicas y signo negativo",
            "texto_descubrimiento": "¡Cuando hace muchísimo frío, el termómetro marca bajo cero! ❄️\nLas temperaturas por debajo del cero se escriben con un signo negativo (como -2°C). Si la temperatura está a 5°C y baja 7 grados, pasas por debajo del cero y quedas a -2°C. ¡Aprenderemos a movernos en la escala fría!",
            "diccionario": {"Temperatura negativa": "Valores por debajo del cero absoluto de congelación del agua."},
            "advertencia": "Cuando restas y bajas del cero, sumas las distancias. De 2° a -3° bajó 5 grados en total.",
            "ejemplos": obtener_ejemplos_expandidos_fase6(4, 2),
            "interactivos": [
                {"pregunta": "Temperatura inicial 2°. Baja 5°. ¿Nueva temperatura?", "respuesta": "-3", "feedback_acierto": "¡Correcto! 2 - 5 = -3.", "feedback_error": "2 - 5 = -3."},
                {"pregunta": "Temperatura inicial -4°. Sube 10°. ¿Nueva temperatura?", "respuesta": "6", "feedback_acierto": "¡Excelente! -4 + 10 = 6.", "feedback_error": "-4 + 10 = 6."},
                {"pregunta": "Estaba a 10°, ahora está a -5°. ¿Cuánto bajó?", "respuesta": "15", "feedback_acierto": "¡Brillante! 10 hasta 0 son 10, y 5 más son 15.", "feedback_error": "10 hasta 0 son 10, y de 0 a -5 son 5 más. Suma 10+5."}
            ]
        },
        {
            "modulo_id": 4, "nivel_id": 3,
            "titulo": "La Máquina Kelvin",
            "texto_descubrimiento": "¡La ciencia espacial usa la escala Kelvin (K) para el espacio sideral! 👽\nConvertir grados Celsius a Kelvin es facilísimo con la regla mágica de la Máquina Kelvin: sumas <span class=\"keyword-highlight\">273</span>. Para ir de Kelvin a Celsius, restas 273. K = C + 273. ¡La escala Kelvin nunca tiene números negativos!",
            "diccionario": {"Escala Kelvin (K)": "Escala de temperatura científica absoluta donde el cero representa la inmovilidad de los átomos.", "Constante Kelvin": "El número 273 que usamos para convertir escalas."},
            "advertencia": "Kelvin no lleva el símbolo de grados (°). Escribimos simplemente 'K'. Y recuerda: ¡siempre sumas 273!",
            "ejemplos": obtener_ejemplos_expandidos_fase6(4, 3),
            "interactivos": [
                {"pregunta": "0°C en Kelvin es:", "respuesta": "273", "feedback_acierto": "¡Correcto! 0 + 273 = 273 K.", "feedback_error": "0 + 273."},
                {"pregunta": "100°C en Kelvin es:", "respuesta": "373", "feedback_acierto": "¡Excelente! 100 + 273 = 373 K.", "feedback_error": "100 + 273."},
                {"pregunta": "Si tengo 300 K, ¿cuántos grados Celsius son?", "respuesta": "27", "feedback_acierto": "¡Brillante! 300 - 273 = 27°C.", "feedback_error": "Resta 300 - 273."}
            ]
        }
    ]

    for data in niveles_teoria:
        nt = NivelTeoria(fase_id=FASE6_ID, **data)
        session.add(nt)

def _finalize_alts(correct, preferred: list, rng: random.Random, lo: int = None) -> list:
    """Devuelve exactamente 4 alternativas string DISTINTAS incluyendo `correct`.

    Prioriza los distractores de `preferred` (que suelen llevar feedback
    pedagógico en errores_previstos) y, si hacen falta más, rellena con valores
    enteros cercanos. Evita el bug de opciones repetidas (p.ej. [8, 6, 6, 10])
    cuando dos fórmulas de distractor colisionan.
    """
    correct = str(correct)
    out = [correct]
    seen = {correct}
    for d in preferred:
        ds = str(d)
        if ds not in seen:
            seen.add(ds)
            out.append(ds)
        if len(out) >= 4:
            return out
    # Relleno numérico cercano (respuestas enteras)
    try:
        base = int(float(correct))
        step = 1
        while len(out) < 4 and step < 80:
            for off in (step, -step, step + 1, -(step + 1)):
                cand = base + off
                if lo is not None and cand < lo:
                    continue
                cs = str(cand)
                if cs not in seen:
                    seen.add(cs)
                    out.append(cs)
                    break
            step += 1
    except (ValueError, TypeError):
        pass
    # Último recurso (respuestas de texto): sufijo para no quedar cortos
    i = 0
    while len(out) < 4:
        cs = f"{correct} ({i})"
        if cs not in seen:
            seen.add(cs)
            out.append(cs)
        i += 1
    return out


# --- Poliedros para M1L1: propiedades, artículo, desglose y figura SVG ---
_POLIEDROS_PROPS = {
    "cubo":                  {"caras": 6, "vertices": 8, "aristas": 12},
    "prisma rectangular":    {"caras": 6, "vertices": 8, "aristas": 12},
    "pirámide cuadrangular": {"caras": 5, "vertices": 5, "aristas": 8},
    "prisma triangular":     {"caras": 5, "vertices": 6, "aristas": 9},
}

_POLIEDRO_ARTICULO = {
    "cubo": "un cubo regular",
    "prisma rectangular": "un prisma rectangular (como una caja de zapatos)",
    "pirámide cuadrangular": "una pirámide con base cuadrada (pirámide cuadrangular)",
    "prisma triangular": "un prisma triangular",
}

_POLIEDRO_DESGLOSE = {
    ("cubo", "caras"): "6 caras cuadradas (tapa, base y 4 caras laterales)",
    ("cubo", "vertices"): "8 vértices (4 esquinas arriba y 4 abajo)",
    ("cubo", "aristas"): "12 aristas (4 arriba, 4 abajo y 4 columnas verticales)",
    ("prisma rectangular", "caras"): "6 caras rectangulares en total",
    ("prisma rectangular", "vertices"): "8 vértices (4 arriba y 4 abajo)",
    ("prisma rectangular", "aristas"): "12 aristas en total",
    ("pirámide cuadrangular", "caras"): "5 caras (1 base cuadrada y 4 caras triangulares)",
    ("pirámide cuadrangular", "vertices"): "5 vértices (4 en la base y la cúspide)",
    ("pirámide cuadrangular", "aristas"): "8 aristas (4 en la base y 4 que suben a la punta)",
    ("prisma triangular", "caras"): "5 caras (2 bases triangulares y 3 caras rectangulares)",
    ("prisma triangular", "vertices"): "6 vértices (3 abajo y 3 arriba)",
    ("prisma triangular", "aristas"): "9 aristas (3 arriba, 3 abajo y 3 verticales)",
}

# Etiquetas para pregunta (respeta el género: los vértices / las caras / las aristas)
_POLIEDRO_INTERROG = {"caras": "¿Cuántas caras", "vertices": "¿Cuántos vértices", "aristas": "¿Cuántas aristas"}
_POLIEDRO_PARAM_ES = {
    "caras": "las caras (paredes planas)",
    "vertices": "los vértices (esquinas)",
    "aristas": "las aristas (líneas/bordes)",
}

_POLIEDRO_SVG = {
    "cubo": (
        "<svg width='160' height='160' viewBox='0 0 120 120' style='margin:10px auto; display:block; background:#111827; border:2px solid #3B82F6; border-radius:12px;'>"
        "  <line x1='60' y1='20' x2='60' y2='60' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <line x1='60' y1='60' x2='90' y2='75' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <line x1='30' y1='75' x2='60' y2='60' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <polygon points='60,20 90,35 60,50 30,35' fill='#3B82F6' fill-opacity='0.25' stroke='#3B82F6' stroke-width='2'/>"
        "  <polygon points='30,35 60,50 60,90 30,75' fill='#3B82F6' fill-opacity='0.15' stroke='#3B82F6' stroke-width='2'/>"
        "  <polygon points='60,50 90,35 90,75 60,90' fill='#3B82F6' fill-opacity='0.2' stroke='#3B82F6' stroke-width='2'/>"
        "</svg>"
    ),
    "prisma rectangular": (
        "<svg width='160' height='160' viewBox='0 0 120 120' style='margin:10px auto; display:block; background:#111827; border:2px solid #3B82F6; border-radius:12px;'>"
        "  <line x1='60' y1='25' x2='60' y2='65' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <line x1='60' y1='65' x2='100' y2='80' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <line x1='20' y1='80' x2='60' y2='65' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <polygon points='60,25 100,40 60,55 20,40' fill='#3B82F6' fill-opacity='0.25' stroke='#3B82F6' stroke-width='2'/>"
        "  <polygon points='20,40 60,55 60,95 20,80' fill='#3B82F6' fill-opacity='0.15' stroke='#3B82F6' stroke-width='2'/>"
        "  <polygon points='60,55 100,40 100,80 60,95' fill='#3B82F6' fill-opacity='0.2' stroke='#3B82F6' stroke-width='2'/>"
        "</svg>"
    ),
    "pirámide cuadrangular": (
        "<svg width='160' height='160' viewBox='0 0 120 120' style='margin:10px auto; display:block; background:#111827; border:2px solid #3B82F6; border-radius:12px;'>"
        "  <line x1='30' y1='80' x2='60' y2='65' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <line x1='90' y1='80' x2='60' y2='65' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <line x1='60' y1='65' x2='60' y2='25' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <polygon points='60,25 30,80 60,95' fill='#3B82F6' fill-opacity='0.2' stroke='#3B82F6' stroke-width='2'/>"
        "  <polygon points='60,25 60,95 90,80' fill='#3B82F6' fill-opacity='0.25' stroke='#3B82F6' stroke-width='2'/>"
        "</svg>"
    ),
    "prisma triangular": (
        "<svg width='160' height='160' viewBox='0 0 120 120' style='margin:10px auto; display:block; background:#111827; border:2px solid #3B82F6; border-radius:12px;'>"
        "  <line x1='30' y1='45' x2='60' y2='25' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <line x1='90' y1='45' x2='60' y2='25' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <line x1='30' y1='85' x2='60' y2='65' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <line x1='90' y1='85' x2='60' y2='65' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <line x1='60' y1='25' x2='60' y2='65' stroke='#94A3B8' stroke-width='1.5' stroke-dasharray='3,3'/>"
        "  <polygon points='30,45 90,45 60,25' fill='#3B82F6' fill-opacity='0.15' stroke='none'/>"
        "  <polygon points='30,45 90,45 90,85 30,85' fill='#3B82F6' fill-opacity='0.2' stroke='#3B82F6' stroke-width='2'/>"
        "</svg>"
    ),
}


async def _gen_fase6_pool(rng: random.Random, mod_id: int, lvl_id: int) -> dict:
    nombre = rng.choice(NOMBRES)
    errores_previstos = {}

    if mod_id == 1:
        if lvl_id == 1:
            # Poliedros: caras, vértices, aristas (tabla de propiedades)
            solid_type = rng.choice(list(_POLIEDROS_PROPS.keys()))
            props = _POLIEDROS_PROPS[solid_type]
            param_key = rng.choice(["caras", "vertices", "aristas"])
            ans = props[param_key]
            ans_str = str(ans)

            # Distractores CONCEPTUALES: los otros dos atributos del mismo sólido,
            # cada uno con su feedback (así el error "contaste vértices" es alcanzable).
            preferred = []
            for other_key in ("caras", "vertices", "aristas"):
                if other_key == param_key:
                    continue
                other_val = props[other_key]
                if other_val == ans:
                    continue  # p.ej. pirámide: caras=vértices=5 → no sirve de distractor
                preferred.append(str(other_val))
                errores_previstos[str(other_val)] = (
                    f"Contaste {_POLIEDRO_PARAM_ES[other_key]} en lugar de {_POLIEDRO_PARAM_ES[param_key]}."
                )

            expl = f"{_POLIEDRO_ARTICULO[solid_type].capitalize()} tiene {_POLIEDRO_DESGLOSE[(solid_type, param_key)]}."
            # Variedad de SITUACIÓN: la mitad de las veces enmarcamos la pregunta con
            # un objeto real que tiene esa forma (un dado, una tienda de campaña, etc.),
            # conectando el cuerpo geométrico con la vida cotidiana del niño.
            interrog_min = _POLIEDRO_INTERROG[param_key].replace("¿", "").lower()  # "cuántas caras"
            if rng.random() < 0.7:
                objeto = rng.choice(_POLIEDRO_OBJETOS[solid_type])
                plantillas = [
                    f"Observa {objeto}: tiene la forma de {_POLIEDRO_ARTICULO[solid_type]}. ¿{interrog_min.capitalize()} tiene?",
                    f"{objeto.capitalize()} es {_POLIEDRO_ARTICULO[solid_type]}. ¿{interrog_min.capitalize()} tiene en total?",
                    f"{nombre} encontró {objeto}, que es {_POLIEDRO_ARTICULO[solid_type]}. ¿{interrog_min.capitalize()} tiene?",
                ]
                enunciado = rng.choice(plantillas) + "<br/>" + _POLIEDRO_SVG[solid_type]
            else:
                enunciado = (
                    f"{_POLIEDRO_INTERROG[param_key]} tiene {_POLIEDRO_ARTICULO[solid_type]}?<br/>"
                    + _POLIEDRO_SVG[solid_type]
                )
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "alts": _finalize_alts(ans_str, preferred, rng, lo=1),
            }
        elif lvl_id == 2:
            # Bloques ocultos (cubos isométricos). Cada figura tiene total y ocultos
            # verificados a mano (los "ocultos" son los cubos que sostienen a otros y
            # no se ven en la vista isométrica).
            _SHAPES_OCULTOS = [
                ([(0,0,0), (1,0,0), (0,1,0), (0,0,1)], 4, 0),
                ([(0,0,0), (1,0,0), (0,1,0), (1,1,0), (0,0,1), (1,0,1), (0,1,1)], 7, 1),
                ([(0,0,0), (1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1)], 6, 1),
                ([(0,0,0), (1,0,0), (2,0,0), (0,1,0), (1,1,0), (0,2,0),
                  (0,0,1), (1,0,1), (0,1,1), (0,0,2)], 10, 3),
                # Cubo macizo 2×2×2: en vista isométrica se ven 7, 1 queda oculto detrás-abajo.
                ([(x,y,z) for x in range(2) for y in range(2) for z in range(2)], 8, 1),
                # Base 3×3 (9) con un cubo central encima: el cubo central de abajo (1,1,0)
                # queda tapado por sus 8 vecinos y por el de arriba → 1 oculto.
                ([(x,y,0) for x in range(3) for y in range(3)] + [(1,1,1)], 10, 1),
                # Escalera de 3 peldaños: 6 + 3 + 1.
                ([(0,0,0),(1,0,0),(2,0,0),(0,1,0),(1,1,0),(2,1,0),
                  (0,0,1),(1,0,1),(0,0,2)], 9, 2),
            ]
            shape_idx = rng.randint(0, len(_SHAPES_OCULTOS) - 1)
            cubes, total_cubes, ocultos = _SHAPES_OCULTOS[shape_idx]

            cache_key = f"iso_cubes_v2_{shape_idx}"
            if cache_key in _graphic_url_cache:
                url = _graphic_url_cache[cache_key]
            else:
                img_bytes = generate_isometric_cubes_image(cubes)
                url = await storage_service.upload_question_graphic(img_bytes, f"iso_cubes_v2_{shape_idx}.png")
                _graphic_url_cache[cache_key] = url

            construccion = rng.choice(CONSTRUCCIONES_CUBOS)
            material = rng.choice(MATERIALES_CUBOS)
            q_type = rng.choice(["total", "ocultos"])
            if q_type == "total":
                ans = total_cubes
                ans_str = str(ans)
                plantillas = [
                    f"{nombre} armó esta {construccion} con cubos {material} de 1 cm³. ¿Cuál es el volumen total (cantidad de cubos) de la figura?",
                    f"Observa la {construccion} de bloques {material}. Contando también los cubos escondidos que sirven de apoyo, ¿cuántos cubos de 1 cm³ hay en total?",
                    f"Esta {construccion} está hecha con bloques {material} idénticos. Cuenta capa por capa: ¿cuál es el volumen total en cubos?",
                ]
                enunciado = rng.choice(plantillas)
                expl = f"Contamos los cubos piso por piso, incluyendo los ocultos: hay {total_cubes} cubos en total ({total_cubes} cm³)."
                if ocultos > 0:
                    errores_previstos[str(total_cubes - ocultos)] = "Solo contaste los bloques visibles. Los de arriba se apoyan en otros ocultos abajo."
            else:
                ans = ocultos
                ans_str = str(ans)
                plantillas = [
                    f"En la {construccion} de bloques {material} de {nombre}, algunos cubos están escondidos sosteniendo a los de arriba. ¿Cuántos cubos están completamente ocultos a la vista?",
                    f"Observa esta {construccion}. Para que los cubos de arriba no floten, debe haber cubos ocultos debajo. ¿Cuántos cubos no se ven en la imagen?",
                ]
                enunciado = rng.choice(plantillas)
                expl = f"Los cubos de pisos superiores se apoyan en otros de abajo. Hay exactamente {ocultos} cubo(s) oculto(s)."
                errores_previstos[str(total_cubes - ocultos)] = "Ese es el número de bloques que SÍ se ven. La pregunta pide cuántos NO se ven."

            datos_numericos = {"cubes": cubes, "tipo_visual": "imagen", "url": url}
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "datos_numericos": datos_numericos,
                "alts": _finalize_alts(ans_str, [str(ans+1), str(ans-1), str(ans+2), str(ans+3)], rng, lo=0)
            }
        else:
            # Moldes desplegados (7 cuerpos distintos, no solo 3)
            _MOLDES = [
                {"ans": "cubo", "desc": "6 cuadrados iguales conectados en forma de cruz",
                 "expl": "Un cubo regular tiene exactamente 6 caras cuadradas idénticas.",
                 "dist": ["prisma rectangular", "pirámide cuadrangular", "cilindro", "prisma triangular"]},
                {"ans": "prisma rectangular", "desc": "6 rectángulos (no todos cuadrados) formando una caja alargada",
                 "expl": "6 caras rectangulares forman un prisma rectangular, como una caja de zapatos.",
                 "dist": ["cubo", "pirámide cuadrangular", "cilindro", "prisma triangular"]},
                {"ans": "pirámide cuadrangular", "desc": "1 cuadrado en el centro y 4 triángulos iguales pegados a sus lados",
                 "expl": "El cuadrado es la base y los 4 triángulos se unen en la punta: una pirámide cuadrangular.",
                 "dist": ["cubo", "prisma rectangular", "cono", "tetraedro"]},
                {"ans": "tetraedro", "desc": "4 triángulos equiláteros iguales",
                 "expl": "4 triángulos equiláteros forman un tetraedro (pirámide triangular de 4 caras).",
                 "dist": ["cubo", "prisma triangular", "octaedro", "pirámide cuadrangular"]},
                {"ans": "prisma triangular", "desc": "2 triángulos iguales y 3 rectángulos",
                 "expl": "2 bases triangulares y 3 caras rectangulares forman un prisma triangular (como una tienda de campaña).",
                 "dist": ["pirámide cuadrangular", "cubo", "cilindro", "tetraedro"]},
                {"ans": "cilindro", "desc": "2 círculos iguales y 1 rectángulo que los une",
                 "expl": "Los 2 círculos son las tapas y el rectángulo se enrolla como pared curva: un cilindro.",
                 "dist": ["cono", "esfera", "prisma rectangular", "cubo"]},
                {"ans": "cono", "desc": "1 círculo y 1 sector (abanico) curvo pegado a su borde",
                 "expl": "El círculo es la base y el sector curvo se enrolla hasta una punta: un cono.",
                 "dist": ["cilindro", "pirámide cuadrangular", "esfera", "tetraedro"]},
            ]
            m = rng.choice(_MOLDES)
            ans_str = m["ans"]
            plantillas = [
                f"El molde desplegado de {nombre} está formado por {m['desc']}. ¿Qué cuerpo tridimensional se forma al plegarlo?",
                f"Si doblas un molde plano de cartón que tiene {m['desc']}, ¿qué figura 3D obtienes?",
                f"{nombre} recortó un molde con {m['desc']}. Al armarlo y cerrarlo, ¿qué cuerpo geométrico forma?",
            ]
            enunciado = rng.choice(plantillas)
            expl = m["expl"]
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "alts": _finalize_alts(ans_str, m["dist"], rng)
            }
    elif mod_id == 2:
        if lvl_id == 1:
            base = rng.choice([1, 2, 3])
            growth = rng.choice([2, 3, 4])
            etapa_target = rng.choice([4, 5])
            ans = base + (etapa_target - 1) * growth
            ans_str = str(ans)
            
            s1 = base
            s2 = base + growth
            s3 = base + 2*growth
            
            enunciado = f"Una sucesión de figuras que construye {nombre} crece etapa por etapa de forma constante. La Etapa 1 tiene {s1} bloque(s), la Etapa 2 tiene {s2} bloques, y la Etapa 3 tiene {s3} bloques. Si el patrón continúa igual, ¿cuántos bloques tendrá la Etapa {etapa_target}?"
            expl = f"El crecimiento es de +{growth} bloques por etapa ({s2} - {s1} = {growth}). Sumamos sucesivamente para llegar a la Etapa {etapa_target}: {ans} bloques."
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "alts": [ans_str, str(ans + growth), str(ans - growth), str(ans + 1)]
            }
        elif lvl_id == 2:
            # Rangos ampliados (antes 12 combos) — base 3×3, medio 2×2, tope 1×2.
            p1 = rng.randint(6, 9)   # piso inferior (grilla 3×3)
            p2 = rng.randint(2, 4)   # piso medio (grilla 2×2)
            p3 = rng.randint(1, 2)   # piso superior (grilla 1×2)
            ans = p1 + p2 + p3
            ans_str = str(ans)

            cubes = []
            count1 = 0
            for x in range(3):
                for y in range(3):
                    if count1 < p1:
                        cubes.append((x, y, 0)); count1 += 1
            count2 = 0
            for x in range(2):
                for y in range(2):
                    if count2 < p2:
                        cubes.append((x, y, 1)); count2 += 1
            count3 = 0
            for x in range(2):
                if count3 < p3:
                    cubes.append((x, 0, 2)); count3 += 1

            cache_key = f"iso_strat_v2_{p1}_{p2}_{p3}"
            if cache_key in _graphic_url_cache:
                url = _graphic_url_cache[cache_key]
            else:
                img_bytes = generate_isometric_cubes_image(cubes)
                url = await storage_service.upload_question_graphic(img_bytes, f"iso_strat_v2_{p1}_{p2}_{p3}.png")
                _graphic_url_cache[cache_key] = url

            construccion = rng.choice(CONSTRUCCIONES_CUBOS)
            plantillas = [
                f"Para hallar el volumen de la {construccion} de {nombre}, contamos capa por capa: el piso inferior tiene {p1} bloques, el medio {p2} y el superior {p3}. ¿Cuál es el volumen total en u³?",
                f"Una {construccion} tiene 3 estratos: {p1} bloques abajo, {p2} en el medio y {p3} arriba. Sumando las capas, ¿cuántos cubos de 1 u³ tiene en total?",
                f"{nombre} apila bloques en 3 pisos: {p1} + {p2} + {p3}. ¿Cuál es el volumen total (u³) de la {construccion}?",
            ]
            enunciado = rng.choice(plantillas)
            datos_numericos = {"cubes": cubes, "tipo_visual": "imagen", "url": url}
            expl = f"Sumamos las capas de abajo hacia arriba: {p1} + {p2} + {p3} = {ans} u³."

            errores_previstos[str(p1*p2)] = "Multiplicaste las capas. Debes SUMAR los bloques de todas las capas para el volumen total."

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "datos_numericos": datos_numericos,
                "alts": _finalize_alts(ans_str, [str(ans+2), str(ans-2), str(p1*p2), str(ans+1)], rng, lo=1)
            }
        else:
            mult = rng.choice([2, 3, 5])
            add = rng.choice([1, 2, 4])
            n_val = rng.choice([10, 20])
            ans = n_val * mult + add
            ans_str = str(ans)
            
            enunciado = f"La regla general que descubrió {nombre} para calcular el número de bloques de una estructura en la etapa N es: <b>{mult}N + {add}</b>. ¿Cuántos bloques se necesitarán para construir la etapa N = {n_val}?"
            expl = f"Reemplazamos N por {n_val} en la fórmula: {mult} × ({n_val}) + {add} = {mult * n_val} + {add} = {ans} bloques."
            
            errores_previstos[str(n_val * mult)] = f"Olvidaste sumar el '+ {add}' al final de la fórmula."
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "alts": [ans_str, str(ans + mult), str(ans - add), str(n_val * mult)]
            }
    elif mod_id == 3:
        if lvl_id == 1:
            # Rangos ampliados (antes 2-4 × 2-3 × 2-3 = 12 combos) para más variedad de
            # figuras; se mantiene contable por capas para el nivel de "modelar volumen".
            largo = rng.randint(2, 5)
            ancho = rng.randint(2, 4)
            alto = rng.randint(2, 4)
            ans = largo * ancho * alto
            ans_str = str(ans)

            cubes = [(x, y, z) for x in range(largo) for y in range(ancho) for z in range(alto)]

            cache_key = f"iso_vol_{largo}_{ancho}_{alto}"
            if cache_key in _graphic_url_cache:
                url = _graphic_url_cache[cache_key]
            else:
                img_bytes = generate_isometric_cubes_image(cubes)
                url = await storage_service.upload_question_graphic(img_bytes, f"iso_vol_{largo}_{ancho}_{alto}.png")
                _graphic_url_cache[cache_key] = url

            # Variedad de SITUACIÓN: distintas construcciones y materiales, y a veces
            # se indican las dimensiones en el texto (medir) y otras se pide contar la
            # imagen (contar) — dos formas distintas de demostrar el mismo concepto.
            construccion = rng.choice(CONSTRUCCIONES_CUBOS)
            material = rng.choice(MATERIALES_CUBOS)
            if rng.random() < 0.5:
                plantillas = [
                    f"{nombre} armó una {construccion} con cubitos {material} de 1 u³. Contando capa por capa en la imagen, ¿cuál es su volumen total (en u³)?",
                    f"Observa la {construccion} de cubitos {material} de 1 u³. ¿Cuántos cubitos la componen en total (volumen en u³)?",
                    f"Cuenta los cubitos de 1 u³ de esta {construccion} {material} que se muestra en la imagen. ¿Cuál es su volumen?",
                ]
            else:
                plantillas = [
                    f"La {construccion} {material} de {nombre} mide {largo} cubos de largo, {ancho} de ancho y {alto} de alto (mira la imagen). ¿Cuántos cubitos de 1 u³ tiene en total?",
                    f"Un bloque {material} tiene {largo} × {ancho} × {alto} cubitos de 1 u³. ¿Cuál es su volumen total?",
                ]
            enunciado = rng.choice(plantillas)
            datos_numericos = {"cubes": cubes, "tipo_visual": "imagen", "url": url}
            expl = f"Contamos por capas o multiplicamos las dimensiones: {largo} × {ancho} × {alto} = {ans} cubitos (u³)."

            errores_previstos[str(largo+ancho+alto)] = "Sumaste las dimensiones (L+A+H) en lugar de multiplicarlas (L×A×H) para hallar el volumen."

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "datos_numericos": datos_numericos,
                "alts": _finalize_alts(ans_str, [str(largo+ancho+alto), str(ans-2), str(ans+2), str(ans+largo)], rng, lo=1)
            }
        elif lvl_id == 2:
            largo = rng.randint(3, 8)
            ancho = rng.randint(2, 5)
            alto = rng.randint(2, 6)
            ans = largo * ancho * alto
            ans_str = str(ans)
            contenedor = rng.choice(CONTENEDORES)
            
            enunciado = f"Calcula el volumen de un(a) {contenedor} en forma de prisma rectangular que mide {largo} cm de largo, {ancho} cm de ancho y {alto} cm de alto."
            expl = f"Aplicamos la fórmula del volumen de un prisma: Largo × Ancho × Alto. Multiplicamos {largo} × {ancho} × {alto} = {ans} cm³."
            
            errores_previstos[str(largo+ancho+alto)] = "Sumaste las dimensiones (L+A+H) en lugar de multiplicarlas (L×A×H)."
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "alts": [ans_str, str(ans + 10), str(ans - 10), str(largo + ancho + alto)]
            }
        else:
            unit = rng.choice(["dm3_to_l", "cm3_to_ml", "m3_to_l"])
            liquido = rng.choice(LIQUIDOS)
            if unit == "dm3_to_l":
                val = rng.randint(2, 20)
                ans = val
                ans_str = str(ans)
                enunciado = f"El {liquido} de {nombre} tiene una capacidad interior de {val} dm³. ¿Cuántos litros (L) de agua caben en él?"
                expl = "Como 1 decímetro cúbico (dm³) equivale exactamente a 1 litro (L), la cantidad es la misma."
                errores_previstos[str(val*10)] = "1 dm³ equivale a 1 Litro exactamente. Multiplicaste por 10."
            elif unit == "cm3_to_ml":
                val = rng.choice([250, 500, 750, 1000])
                ans = val
                ans_str = str(ans)
                enunciado = f"Un {liquido} contiene {val} cm³ de jarabe. ¿A cuántos mililitros (mL) equivale esta cantidad?"
                expl = "Como 1 centímetro cúbico (cm³) equivale exactamente a 1 mililitro (mL), la cantidad es la misma."
                errores_previstos[str(val//10)] = "1 cm³ equivale a 1 mL exactamente."
            else:
                val = rng.randint(1, 5)
                ans = val * 1000
                ans_str = str(ans)
                enunciado = f"Un(a) {liquido} grande tiene un volumen de {val} m³. ¿Cuántos litros (L) de agua se necesitan para llenarla(o) por completo?"
                expl = "Como 1 metro cúbico (m³) equivale exactamente a 1000 litros (L), multiplicamos por 1000."
                errores_previstos[str(val*100)] = "1 m³ contiene MIL (1000) Litros. Multiplicaste solo por 100."
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "alts": [ans_str, str(ans//10 if ans > 10 else ans+1), str(ans*10 if ans < 1000 else ans-100), str(ans+10)]
            }
    else: # mod_id == 4
        if lvl_id == 1:
            q_type = rng.choice(["weight", "weight", "g_to_kg", "temp_read"])
            if q_type == "weight":
                # Rango ampliado de pesos (antes solo 4 valores fijos).
                kg = rng.choice([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.5, 10.0])
                ans = int(kg * 1000)
                ans_str = str(ans)
                masa = rng.choice(MASAS)
                plantillas = [
                    f"En una balanza electrónica, un(a) {masa} de {nombre} pesa {kg} kg. ¿Cuál es su masa en gramos (g)?",
                    f"{nombre} pesa un(a) {masa} y la balanza marca {kg} kg. ¿A cuántos gramos (g) equivale?",
                    f"Un(a) {masa} tiene una masa de {kg} kg. Conviértela a gramos (g).",
                ]
                enunciado = rng.choice(plantillas)
                expl = f"Como 1 kg = 1000 g, multiplicamos {kg} × 1000 = {ans} g."
                errores_previstos[str(int(kg*100))] = "Multiplicaste por 100. Recuerda que kilo significa MIL (1000 gramos)."
                alts = [ans_str, str(ans+500), str(int(kg*100)), str(int(kg*10))]
                datos_numericos = {}
            elif q_type == "g_to_kg":
                # Sentido inverso g → kg: nueva SITUACIÓN, mismo concepto.
                kg = rng.choice([1.0, 2.0, 3.0, 4.0, 1.5, 2.5, 0.5])
                grams = int(kg * 1000)
                ans_str = str(kg) if kg != int(kg) else str(int(kg))
                masa = rng.choice(MASAS)
                enunciado = f"La balanza de {nombre} muestra que un(a) {masa} pesa {grams} gramos. ¿A cuántos kilogramos (kg) equivale?"
                expl = f"Como 1000 g = 1 kg, dividimos {grams} ÷ 1000 = {ans_str} kg."
                errores_previstos[str(grams*1000)] = "Multiplicaste por 1000 en vez de dividir. Para pasar de gramos a kilos se divide."
                alts = [ans_str, str(grams), str(grams//100), str(int(kg)+1 if kg==int(kg) else round(kg+1,1))]
                datos_numericos = {}
            else:  # temp_read
                temp = rng.randint(8, 42)
                ans_str = f"{temp}"
                cache_key = f"therm_{temp}"
                if cache_key in _graphic_url_cache:
                    url = _graphic_url_cache[cache_key]
                else:
                    img_bytes = generate_thermometer_image(float(temp))
                    url = await storage_service.upload_question_graphic(img_bytes, f"therm_{temp}.png")
                    _graphic_url_cache[cache_key] = url
                escenario_t = rng.choice(TEMPERATURAS)
                plantillas = [
                    f"Observa la escala del termómetro del {escenario_t} en la imagen. ¿Qué temperatura marca en grados Celsius (°C)?",
                    f"{nombre} revisa el termómetro del {escenario_t}. Según la imagen, ¿cuántos grados Celsius (°C) marca?",
                    f"Lee la temperatura que señala el líquido rojo en el termómetro del {escenario_t} (mira la imagen). ¿Cuántos °C son?",
                ]
                enunciado = rng.choice(plantillas)
                # Imagen PNG del termómetro (escala sin número exacto) para no revelar la respuesta.
                datos_numericos = {"url": url, "tipo_visual": "imagen", "valor": temp, "min": 10, "max": 45, "unidad": "°C"}
                expl = f"El nivel del líquido rojo coincide con la marca de {temp}°C en la escala."
                alts = [ans_str, str(temp + 5), str(temp - 5), str(temp + 3)]
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "datos_numericos": datos_numericos,
                "alts": _finalize_alts(ans_str, alts[1:], rng)
            }
        elif lvl_id == 2:
            init_temp = rng.randint(1, 15)
            drop = rng.randint(init_temp + 2, init_temp + 10)
            ans = init_temp - drop
            ans_str = str(ans)
            
            cache_key = f"therm_neg_{ans}"
            if cache_key in _graphic_url_cache:
                url = _graphic_url_cache[cache_key]
            else:
                img_bytes = generate_thermometer_image(float(ans))
                url = await storage_service.upload_question_graphic(img_bytes, f"therm_{ans}.png")
                _graphic_url_cache[cache_key] = url

            escenario_t = rng.choice(TEMPERATURAS)
            enunciado = f"En la mañana la temperatura en el {escenario_t} era de {init_temp}°C. Por la tarde, la temperatura bajó {drop}°C, llegando al nivel bajo cero mostrado en la imagen. ¿Cuál es la nueva temperatura en grados Celsius (°C)?"
            # Imagen PNG (escala sin número exacto) para no revelar la respuesta.
            datos_numericos = {
                "url": url,
                "init": init_temp, "drop": drop, "final": ans,
                "tipo_visual": "imagen",
                "valor": ans,
                "min": -20,
                "max": 20,
                "unidad": "°C"
            }
            expl = f"Restamos la variación a la temperatura inicial: {init_temp} - {drop} = {ans}°C. Al bajar del cero, el resultado es negativo."
            
            errores_previstos[str(init_temp + drop)] = "Sumaste la temperatura en lugar de restarla (bajó = restar)."
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "datos_numericos": datos_numericos,
                "alts": [ans_str, str(ans - 2), str(-ans), str(init_temp + drop)]
            }
        else:
            celsius = rng.randint(-15, 45)
            ans = celsius + 273
            ans_str = str(ans)
            escenario_t = rng.choice(TEMPERATURAS)
            
            enunciado = f"En el {escenario_t} espacial, un sensor registra una temperatura de {celsius}°C. ¿Cuál es esta temperatura expresada en la escala absoluta de Kelvin (K)?"
            expl = f"Para convertir grados Celsius a Kelvin, sumamos 273 a la temperatura en Celsius: {celsius} + 273 = {ans} K."
            
            errores_previstos[str(celsius - 273)] = "Restaste 273. Para convertir de Celsius a Kelvin debes SUMAR 273."
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "errores_previstos": errores_previstos,
                "expl": expl,
                "alts": [ans_str, str(ans + 100), str(celsius - 273), str(celsius)]
            }

async def seed_practica_pool(session: AsyncSession):
    print("Sembrando pool de práctica Fase 6 (familias con variantes espejo)...")
    sections = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 2), (2, 3),
        (3, 1), (3, 2), (3, 3),
        (4, 1), (4, 2), (4, 3)
    ]

    # 30 familias × 4 variantes (1 original + 3 espejo) = 120 preguntas por nivel.
    # `estructura_padre_id` agrupa la familia: es lo que cuenta el progreso de
    # práctica libre (COUNT DISTINCT en router.py) y lo que habilita el Bucle
    # Espejo + el modal de Rescate. Sin esto el nivel es imposible de aprobar.
    FAMILIAS_POR_NIVEL = 30

    for mod_id, lvl_id in sections:
        seccion_id = mod_id * 100 + lvl_id
        for fam in range(1, FAMILIAS_POR_NIVEL + 1):
            padre_id = f"f6_m{mod_id}_l{lvl_id}_fam_{fam:03d}"
            for var in range(4):
                es_espejo = var > 0
                rng = random.Random(FASE6_ID * 100000 + seccion_id * 1000 + fam * 10 + var)
                q_data = await _gen_fase6_pool(rng, mod_id, lvl_id)

                # 4 alternativas garantizadas distintas (evita opciones repetidas).
                alts = _finalize_alts(q_data["respuesta_correcta"], q_data.get("alts", []), rng)

                # PRESERVAR los datos visuales (url de cubos/termómetro, tipo_visual)
                # generados por _gen_fase6_pool en lugar de descartarlos.
                datos = dict(q_data.get("datos_numericos") or {})
                datos["fase6"] = True
                datos["es_espejo"] = es_espejo

                p = Pregunta(
                    fase_id=FASE6_ID, seccion=seccion_id, estructura_padre_id=padre_id,
                    operacion=OperacionEnum.MIXTA,
                    tipo_pregunta=TipoPreguntaEnum.MULTIPLE_OPCION, enunciado=q_data["enunciado"],
                    respuesta_correcta=q_data["respuesta_correcta"], datos_numericos=datos,
                    errores_previstos=q_data.get("errores_previstos", {}),
                    explicacion_paso_a_paso={"titulo": "Resolución", "pasos": [{"orden": 1, "texto": q_data["expl"]}]},
                    estado=StatusEnum.ACTIVO
                )
                for idx, alt in enumerate(alts):
                    is_correct = (alt == q_data["respuesta_correcta"])
                    error_msg = q_data.get("errores_previstos", {}).get(alt, "Esa alternativa es incorrecta.") if not is_correct else None
                    p.alternativas.append(Alternativa(texto=alt, es_correcta=is_correct, orden=idx+1, tipo_error=TipoErrorEnum.CALCULO if not is_correct else None, feedback_error=error_msg))
                session.add(p)
        await session.commit()

async def seed_preguntas_desafios(session: AsyncSession):
    print("Sembrando pool de Desafíos de Fase 6 (30 preguntas por desafío)...")
    for modulo_id in range(1, 5):
        for desafio_id in (11, 12, 13):
            seccion_id = modulo_id * 1000 + desafio_id
            
            for idx in range(1, 31):
                rng = random.Random(FASE6_ID * 1000000 + seccion_id * 1000 + idx)
                lvl_id = rng.choice([1, 2, 3])
                q_data = await _gen_fase6_pool(rng, modulo_id, lvl_id)
                
                tipo_pregunta = TipoPreguntaEnum.MULTIPLE_OPCION if desafio_id in (11, 12) else TipoPreguntaEnum.RESPUESTA_NUMERICA
                if not q_data["respuesta_correcta"].lstrip('-').isdigit():
                    tipo_pregunta = TipoPreguntaEnum.MULTIPLE_OPCION

                # PRESERVAR los datos visuales (cubos/termómetro) también en desafíos.
                datos = dict(q_data.get("datos_numericos") or {})
                datos["es_desafio"] = True

                p = Pregunta(
                    fase_id=FASE6_ID, seccion=seccion_id, operacion=OperacionEnum.MIXTA,
                    tipo_pregunta=tipo_pregunta, enunciado=q_data["enunciado"],
                    respuesta_correcta=q_data["respuesta_correcta"], datos_numericos=datos,
                    errores_previstos=q_data.get("errores_previstos", {}),
                    explicacion_paso_a_paso={"titulo": "Desafío", "pasos": [{"orden": 1, "texto": q_data["expl"]}]},
                    estado=StatusEnum.ACTIVO
                )

                if tipo_pregunta == TipoPreguntaEnum.MULTIPLE_OPCION:
                    alts = _finalize_alts(q_data["respuesta_correcta"], q_data.get("alts", []), rng)
                    for idx_alt, alt in enumerate(alts):
                        is_correct = (alt == q_data["respuesta_correcta"])
                        error_msg = q_data.get("errores_previstos", {}).get(alt, "Esa alternativa es incorrecta.") if not is_correct else None
                        p.alternativas.append(Alternativa(texto=alt, es_correcta=is_correct, orden=idx_alt+1, tipo_error=TipoErrorEnum.CALCULO if not is_correct else None, feedback_error=error_msg))
                session.add(p)
    await session.commit()

async def seed_configuracion_progreso(session: AsyncSession):
    print("Sembrando configuraciones de progreso Fase 6...")
    
    # 1. Configuración por defecto de la Fase
    config_def = ConfiguracionProgreso(
        fase_id=FASE6_ID, seccion=0, operacion=OperacionEnum.MIXTA,
        cantidad_requerida=15, porcentaje_aprobacion=90, orden_desbloqueo=99,
        tipo_feedback="simple", usa_cronometro=True, tiempo_default_segundos=60
    )
    session.add(config_def)
    
    # 2. Configuraciones de Niveles de Práctica Libre
    sections = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 2), (2, 3),
        (3, 1), (3, 2), (3, 3),
        (4, 1), (4, 2), (4, 3)
    ]
    for mod_id, lvl_id in sections:
        seccion_id = mod_id * 100 + lvl_id
        config = ConfiguracionProgreso(
            fase_id=FASE6_ID, seccion=seccion_id, operacion=OperacionEnum.MIXTA,
            cantidad_requerida=10, porcentaje_aprobacion=80, orden_desbloqueo=seccion_id,
            tipo_feedback="completo", usa_cronometro=False, tiempo_default_segundos=0
        )
        session.add(config)
        
    # 3. Configuraciones de Desafíos por Módulo
    for mod_id in range(1, 5):
        # Desafío 11
        config_11 = ConfiguracionProgreso(
            fase_id=FASE6_ID, seccion=mod_id * 1000 + 11, operacion=OperacionEnum.MIXTA,
            cantidad_requerida=20, porcentaje_aprobacion=90, orden_desbloqueo=mod_id * 1000 + 11,
            tipo_feedback="simple", usa_cronometro=True, tiempo_default_segundos=25
        )
        session.add(config_11)
        # Desafío 12
        config_12 = ConfiguracionProgreso(
            fase_id=FASE6_ID, seccion=mod_id * 1000 + 12, operacion=OperacionEnum.MIXTA,
            cantidad_requerida=20, porcentaje_aprobacion=90, orden_desbloqueo=mod_id * 1000 + 12,
            tipo_feedback="simple", usa_cronometro=True, tiempo_default_segundos=40
        )
        session.add(config_12)
        # Desafío 13
        config_13 = ConfiguracionProgreso(
            fase_id=FASE6_ID, seccion=mod_id * 1000 + 13, operacion=OperacionEnum.MIXTA,
            cantidad_requerida=10, porcentaje_aprobacion=90, orden_desbloqueo=mod_id * 1000 + 13,
            tipo_feedback="simple", usa_cronometro=True, tiempo_default_segundos=50
        )
        session.add(config_13)
        
    await session.commit()

async def run_fase6_seed():
    print("=" * 60)
    print("Iniciando inyección de datos semilla de Fase 6...")
    from app.seed import should_seed_phase, update_seed_version, SEED_VERSIONS
    async with AsyncSessionLocal() as session:
        if not await should_seed_phase(session, "fase_6", FASE6_ID):
            return
        
        res = await session.execute(select(Fase).where(Fase.id == FASE6_ID))
        if not res.scalar_one_or_none():
            fase = Fase(id=FASE6_ID, nombre="Geometría Espacial, Volumen y Magnitudes Físicas", descripcion="Desarrollar la visualización tridimensional, el razonamiento abstracto analítico y la medición de magnitudes.", orden=6, estado=StatusEnum.ACTIVO)
            session.add(fase)
            await session.flush()
            
        await clear_fase6_data(session)
        await seed_teoria_niveles(session)
        await seed_configuracion_progreso(session)
        await seed_practica_pool(session)
        await seed_preguntas_desafios(session)
        await update_seed_version(session, "fase_6", SEED_VERSIONS.get("fase_6", "20260614_v1"))
        await session.commit()
    print("Fase 6 inyectada con éxito!")

if __name__ == "__main__":
    asyncio.run(run_fase6_seed())
