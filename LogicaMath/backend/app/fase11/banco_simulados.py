"""
Banco de preguntas de los Simulados (Fase 9 - "Simulados Colegio Pedro II").

Reemplaza el stub anterior (3 preguntas hardcodeadas -- una en portugués e
incontestable -- repetidas al azar 200 veces). Las 20 preguntas están basadas
en el análisis matricial del examen real de admisión al 6º año del Colégio
Militar do Rio de Janeiro (ver `coelgiomilitar.md` en la raíz del repo),
adaptadas al español y a un nivel resoluble con cálculo (opción múltiple).

Cada pregunta lleva su respuesta correcta VERIFICADA, 3 distractores
pedagógicos (varios encarnan las "trampas" descritas en el análisis) y una
explicación breve. El seeder combina correcta + distractores y los baraja de
forma determinista por sección, garantizando 10 preguntas DISTINTAS por
simulacro y variedad entre secciones.
"""

# tema | enunciado | correcta | distractores(3) | explicacion | dificultad(1-3)
BANCO_SIMULADOS = [
    {
        "tema": "Estadística: media aritmética",
        "enunciado": "Un gráfico de barras muestra las temperaturas de 5 días: 18, 20, 22, 19 y 21 °C. ¿Cuál fue la temperatura media?",
        "correcta": "20",
        "distractores": ["19", "21", "22"],
        "explicacion": "Suma los 5 valores (18+20+22+19+21 = 100) y divide entre 5: 100 ÷ 5 = 20 °C.",
        "dificultad": 1,
    },
    {
        "tema": "Sistema métrico decimal",
        "enunciado": "Mariana entrenó corriendo 2 km, después 1500 m y después 30000 cm. ¿Cuántos metros corrió en total?",
        "correcta": "3800",
        "distractores": ["3350", "3500", "33500"],
        "explicacion": "Convierte todo a metros: 2 km = 2000 m, 1500 m = 1500 m, 30000 cm = 300 m. Total: 2000+1500+300 = 3800 m.",
        "dificultad": 2,
    },
    {
        "tema": "Fracciones de una cantidad (dinero)",
        "enunciado": "Tito guardó 360 monedas. 1/3 son de R$1, 1/4 son de R$0,50 y 1/6 son de R$0,25. El resto son de R$0,10. ¿Cuántas monedas de R$0,10 tiene?",
        "correcta": "90",
        "distractores": ["60", "120", "72"],
        "explicacion": "1/3 de 360 = 120; 1/4 = 90; 1/6 = 60. Suman 270. El resto: 360 − 270 = 90 monedas.",
        "dificultad": 2,
    },
    {
        "tema": "Porcentaje del remanente",
        "enunciado": "Ana gastó 3/5 de su dinero en libros y el 20% de lo que le quedó en transporte. Si tenía R$200, ¿cuánto gastó en transporte?",
        "correcta": "R$ 16",
        "distractores": ["R$ 40", "R$ 24", "R$ 80"],
        "explicacion": "En libros gastó 3/5 de 200 = 120, le quedaron 80. El 20% de 80 = 16.",
        "dificultad": 3,
    },
    {
        "tema": "Geometría espacial: cubo pintado",
        "enunciado": "Un cubo de 3×3×3 (27 cubitos) se pinta por fuera y luego se separa en cubitos. ¿Cuántos cubitos tienen exactamente 2 caras pintadas?",
        "correcta": "12",
        "distractores": ["8", "6", "4"],
        "explicacion": "Los cubitos con 2 caras pintadas están en las aristas (sin las esquinas). Un cubo tiene 12 aristas y en cada una hay 1 cubito central: 12.",
        "dificultad": 3,
    },
    {
        "tema": "Números romanos",
        "enunciado": "Un número de cuatro cifras es 2358. ¿Cómo se escribe su mitad en números romanos?",
        "correcta": "MCLXXIX",
        "distractores": ["MCXCIX", "MCLXXVIIII", "MDCLXXIX"],
        "explicacion": "La mitad de 2358 es 1179 = 1000 (M) + 100 (C) + 50 (L) + 20 (XX) + 9 (IX) = MCLXXIX.",
        "dificultad": 3,
    },
    {
        "tema": "Razonamiento espacial: el dado",
        "enunciado": "En un dado común, las caras opuestas suman 7. Si una cara muestra 2 puntos, ¿cuántos puntos tiene la cara opuesta?",
        "correcta": "5",
        "distractores": ["6", "4", "7"],
        "explicacion": "Caras opuestas suman 7, entonces la opuesta al 2 es 7 − 2 = 5.",
        "dificultad": 1,
    },
    {
        "tema": "Números primos",
        "enunciado": "¿Cuántos de estos números son primos: 109, 161, 221, 251, 263?",
        "correcta": "3",
        "distractores": ["2", "4", "5"],
        "explicacion": "Primos: 109, 251 y 263. No lo son: 161 = 7×23 y 221 = 13×17. Son 3 primos.",
        "dificultad": 3,
    },
    {
        "tema": "Poliedros: vértices, caras y aristas",
        "enunciado": "En un prisma triangular, ¿cuánto suman el número de vértices, caras y aristas (V + C + A)?",
        "correcta": "20",
        "distractores": ["18", "21", "24"],
        "explicacion": "Un prisma triangular tiene 6 vértices, 5 caras y 9 aristas: 6 + 5 + 9 = 20.",
        "dificultad": 2,
    },
    {
        "tema": "Logística: número de viajes",
        "enunciado": "Un camión puede transportar 18 cajas por viaje. Si hay que mover 72 cajas, ¿cuántos viajes necesita como mínimo?",
        "correcta": "4",
        "distractores": ["3", "5", "6"],
        "explicacion": "72 ÷ 18 = 4 viajes exactos.",
        "dificultad": 1,
    },
    {
        "tema": "Mínimo común múltiplo (MCM)",
        "enunciado": "Tres faros parpadean cada 6, 7 y 8 segundos. Si parpadean juntos ahora, ¿dentro de cuántos segundos volverán a parpadear los tres a la vez?",
        "correcta": "168",
        "distractores": ["336", "84", "42"],
        "explicacion": "Es el MCM de 6, 7 y 8. Como 6=2·3, 7=7 y 8=2³, el MCM = 2³·3·7 = 168 segundos.",
        "dificultad": 3,
    },
    {
        "tema": "Fracción irreducible",
        "enunciado": "En una reunión hay 600 personas y 220 son niños. ¿Qué fracción irreducible del total son niños?",
        "correcta": "11/30",
        "distractores": ["22/60", "2/5", "11/19"],
        "explicacion": "220/600 se simplifica dividiendo entre 20: 11/30.",
        "dificultad": 2,
    },
    {
        "tema": "Calendario (aritmética modular)",
        "enunciado": "Si hoy es martes, ¿qué día de la semana será dentro de 100 días?",
        "correcta": "Jueves",
        "distractores": ["Miércoles", "Viernes", "Lunes"],
        "explicacion": "100 ÷ 7 deja resto 2. Dos días después del martes es jueves.",
        "dificultad": 2,
    },
    {
        "tema": "Promedio de notas",
        "enunciado": "Las notas de Ana en tres pruebas fueron 7, 8 y 12. ¿Cuál es su promedio?",
        "correcta": "9",
        "distractores": ["8", "10", "27"],
        "explicacion": "(7 + 8 + 12) ÷ 3 = 27 ÷ 3 = 9.",
        "dificultad": 1,
    },
    {
        "tema": "Máximo común divisor (MCD)",
        "enunciado": "Se reparten 728 sillas azules y 819 sillas blancas en aulas, con la misma cantidad por aula y sin mezclar colores. ¿Cuál es el mayor número de sillas por aula posible?",
        "correcta": "91",
        "distractores": ["7", "13", "63"],
        "explicacion": "Es el MCD de 728 y 819. Como 728 = 91×8 y 819 = 91×9, el MCD es 91.",
        "dificultad": 3,
    },
    {
        "tema": "Perímetro de un rectángulo",
        "enunciado": "Un rectángulo mide 8 cm de largo y 5 cm de ancho. ¿Cuál es su perímetro?",
        "correcta": "26",
        "distractores": ["40", "13", "18"],
        "explicacion": "Perímetro = 2 × (largo + ancho) = 2 × (8 + 5) = 2 × 13 = 26 cm.",
        "dificultad": 1,
    },
    {
        "tema": "Área de una figura compuesta",
        "enunciado": "Una figura en forma de L se hace con un rectángulo de 6×4 al que se le quita un cuadrado de 2×2. ¿Cuál es el área de la L?",
        "correcta": "20",
        "distractores": ["24", "16", "28"],
        "explicacion": "Área del rectángulo: 6×4 = 24. Se quita el cuadrado 2×2 = 4. Área de la L: 24 − 4 = 20.",
        "dificultad": 2,
    },
    {
        "tema": "Redondeo por exceso (compra de latas)",
        "enunciado": "Para pintar una pared se necesitan 13 litros de pintura y cada lata trae 5 litros. ¿Cuántas latas hay que comprar?",
        "correcta": "3",
        "distractores": ["2", "4", "13"],
        "explicacion": "13 ÷ 5 = 2 latas y sobran 3 litros por cubrir, así que hay que comprar 3 latas enteras.",
        "dificultad": 2,
    },
    {
        "tema": "Fracciones continuas",
        "enunciado": "¿Cuánto vale la expresión 1 + 1/(2 + 1/2)?",
        "correcta": "7/5",
        "distractores": ["5/7", "3/2", "2/5"],
        "explicacion": "2 + 1/2 = 5/2. Entonces 1/(5/2) = 2/5. Y 1 + 2/5 = 7/5.",
        "dificultad": 3,
    },
    {
        "tema": "Potencias de 10 con decimales",
        "enunciado": "¿Cuánto es 3,5 × 1000?",
        "correcta": "3500",
        "distractores": ["350", "35000", "35"],
        "explicacion": "Multiplicar por 1000 corre la coma 3 lugares a la derecha: 3,5 → 3500.",
        "dificultad": 1,
    },
]
