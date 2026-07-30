# theory_examples.py
# ─────────────────────────────────────────────────────────────
# Base de ejemplos extendidos y formateados premium para Fase 4.
# Proporciona los ejemplos estructurados para cada módulo y nivel de Fase 4 con gráficos SVG y explicaciones amigables.

def obtener_ejemplos_expandidos_fase4(modulo_id: int, nivel_id: int) -> list:
    ejemplos_db = {
        # --- MÓDULO 1: LA FRACCIÓN VISUAL ---
        # Nivel 1: Lectura y modelado de numerador/denominador en polígonos simétricos
        (1, 1): [
            {
                "enunciado": "Una pizza está cortada en <span class=\"keyword-highlight\">8 pedazos iguales</span>. Si te comes <span class=\"keyword-highlight\">3 pedazos</span>, ¿qué fracción representa?<br/>"
                             "<svg width='120' height='120' viewBox='0 0 100 100' style='margin:10px auto; display:block; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3));'>"
                             "  <circle cx='50' cy='50' r='42' fill='#FDE047' stroke='#D97706' stroke-width='3'/>"
                             "  <!-- 3 porciones rojas (comidas / seleccionadas) -->"
                             "  <path d='M50,50 L50,8 A42,42 0 0,1 79.7,20.3 Z' fill='#EF4444' stroke='#D97706' stroke-width='1.5'/>"
                             "  <path d='M50,50 L79.7,20.3 A42,42 0 0,1 92,50 Z' fill='#EF4444' stroke='#D97706' stroke-width='1.5'/>"
                             "  <path d='M50,50 L92,50 A42,42 0 0,1 79.7,79.7 Z' fill='#EF4444' stroke='#D97706' stroke-width='1.5'/>"
                             "  <!-- Líneas divisorias para el resto -->"
                             "  <line x1='50' y1='50' x2='50' y2='92' stroke='#D97706' stroke-width='2'/>"
                             "  <line x1='50' y1='50' x2='8' y2='50' stroke='#D97706' stroke-width='2'/>"
                             "  <line x1='50' y1='50' x2='20.3' y2='20.3' stroke='#D97706' stroke-width='2'/>"
                             "  <line x1='50' y1='50' x2='20.3' y2='79.7' stroke='#D97706' stroke-width='2'/>"
                             "</svg>",
                "pasos": [
                    {"orden": 1, "texto": "Contamos las porciones totales de la pizza (abajo): <span class=\"keyword-highlight\">8</span>."},
                    {"orden": 2, "texto": "Contamos las porciones pintadas de color rojo (arriba): <span class=\"keyword-highlight\">3</span>."},
                    {"orden": 3, "texto": "Escribimos la fracción mágica: <span class=\"keyword-highlight\">3/8</span> (¡tres octavos!)."}
                ]
            },
            {
                "enunciado": "Una barra de chocolate tiene <span class=\"keyword-highlight\">4 cuadrados idénticos</span>. Te comes <span class=\"keyword-highlight\">1 cuadrado</span>. ¿Qué fracción queda?",
                "pasos": [
                    {"orden": 1, "texto": "El chocolate entero se dividió en <span class=\"keyword-highlight\">4</span> partes iguales. El total va abajo: 4."},
                    {"orden": 2, "texto": "Si comes 1, te quedan: <span class=\"keyword-highlight\">4 - 1 = 3</span> cuadrados deliciosos (Numerador = 3)."},
                    {"orden": 3, "texto": "La fracción restante es: <span class=\"keyword-highlight\">3/4</span>."}
                ]
            },
            {
                "enunciado": "Una bandera está dividida en <span class=\"keyword-highlight\">3 franjas verticales iguales</span>. Hay <span class=\"keyword-highlight\">2 franjas de color rojo</span>. ¿Qué fracción es roja?",
                "pasos": [
                    {"orden": 1, "texto": "El total de franjas es <span class=\"keyword-highlight\">3</span>. Va en el denominador (abajo)."},
                    {"orden": 2, "texto": "Las rojas son <span class=\"keyword-highlight\">2</span>. Va en el numerador (arriba)."},
                    {"orden": 3, "texto": "La fracción resultante es: <span class=\"keyword-highlight\">2/3</span>."}
                ]
            },
            {
                "enunciado": "Una ventana tiene <span class=\"keyword-highlight\">6 cristales iguales</span>. Si <span class=\"keyword-highlight\">5 cristales</span> están limpios, ¿qué fracción representa?",
                "pasos": [
                    {"orden": 1, "texto": "Total de divisiones = <span class=\"keyword-highlight\">6</span> (Denominador)."},
                    {"orden": 2, "texto": "Porción de cristales limpios = <span class=\"keyword-highlight\">5</span> (Numerador)."},
                    {"orden": 3, "texto": "La fracción es: <span class=\"keyword-highlight\">5/6</span> de la ventana limpia."}
                ]
            }
        ],
        # Nivel 2: Construcción de equivalencias
        (1, 2): [
            {
                "enunciado": "Si dividimos una figura en <span class=\"keyword-highlight\">4 veces más partes iguales</span>, necesitaremos colorear <span class=\"keyword-highlight\">4 veces más partes</span> para representar la misma porción del total.<br/>"
                             "<div style='display:flex; justify-content:center; align-items:center; gap:30px; margin:15px auto;'>"
                             "  <div style='text-align:center;'>"
                             "    <svg width='120' height='120' viewBox='0 0 120 120' style='border:2px solid #FFFFFF; background:#1F2937; border-radius:8px;'>"
                             "      <rect x='0' y='0' width='40' height='120' fill='#374151'/>"
                             "      <rect x='40' y='0' width='40' height='120' fill='#8B5CF6'/>"
                             "      <rect x='80' y='0' width='40' height='120' fill='#374151'/>"
                             "      <line x1='40' y1='0' x2='40' y2='120' stroke='#FFFFFF' stroke-width='2'/>"
                             "      <line x1='80' y1='0' x2='80' y2='120' stroke='#FFFFFF' stroke-width='2'/>"
                             "    </svg>"
                             "    <div style='font-size:0.9rem; color:#8B5CF6; font-weight:bold; margin-top:6px;'>1/3</div>"
                             "  </div>"
                             "  <div style='font-size:2rem; color:#FFFFFF; font-weight:bold;'>=</div>"
                             "  <div style='text-align:center;'>"
                             "    <svg width='120' height='120' viewBox='0 0 120 120' style='border:2px solid #FFFFFF; background:#1F2937; border-radius:8px;'>"
                             "      <polygon points='0,0 40,0 0,60' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='0,60 40,0 40,60' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='0,60 40,60 0,120' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='0,120 40,60 40,120' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='40,0 80,0 40,60' fill='#8B5CF6' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='40,60 80,0 80,60' fill='#8B5CF6' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='40,60 80,60 40,120' fill='#8B5CF6' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='40,120 80,60 80,120' fill='#8B5CF6' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='80,0 120,0 80,60' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='80,60 120,0 120,60' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='80,60 120,60 80,120' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <polygon points='80,120 120,60 120,120' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <line x1='40' y1='0' x2='40' y2='120' stroke='#FFFFFF' stroke-width='2.5'/>"
                             "      <line x1='80' y1='0' x2='80' y2='120' stroke='#FFFFFF' stroke-width='2.5'/>"
                             "      <line x1='0' y1='60' x2='120' y2='60' stroke='#FFFFFF' stroke-width='2.5'/>"
                             "    </svg>"
                             "    <div style='font-size:0.9rem; color:#8B5CF6; font-weight:bold; margin-top:6px;'>4/12</div>"
                             "  </div>"
                             "</div>"
                             "<div style='display:flex; justify-content:center; align-items:center; gap:8px; font-size:1.2rem; color:#FFFFFF; margin-bottom:10px;'>"
                             "  <div style='text-align:center;'>"
                             "    <div style='border-bottom:2px solid #fff; padding: 0 4px;'>1 × 4</div>"
                             "    <div>3 × 4</div>"
                             "  </div>"
                             "  <div style='font-weight:bold;'>=</div>"
                             "  <div style='text-align:center; color:#A855F7;'>"
                             "    <div style='border-bottom:2px solid #A855F7; padding: 0 4px; font-weight:bold;'>4</div>"
                             "    <div style='font-weight:bold;'>12</div>"
                             "  </div>"
                             "</div>",
                "pasos": [
                    {"orden": 1, "texto": "Contamos las partes originales: la figura de la izquierda está dividida en 3 columnas iguales y 1 está coloreada (1/3)."},
                    {"orden": 2, "texto": "Subdividimos la figura: al cortar cada columna por la mitad y trazar diagonales, obtenemos 4 veces más partes: 3 × 4 = 12."},
                    {"orden": 3, "texto": "Para mantener el mismo área pintada, la parte morada ahora tiene 4 trozos pequeños (1 × 4 = 4). Así, 1/3 equivale a 4/12."}
                ]
            },
            {
                "enunciado": "Escribe una fracción diferente que sea igual a <span class=\"keyword-highlight\">1/2</span> dividiendo un cuadrado en <span class=\"keyword-highlight\">16 partes iguales</span> con un patrón de diamantes y coloreando <span class=\"keyword-highlight\">8 de ellas</span>.<br/>"
                             "<div style='display:flex; flex-direction:column; align-items:center; gap:10px; margin:15px auto;'>"
                             "  <svg width='120' height='120' viewBox='0 0 120 120' style='border:2px solid #FFFFFF; background:#1F2937; border-radius:8px;'>"
                             "    <polygon points='60,0 0,30 60,30' fill='#0D9488'/>"
                             "    <polygon points='60,60 0,30 60,30' fill='#0D9488'/>"
                             "    <polygon points='60,0 120,30 60,30' fill='#0D9488'/>"
                             "    <polygon points='60,60 120,30 60,30' fill='#0D9488'/>"
                             "    <polygon points='60,60 0,90 60,90' fill='#0D9488'/>"
                             "    <polygon points='60,120 0,90 60,90' fill='#0D9488'/>"
                             "    <polygon points='60,60 120,90 60,90' fill='#0D9488'/>"
                             "    <polygon points='60,120 120,90 60,90' fill='#0D9488'/>"
                             "    <polygon points='0,0 60,0 0,30' fill='#374151'/>"
                             "    <polygon points='0,60 60,60 0,30' fill='#374151'/>"
                             "    <polygon points='120,0 60,0 120,30' fill='#374151'/>"
                             "    <polygon points='120,60 60,60 120,30' fill='#374151'/>"
                             "    <polygon points='0,60 60,60 0,90' fill='#374151'/>"
                             "    <polygon points='0,120 60,120 0,90' fill='#374151'/>"
                             "    <polygon points='120,60 60,60 120,90' fill='#374151'/>"
                             "    <polygon points='120,120 60,120 120,90' fill='#374151'/>"
                             "    <line x1='0' y1='30' x2='60' y2='0' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='0' y1='30' x2='60' y2='60' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='120' y1='30' x2='60' y2='0' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='120' y1='30' x2='60' y2='60' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='0' y1='90' x2='60' y2='60' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='0' y1='90' x2='60' y2='120' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='120' y1='90' x2='60' y2='60' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='120' y1='90' x2='60' y2='120' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='60' y1='0' x2='60' y2='120' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='0' y1='60' x2='120' y2='60' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='0' y1='30' x2='120' y2='30' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <line x1='0' y1='90' x2='120' y2='90' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "  </svg>"
                             "  <div style='display:flex; justify-content:center; align-items:center; gap:8px; font-size:1.2rem; color:#FFFFFF;'>"
                             "    <div style='text-align:center;'>"
                             "      <div style='border-bottom:2px solid #fff; padding: 0 4px;'>1</div>"
                             "      <div>2</div>"
                             "    </div>"
                             "    <div style='font-weight:bold;'>=</div>"
                             "    <div style='text-align:center; color:#0D9488;'>"
                             "      <div style='border-bottom:2px solid #0D9488; padding: 0 4px; font-weight:bold;'>8</div>"
                             "      <div style='font-weight:bold;'>16</div>"
                             "    </div>"
                             "  </div>"
                             "</div>",
                "pasos": [
                    {"orden": 1, "texto": "Dividimos el cuadrado grande: usando líneas horizontales, verticales y diagonales de diamantes, lo cortamos en exactamente 16 triángulos iguales."},
                    {"orden": 2, "texto": "Contamos la parte coloreada de turquesa: los dos rombos centrales están formados por 8 triángulos turquesas."},
                    {"orden": 3, "texto": "Obtenemos la equivalencia: 8 partes de 16 cubren exactamente la mitad del área del cuadrado, por lo que: 1/2 = 8/16."}
                ]
            },
            {
                "enunciado": "Al multiplicar el numerador y el denominador de una fracción por el <span class=\"keyword-highlight\">mismo factor</span>, creamos una fracción equivalente idéntica en proporción.<br/>"
                             "<div style='display:flex; justify-content:center; align-items:center; gap:30px; margin:15px auto;'>"
                             "  <div style='text-align:center;'>"
                             "    <svg width='120' height='120' viewBox='0 0 120 120' style='border:2px solid #FFFFFF; background:#1F2937; border-radius:8px;'>"
                             "      <rect x='0' y='0' width='120' height='120' fill='#374151'/>"
                             "      <rect x='0' y='0' width='60' height='30' fill='#0D9488'/>"
                             "      <rect x='60' y='0' width='60' height='30' fill='#0D9488'/>"
                             "      <rect x='0' y='30' width='60' height='30' fill='#0D9488'/>"
                             "      <line x1='60' y1='0' x2='60' y2='120' stroke='#FFFFFF' stroke-width='2'/>"
                             "      <line x1='0' y1='30' x2='120' y2='30' stroke='#FFFFFF' stroke-width='2'/>"
                             "      <line x1='0' y1='60' x2='120' y2='60' stroke='#FFFFFF' stroke-width='2'/>"
                             "      <line x1='0' y1='90' x2='120' y2='90' stroke='#FFFFFF' stroke-width='2'/>"
                             "    </svg>"
                             "    <div style='font-size:0.9rem; color:#0D9488; font-weight:bold; margin-top:6px;'>3/8</div>"
                             "  </div>"
                             "  <div style='font-size:2rem; color:#FFFFFF; font-weight:bold;'>=</div>"
                             "  <div style='text-align:center;'>"
                             "    <svg width='120' height='120' viewBox='0 0 120 120' style='border:2px solid #FFFFFF; background:#1F2937; border-radius:8px;'>"
                             "      <rect x='0' y='0' width='120' height='120' fill='#374151'/>"
                             "      <rect x='0' y='0' width='60' height='30' fill='#0D9488'/>"
                             "      <rect x='60' y='0' width='60' height='30' fill='#0D9488'/>"
                             "      <rect x='0' y='30' width='60' height='30' fill='#0D9488'/>"
                             "      <line x1='0' y1='30' x2='60' y2='0' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <line x1='120' y1='30' x2='60' y2='0' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <line x1='0' y1='30' x2='60' y2='60' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <line x1='120' y1='30' x2='60' y2='60' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <line x1='0' y1='90' x2='60' y2='60' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <line x1='120' y1='90' x2='60' y2='60' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <line x1='0' y1='90' x2='60' y2='120' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <line x1='120' y1='90' x2='60' y2='120' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "      <line x1='60' y1='0' x2='60' y2='120' stroke='#FFFFFF' stroke-width='2.5'/>"
                             "      <line x1='0' y1='30' x2='120' y2='30' stroke='#FFFFFF' stroke-width='2.5'/>"
                             "      <line x1='0' y1='60' x2='120' y2='60' stroke='#FFFFFF' stroke-width='2.5'/>"
                             "      <line x1='0' y1='90' x2='120' y2='90' stroke='#FFFFFF' stroke-width='2.5'/>"
                             "    </svg>"
                             "    <div style='font-size:0.9rem; color:#0D9488; font-weight:bold; margin-top:6px;'>6/16</div>"
                             "  </div>"
                             "</div>"
                             "<div style='display:flex; justify-content:center; align-items:center; gap:8px; font-size:1.2rem; color:#FFFFFF; margin-bottom:10px;'>"
                             "  <div style='text-align:center;'>"
                             "    <div style='border-bottom:2px solid #fff; padding: 0 4px;'>3 × 2</div>"
                             "    <div>8 × 2</div>"
                             "  </div>"
                             "  <div style='font-weight:bold;'>=</div>"
                             "  <div style='text-align:center; color:#0D9488;'>"
                             "    <div style='border-bottom:2px solid #0D9488; padding: 0 4px; font-weight:bold;'>6</div>"
                             "    <div style='font-weight:bold;'>16</div>"
                             "  </div>"
                             "</div>",
                "pasos": [
                    {"orden": 1, "texto": "Fracción original: la cuadrícula izquierda tiene 8 rectángulos y 3 están coloreados (3/8)."},
                    {"orden": 2, "texto": "Si dividimos cada rectángulo diagonalmente en 2 partes iguales, duplicamos el total de piezas: 8 × 2 = 16."},
                    {"orden": 3, "texto": "Los 3 rectángulos turquesas ahora representan 6 triángulos coloreados: 3 × 2 = 6. Obtenemos la fracción equivalente clonada: 6/16."}
                ]
            },
            {
                "enunciado": "Encuentra una fracción equivalente a <span class=\"keyword-highlight\">1/2</span> pintando exactamente la mitad de un hexágono dividido en <span class=\"keyword-highlight\">12 triángulos iguales</span> formando una estrella o molinillo.<br/>"
                             "<div style='display:flex; flex-direction:column; align-items:center; gap:10px; margin:15px auto;'>"
                             "  <svg width='120' height='120' viewBox='0 0 120 120' style='filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3));'>"
                             "    <polygon points='60,10 103.3,35 103.3,85 60,110 16.7,85 16.7,35' fill='#374151' stroke='#FFFFFF' stroke-width='2.5'/>"
                             "    <polygon points='60,60 60,10 43.35,22.5' fill='#F59E0B' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 16.7,35 16.7,60' fill='#F59E0B' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 16.7,85 43.35,97.5' fill='#F59E0B' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 60,110 81.65,97.5' fill='#F59E0B' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 103.3,85 103.3,60' fill='#F59E0B' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 103.3,35 81.65,22.5' fill='#F59E0B' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 43.35,22.5 16.7,35' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 16.7,60 16.7,85' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 43.35,97.5 60,110' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 81.65,97.5 103.3,85' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 103.3,60 103.3,35' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "    <polygon points='60,60 81.65,22.5 60,10' fill='#374151' stroke='#FFFFFF' stroke-width='1.5'/>"
                             "  </svg>"
                             "  <div style='display:flex; justify-content:center; align-items:center; gap:8px; font-size:1.2rem; color:#FFFFFF;'>"
                             "    <div style='text-align:center;'>"
                             "      <div style='border-bottom:2px solid #fff; padding: 0 4px;'>1</div>"
                             "      <div>2</div>"
                             "    </div>"
                             "    <div style='font-weight:bold;'>=</div>"
                             "    <div style='text-align:center; color:#F59E0B;'>"
                             "      <div style='border-bottom:2px solid #F59E0B; padding: 0 4px; font-weight:bold;'>6</div>"
                             "      <div style='font-weight:bold;'>12</div>"
                             "    </div>"
                             "  </div>"
                             "</div>",
                "pasos": [
                    {"orden": 1, "texto": "Estudiamos el hexágono: está dividido en exactamente 12 triángulos del mismo tamaño."},
                    {"orden": 2, "texto": "Contamos las partes del molinillo: hay 6 aspas amarillas, lo que representa la mitad exacta de las 12 porciones totales."},
                    {"orden": 3, "texto": "Hallamos la equivalencia: al simplificar 6/12 o amplificar 1/2 por 6, comprobamos que 1/2 es equivalente a 6/12."}
                ]
            }
        ],
        # Nivel 3: Áreas fraccionarias en composiciones geométricas asimétricas
        (1, 3): [
            {
                "enunciado": "Un cuadrado se dividió en <span class=\"keyword-highlight\">4 partes</span>, pero 2 son el doble de grandes que las otras. ¿Cada parte representa 1/4?<br/>"
                             "<svg width='100' height='100' viewBox='0 0 100 100' style='margin:10px auto; display:block; border:2px solid #4B5563; background:#1F2937;'>"
                             "  <!-- 2 partes grandes (33.3% y 33.3%) y 2 pequeñas (16.6% cada una) -->"
                             "  <rect x='0' y='0' width='33.3' height='100' fill='none' stroke='#9CA3AF' stroke-width='2'/>"
                             "  <rect x='33.3' y='0' width='33.3' height='100' fill='none' stroke='#9CA3AF' stroke-width='2'/>"
                             "  <rect x='66.6' y='0' width='16.6' height='100' fill='none' stroke='#9CA3AF' stroke-width='2'/>"
                             "  <rect x='83.2' y='0' width='16.8' height='100' fill='none' stroke='#9CA3AF' stroke-width='2'/>"
                             "  <text x='50' y='55' fill='#EF4444' font-size='14' font-weight='bold' text-anchor='middle'>¿Son iguales?</text>"
                             "</svg>",
                "pasos": [
                    {"orden": 1, "texto": "Recuerda la regla de oro: para representar fracciones directamente, todas las partes deben tener <span class=\"keyword-highlight\">exactamente la misma área</span>."},
                    {"orden": 2, "texto": "Al mirar el dibujo, vemos que los bloques son desiguales (unos son anchos y otros delgados)."},
                    {"orden": 3, "texto": "Por lo tanto, la respuesta correcta es: <span class=\"keyword-highlight\">No, porque las partes no son iguales</span>."}
                ]
            },
            {
                "enunciado": "Un rectángulo está cortado por su diagonal en <span class=\"keyword-highlight\">2 triángulos iguales</span>. ¿Qué fracción representa cada uno?",
                "pasos": [
                    {"orden": 1, "texto": "La diagonal divide la figura en <span class=\"keyword-highlight\">2 porciones simétricas</span> del mismo tamaño."},
                    {"orden": 2, "texto": "Cada triángulo es una de esas partes de un total de dos."},
                    {"orden": 3, "texto": "La respuesta es: <span class=\"keyword-highlight\">1/2</span> del rectángulo."}
                ]
            },
            {
                "enunciado": "Un círculo tiene una línea que corta una pequeña porción del borde. ¿Es esa porción la mitad (1/2)?",
                "pasos": [
                    {"orden": 1, "texto": "Para que represente la mitad exacta, la línea de corte debe pasar por el mero centro (diámetro)."},
                    {"orden": 2, "texto": "Al estar la línea en una orilla, una parte es diminuta y otra gigante."},
                    {"orden": 3, "texto": "Respuesta: <span class=\"keyword-highlight\">No, porque las partes no son iguales</span>."}
                ]
            },
            {
                "enunciado": "Una figura especial está dividida en <span class=\"keyword-highlight\">7 porciones de tamaños DISTINTOS</span> que en total suman <span class=\"keyword-highlight\">12 doceavos (12/12)</span>. ¿Cómo puedes saber qué fracción representa cada porción?<br/>"
                             "<svg width='130' height='100' viewBox='0 0 90 90' style='margin:10px auto; display:block; filter: drop-shadow(0px 4px 8px rgba(99,102,241,0.5));'>"
                             "  <!-- Col izquierda grande: 4/12 -->"
                             "  <polygon points='0,0 30,0 30,90 0,90' fill='#4F46E5' opacity='0.85' stroke='#312E81' stroke-width='1.5'/>"
                             "  <text x='15' y='48' fill='white' font-size='7' font-weight='bold' text-anchor='middle'>4/12</text>"
                             "  <!-- Col central superior: 2/12 -->"
                             "  <polygon points='30,0 60,0 60,45 30,45' fill='#7C3AED' opacity='0.8' stroke='#312E81' stroke-width='1.5'/>"
                             "  <text x='45' y='26' fill='white' font-size='7' font-weight='bold' text-anchor='middle'>2/12</text>"
                             "  <!-- Col central inferior: 2/12 -->"
                             "  <polygon points='30,45 60,45 60,90 30,90' fill='#7C3AED' opacity='0.6' stroke='#312E81' stroke-width='1.5'/>"
                             "  <text x='45' y='70' fill='white' font-size='7' font-weight='bold' text-anchor='middle'>2/12</text>"
                             "  <!-- Triángulo sup-der: 1/12 -->"
                             "  <polygon points='60,0 90,0 90,45' fill='#EC4899' opacity='0.75' stroke='#312E81' stroke-width='1.5'/>"
                             "  <text x='76' y='18' fill='white' font-size='6' font-weight='bold' text-anchor='middle'>1/12</text>"
                             "  <!-- Triángulo cen-der sup: 1/12 -->"
                             "  <polygon points='60,0 90,45 60,45' fill='#F43F5E' opacity='0.7' stroke='#312E81' stroke-width='1.5'/>"
                             "  <text x='71' y='36' fill='white' font-size='6' font-weight='bold' text-anchor='middle'>1/12</text>"
                             "  <!-- Triángulo cen-der inf: 1/12 -->"
                             "  <polygon points='60,45 90,45 60,90' fill='#F97316' opacity='0.7' stroke='#312E81' stroke-width='1.5'/>"
                             "  <text x='71' y='62' fill='white' font-size='6' font-weight='bold' text-anchor='middle'>1/12</text>"
                             "  <!-- Triángulo inf-der: 1/12 -->"
                             "  <polygon points='90,45 90,90 60,90' fill='#EAB308' opacity='0.7' stroke='#312E81' stroke-width='1.5'/>"
                             "  <text x='76' y='78' fill='white' font-size='6' font-weight='bold' text-anchor='middle'>1/12</text>"
                             "</svg>",
                "pasos": [
                    {"orden": 1, "texto": "La figura está dividida en 7 porciones de <span class=\"keyword-highlight\">tamaños diferentes</span>, pero juntas suman exactamente 1 figura entera (12/12)."},
                    {"orden": 2, "texto": "La columna izquierda grande vale <span class=\"keyword-highlight\">4/12</span>. Las dos del centro valen <span class=\"keyword-highlight\">2/12 cada una</span>. Y los 4 triángulos de la derecha valen <span class=\"keyword-highlight\">1/12 cada uno</span>."},
                    {"orden": 3, "texto": "Verificamos: 4 + 2 + 2 + 1 + 1 + 1 + 1 = <span class=\"keyword-highlight\">12/12 ✓</span>. ¡Las áreas distintas no hacen fracciones iguales!"}
                ]
            }
            ,
            {
                "enunciado": "Las fracciones se construyen a partir de partes que son iguales en tamaño.<br/>"
                             "Esta figura no tiene pintada exactamente la tercera parte (1/3). Está dividida en 3 partes, pero no en 3 partes iguales.<br/>"
                             "<div style='display:flex; justify-content:center; gap:20px; margin:10px auto;'>"
                             "  <svg width='110' height='110' viewBox='0 0 100 100' style='filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3));'>"
                             "    <rect x='2' y='2' width='96' height='96' fill='#345' stroke='#fff' stroke-width='2'/>"
                             "    <polygon points='2,98 50,50 98,98' fill='#10B981'/>"
                             "    <line x1='50' y1='2' x2='50' y2='50' stroke='#fff' stroke-width='2'/>"
                             "    <line x1='50' y1='50' x2='2' y2='98' stroke='#fff' stroke-width='2'/>"
                             "    <line x1='50' y1='50' x2='98' y2='98' stroke='#fff' stroke-width='2'/>"
                             "  </svg>"
                             "  <svg width='110' height='110' viewBox='0 0 100 100' style='filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3));'>"
                             "    <rect x='2' y='2' width='96' height='96' fill='#345' stroke='#fff' stroke-width='2'/>"
                             "    <polygon points='2,98 50,50 98,98' fill='#10B981'/>"
                             "    <line x1='50' y1='2' x2='50' y2='98' stroke='#fff' stroke-width='2'/>"
                             "    <line x1='2' y1='50' x2='98' y2='50' stroke='#fff' stroke-width='2'/>"
                             "    <line x1='2' y1='2' x2='98' y2='98' stroke='#fff' stroke-width='2'/>"
                             "    <line x1='98' y1='2' x2='2' y2='98' stroke='#fff' stroke-width='2'/>"
                             "  </svg>"
                             "</div>"
                             "¿Ves cómo funciona?",
                "pasos": [
                    {"orden": 1, "texto": "En la primera figura, las 3 partes tienen <span class=\"keyword-highlight\">formas y tamaños diferentes</span>. Por eso no representa 1/3."},
                    {"orden": 2, "texto": "En la segunda figura, al subdividirla en <span class=\"keyword-highlight\">8 partes iguales</span>, la misma región representa exactamente 2/8 (o 1/4)."},
                    {"orden": 3, "texto": "¡Para que sea una fracción directa, las partes divisorias deben ser idénticas!"}
                ]
            },
            {
                "enunciado": "En resumen, esta es la idea clave:<br/>"
                             "Identificamos las fracciones de una figura buscando partes iguales.<br/>"
                             "<svg width='120' height='120' viewBox='0 0 100 100' style='margin:10px auto; display:block; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3));'>"
                             "  <rect x='2' y='2' width='96' height='96' fill='#345' stroke='#fff' stroke-width='2'/>"
                             "  <polygon points='50,2 75,2 50,25' fill='#8B5CF6'/>"
                             "  <polygon points='2,25 25,25 2,50' fill='#8B5CF6'/>"
                             "  <polygon points='98,50 98,75 75,75' fill='#8B5CF6'/>"
                             "  <polygon points='25,98 50,98 25,75' fill='#8B5CF6'/>"
                             "  <line x1='25' y1='2' x2='25' y2='98' stroke='#fff' stroke-width='1.5'/>"
                             "  <line x1='50' y1='2' x2='50' y2='98' stroke='#fff' stroke-width='1.5'/>"
                             "  <line x1='75' y1='2' x2='75' y2='98' stroke='#fff' stroke-width='1.5'/>"
                             "  <line x1='2' y1='25' x2='98' y2='25' stroke='#fff' stroke-width='1.5'/>"
                             "  <line x1='2' y1='50' x2='98' y2='50' stroke='#fff' stroke-width='1.5'/>"
                             "  <line x1='2' y1='75' x2='98' y2='75' stroke='#fff' stroke-width='1.5'/>"
                             "  <path d='M2,2L25,25M50,2L25,25M50,2L75,25M98,2L75,25M25,25L2,50M25,25L50,50M75,25L50,50M75,25L98,50M2,50L25,75M50,50L25,75M50,50L75,75M98,50L75,75M25,75L2,98M25,75L50,98M75,75L50,98M75,75L98,98' stroke='#fff' stroke-width='1.5' fill='none'/>"
                             "</svg>"
                             "Las partes de igual tamaño son los bloques de construcción de las fracciones.",
                "pasos": [
                    {"orden": 1, "texto": "Esta cuadrícula está dividida en <span class=\"keyword-highlight\">32 pequeños triángulos del mismo tamaño</span>."},
                    {"orden": 2, "texto": "Como hay <span class=\"keyword-highlight\">4 partes coloreadas</span> de morado, representan la fracción 4/32."},
                    {"orden": 3, "texto": "Simplificando: 4 ÷ 4 = 1, y 32 ÷ 4 = 8. ¡Esto representa exactamente <span class=\"keyword-highlight\">1/8</span> de la figura!"}
                ]
            }
        ],



        # --- MÓDULO 2: FRACCIÓN DE CANTIDAD ---
        # Nivel 1: Cálculo de porciones unitarias (1/n) sobre grupos
        (2, 1): [
            {
                "enunciado": "Calcula <span class=\"keyword-highlight\">1/3 de 15 caramelos</span>.",
                "pasos": [
                    {"orden": 1, "texto": "El denominador 3 nos ordena repartir los 15 caramelos en <span class=\"keyword-highlight\">3 cajas iguales</span>."},
                    {"orden": 2, "texto": "Dividimos el total: <span class=\"keyword-highlight\">15 ÷ 3 = 5</span> caramelos por caja."},
                    {"orden": 3, "texto": "Como buscamos 1/3, tomamos 1 sola caja. El resultado es: <span class=\"keyword-highlight\">5 caramelos</span>."}
                ]
            },
            {
                "enunciado": "Calcula <span class=\"keyword-highlight\">1/4 de 20 monedas</span>.",
                "pasos": [
                    {"orden": 1, "texto": "Dividimos las monedas en 4 grupos iguales: <span class=\"keyword-highlight\">20 ÷ 4 = 5</span>."},
                    {"orden": 2, "texto": "Como la fracción pide 1 de esas pilas, multiplicamos: 5 × 1 = 5."},
                    {"orden": 3, "texto": "Resultado final: <span class=\"keyword-highlight\">5 monedas</span>."}
                ]
            },
            {
                "enunciado": "Calcula <span class=\"keyword-highlight\">1/5 de 50 soldados</span>.",
                "pasos": [
                    {"orden": 1, "texto": "Dividimos los 50 soldados en 5 batallones idénticos: <span class=\"keyword-highlight\">50 ÷ 5 = 10</span>."},
                    {"orden": 2, "texto": "Tomamos un batallón: 10 soldados."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">10 soldados</span>."}
                ]
            },
            {
                "enunciado": "Calcula <span class=\"keyword-highlight\">1/8 de 32 cartas</span>.",
                "pasos": [
                    {"orden": 1, "texto": "Repartimos las 32 cartas en 8 montones iguales: <span class=\"keyword-highlight\">32 ÷ 8 = 4</span> cartas por montón."},
                    {"orden": 2, "texto": "Tomamos solo 1 montón: 4 cartas."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">4 cartas</span>."}
                ]
            }
        ],
        # Nivel 2: Operador compuesto (m/n de X) y algoritmo de dos pasos
        (2, 2): [
            {
                "enunciado": "Calcula <span class=\"keyword-highlight\">3/4 de 20 manzanas</span>.",
                "pasos": [
                    {"orden": 1, "texto": "<b>Paso 1 (Dividir):</b> Dividimos el total entre el de abajo: <span class=\"keyword-highlight\">20 ÷ 4 = 5</span> manzanas por caja."},
                    {"orden": 2, "texto": "<b>Paso 2 (Multiplicar):</b> Juntamos las cajas del numerador (arriba): <span class=\"keyword-highlight\">5 × 3 = 15</span> manzanas."},
                    {"orden": 3, "texto": "Resultado del motor de dos pasos: <span class=\"keyword-highlight\">15 manzanas</span>."}
                ]
            },
            {
                "enunciado": "Calcula <span class=\"keyword-highlight\">2/5 de 50 monedas</span>.",
                "pasos": [
                    {"orden": 1, "texto": "Paso 1: Repartimos 50 monedas en 5 montones iguales: <span class=\"keyword-highlight\">50 ÷ 5 = 10</span>."},
                    {"orden": 2, "texto": "Paso 2: Tomamos los 2 montones que nos pide el numerador: <span class=\"keyword-highlight\">10 × 2 = 20</span>."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">20 monedas</span>."}
                ]
            },
            {
                "enunciado": "En una clase de 30 alumnos, <span class=\"keyword-highlight\">2/3</span> llevan gafas. ¿Cuántos alumnos son?",
                "pasos": [
                    {"orden": 1, "texto": "Paso 1: Dividimos la clase en 3 grupos iguales: <span class=\"keyword-highlight\">30 ÷ 3 = 10</span>."},
                    {"orden": 2, "texto": "Paso 2: Tomamos 2 de esos grupos: <span class=\"keyword-highlight\">10 × 2 = 20</span>."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">20 alumnos con gafas</span>."}
                ]
            },
            {
                "enunciado": "Calcula <span class=\"keyword-highlight\">5/8 de 40 cartas</span>.",
                "pasos": [
                    {"orden": 1, "texto": "Paso 1: Dividimos 40 entre el denominador 8: <span class=\"keyword-highlight\">40 ÷ 8 = 5</span>."},
                    {"orden": 2, "texto": "Paso 2: Multiplicamos por el numerador 5: <span class=\"keyword-highlight\">5 × 5 = 25</span>."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">25 cartas</span>."}
                ]
            }
        ],
        # Nivel 3: Lógica del complemento y deducción del resto
        (2, 3): [
            {
                "enunciado": "Si regalas <span class=\"keyword-highlight\">1/4 de tus juguetes</span>, ¿qué fracción de tus juguetes te queda?<br/>"
                             "<svg width='160' height='40' viewBox='0 0 160 40' style='margin:10px auto; display:block; border:1px solid #4B5563; background:#1F2937;'>"
                             "  <rect x='0' y='0' width='40' height='40' fill='#EF4444' opacity='0.4'/>"
                             "  <text x='20' y='25' fill='#EF4444' font-size='10' text-anchor='middle'>Regalado</text>"
                             "  <rect x='40' y='0' width='120' height='40' fill='#10B981' opacity='0.3'/>"
                             "  <text x='100' y='25' fill='#10B981' font-size='10' text-anchor='middle'>Te queda (3/4)</text>"
                             "  <line x1='40' y1='0' x2='40' y2='40' stroke='#9CA3AF' stroke-width='2'/>"
                             "  <line x1='80' y1='0' x2='80' y2='40' stroke='#9CA3AF' stroke-width='1.5'/>"
                             "  <line x1='120' y1='0' x2='120' y2='40' stroke='#9CA3AF' stroke-width='1.5'/>"
                             "</svg>",
                "pasos": [
                    {"orden": 1, "texto": "Tu colección de juguetes total representa la unidad entera: <span class=\"keyword-highlight\">4/4</span>."},
                    {"orden": 2, "texto": "Le restamos la fracción que regalaste: <span class=\"keyword-highlight\">4/4 - 1/4 = 3/4</span>."},
                    {"orden": 3, "texto": "Respuesta: Te quedan <span class=\"keyword-highlight\">3/4</span> de tus juguetes."}
                ]
            },
            {
                "enunciado": "Sofía preparó <span class=\"keyword-highlight\">40 cupcakes</span> y vendió <span class=\"keyword-highlight\">1/4</span> en la feria. ¿Cuántos le quedaron?",
                "pasos": [
                    {"orden": 1, "texto": "Calculamos la parte vendida: <span class=\"keyword-highlight\">1/4 de 40 = 10</span> cupcakes."},
                    {"orden": 2, "texto": "Restamos la porción vendida del total inicial: <span class=\"keyword-highlight\">40 - 10 = 30</span> cupcakes."},
                    {"orden": 3, "texto": "Resultado: Le quedaron <span class=\"keyword-highlight\">30 cupcakes</span>."}
                ]
            },
            {
                "enunciado": "Un tanque de agua de 50 litros se derrama en <span class=\"keyword-highlight\">2/5</span> de su volumen. ¿Cuántos litros quedan?",
                "pasos": [
                    {"orden": 1, "texto": "Calculamos la fracción derramada: <span class=\"keyword-highlight\">2/5 de 50 = 20 litros</span>."},
                    {"orden": 2, "texto": "Restamos del tanque lleno: <span class=\"keyword-highlight\">50 - 20 = 30 litros</span>."},
                    {"orden": 3, "texto": "Quedan en el tanque: <span class=\"keyword-highlight\">30 litros</span>."}
                ]
            },
            {
                "enunciado": "Si gastas <span class=\"keyword-highlight\">3/8 de tus ahorros</span>, ¿qué fracción sigue guardada en el banco?",
                "pasos": [
                    {"orden": 1, "texto": "Tus ahorros completos iniciales se representan como <span class=\"keyword-highlight\">8/8</span>."},
                    {"orden": 2, "texto": "Le restamos los octavos que gastaste: <span class=\"keyword-highlight\">8/8 - 3/8 = 5/8</span>."},
                    {"orden": 3, "texto": "La fracción guardada es: <span class=\"keyword-highlight\">5/8</span>."}
                ]
            }
        ],

        # --- MÓDULO 3: PORCENTAJES RÁPIDOS Y PROMEDIOS ---
        # Nivel 1: Mapeo de porcentajes intuitivos: 50%, 25%, 10%
        (3, 1): [
            {
                "enunciado": "Calcula el <span class=\"keyword-highlight\">50% de 60 monedas</span>.",
                "pasos": [
                    {"orden": 1, "texto": "El 50% significa exactamente la mitad de un total (50 de cada 100)."},
                    {"orden": 2, "texto": "Dividimos el total entre 2 para calcular la mitad: <span class=\"keyword-highlight\">60 ÷ 2 = 30</span>."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">30 monedas</span>."}
                ]
            },
            {
                "enunciado": "Calcula el <span class=\"keyword-highlight\">25% de 80 puntos</span>.",
                "pasos": [
                    {"orden": 1, "texto": "El 25% representa una cuarta parte (1/4) de la unidad."},
                    {"orden": 2, "texto": "Dividimos el total de puntos entre 4: <span class=\"keyword-highlight\">80 ÷ 4 = 20</span>."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">20 puntos</span>."}
                ]
            },
            {
                "enunciado": "Calcula el <span class=\"keyword-highlight\">10% de 350 monedas</span>.",
                "pasos": [
                    {"orden": 1, "texto": "El 10% representa una décima parte (1/10) del total."},
                    {"orden": 2, "texto": "Dividimos entre 10 quitando el cero del final: <span class=\"keyword-highlight\">350 ÷ 10 = 35</span>."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">35 monedas</span>."}
                ]
            },
            {
                "enunciado": "Un artículo de 20 pesos tiene un descuento del <span class=\"keyword-highlight\">50%</span>. ¿Cuál es el precio final?",
                "pasos": [
                    {"orden": 1, "texto": "Calculamos el descuento del 50% (la mitad): <span class=\"keyword-highlight\">20 ÷ 2 = 10 pesos</span> de rebaja."},
                    {"orden": 2, "texto": "Restamos la rebaja del precio original: <span class=\"keyword-highlight\">20 - 10 = 10</span>."},
                    {"orden": 3, "texto": "Precio final: <span class=\"keyword-highlight\">10 pesos</span>."}
                ]
            }
        ],
        # Nivel 2: Lectura e interpretación de gráficos circulares
        (3, 2): [
            {
                "enunciado": "En un gráfico circular, el <span class=\"keyword-highlight\">40%</span> prefiere fútbol, el <span class=\"keyword-highlight\">35%</span> básquet y el resto vóley. ¿Qué porcentaje prefiere vóley?<br/>"
                             "<svg width='100' height='100' viewBox='0 0 100 100' style='margin:10px auto; display:block; filter: drop-shadow(0px 3px 5px rgba(0,0,0,0.4));'>"
                             "  <circle cx='50' cy='50' r='40' fill='#4B5563'/>"
                             "  <!-- Fútbol 40% (144 grados): de 0 a 144 -->"
                             "  <path d='M50,50 L50,10 A40,40 0 0,1 88,37.6 Z' fill='#3B82F6' stroke='#1F2937'/>"
                             "  <!-- Básquet 35% (126 grados): de 144 a 270 -->"
                             "  <path d='M50,50 L88,37.6 A40,40 0 0,1 50,90 Z' fill='#F59E0B' stroke='#1F2937'/>"
                             "  <!-- Vóley 25% (90 grados): de 270 a 360 -->"
                             "  <path d='M50,50 L50,90 A40,40 0 0,1 10,50 A40,40 0 0,1 50,10 Z' fill='#10B981' stroke='#1F2937'/>"
                             "  <circle cx='50' cy='50' r='18' fill='#1F2937'/>"
                             "</svg>",
                "pasos": [
                    {"orden": 1, "texto": "La suma total de todas las rebanadas de un gráfico circular es siempre <span class=\"keyword-highlight\">100%</span>."},
                    {"orden": 2, "texto": "Sumamos los porcentajes de fútbol y básquet: <span class=\"keyword-highlight\">40% + 35% = 75%</span>."},
                    {"orden": 3, "texto": "Restamos esa suma del 100% total: <span class=\"keyword-highlight\">100% - 75% = 25%</span> de preferencia por vóley."}
                ]
            },
            {
                "enunciado": "De 200 alumnos encuestados, el <span class=\"keyword-highlight\">25%</span> prefiere matemáticas. ¿Cuántos alumnos son?",
                "pasos": [
                    {"orden": 1, "texto": "El 25% equivale a una cuarta parte del grupo entero (1/4)."},
                    {"orden": 2, "texto": "Dividimos los alumnos totales entre 4: <span class=\"keyword-highlight\">200 ÷ 4 = 50</span>."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">50 alumnos</span>."}
                ]
            },
            {
                "enunciado": "En un gráfico sobre mascotas, el 50% son perros, el 30% gatos y el resto peces. ¿Qué porcentaje representan los peces?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos perros y gatos: <span class=\"keyword-highlight\">50% + 30% = 80%</span>."},
                    {"orden": 2, "texto": "Restamos de la unidad total (100%): <span class=\"keyword-highlight\">100% - 80% = 20%</span>."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">20%</span> son peces."}
                ]
            },
            {
                "enunciado": "Si un pastel representa un total de 120 rebanadas, y el 10% son de fresa, ¿cuántas son de fresa?",
                "pasos": [
                    {"orden": 1, "texto": "El 10% equivale a dividir el total entre 10."},
                    {"orden": 2, "texto": "Dividimos: <span class=\"keyword-highlight\">120 ÷ 10 = 12</span> rebanadas."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">12 rebanadas de fresa</span>."}
                ]
            }
        ],
        # Nivel 3: Comparación de tasas en gráficos de barras
        (3, 3): [
            {
                "enunciado": "Un gráfico de barras muestra: Región A = <span class=\"keyword-highlight\">450</span>, Región B = <span class=\"keyword-highlight\">320</span>, Región C = <span class=\"keyword-highlight\">530</span>. ¿Cuántas empresas hay en total?<br/>"
                             "<svg width='180' height='100' viewBox='0 0 180 100' style='margin:10px auto; display:block; background:#1F2937; border-radius:10px; padding:5px;'>"
                             "  <!-- Barra A (altura 60%) -->"
                             "  <rect x='20' y='30' width='25' height='55' fill='#EF4444' rx='3'/>"
                             "  <text x='32.5' y='95' fill='#FFF' font-size='9' text-anchor='middle'>A</text>"
                             "  <text x='32.5' y='25' fill='#EF4444' font-size='9' font-weight='bold' text-anchor='middle'>450</text>"
                             "  "
                             "  <!-- Barra B (altura 40%) -->"
                             "  <rect x='70' y='45' width='25' height='40' fill='#F59E0B' rx='3'/>"
                             "  <text x='82.5' y='95' fill='#FFF' font-size='9' text-anchor='middle'>B</text>"
                             "  <text x='82.5' y='40' fill='#F59E0B' font-size='9' font-weight='bold' text-anchor='middle'>320</text>"
                             "  "
                             "  <!-- Barra C (altura 70%) -->"
                             "  <rect x='120' y='20' width='25' height='65' fill='#3B82F6' rx='3'/>"
                             "  <text x='132.5' y='95' fill='#FFF' font-size='9' text-anchor='middle'>C</text>"
                             "  <text x='132.5' y='15' fill='#3B82F6' font-size='9' font-weight='bold' text-anchor='middle'>530</text>"
                             "  <line x1='10' y1='85' x2='170' y2='85' stroke='#4B5563' stroke-width='2'/>"
                             "</svg>",
                "pasos": [
                    {"orden": 1, "texto": "Para hallar el total, sumamos la altura y valor representado por cada barra."},
                    {"orden": 2, "texto": "Sumamos los tres valores: <span class=\"keyword-highlight\">450 + 320 + 530</span>."},
                    {"orden": 3, "texto": "Resultado acumulado: <span class=\"keyword-highlight\">1300 empresas</span>."}
                ]
            },
            {
                "enunciado": "Usando el gráfico anterior, ¿cuántas empresas más tiene la Región C que la Región B?",
                "pasos": [
                    {"orden": 1, "texto": "Buscamos los valores correspondientes: Región C = 530, Región B = 320."},
                    {"orden": 2, "texto": "Restamos el menor del mayor para hallar la diferencia: <span class=\"keyword-highlight\">530 - 320 = 210</span>."},
                    {"orden": 3, "texto": "La Región C tiene <span class=\"keyword-highlight\">210 empresas más</span>."}
                ]
            },
            {
                "enunciado": "Las barras indican ventas: Enero = 150, Febrero = 200, Marzo = 120. ¿Cuál fue el mes con mayor volumen y cuánto vendió?",
                "pasos": [
                    {"orden": 1, "texto": "Identificamos la barra con mayor altura en el gráfico: Febrero."},
                    {"orden": 2, "texto": "Leemos el valor numérico en la escala: 200 unidades."},
                    {"orden": 3, "texto": "El mes mayor es <span class=\"keyword-highlight\">Febrero con 200</span>."}
                ]
            },
            {
                "enunciado": "Si en la Región A hay 450 y en la B 320, ¿cuál es la suma combinada de ambas regiones?",
                "pasos": [
                    {"orden": 1, "texto": "Planteamos la suma simple: A + B = <span class=\"keyword-highlight\">450 + 320</span>."},
                    {"orden": 2, "texto": "Resolvemos la suma: 770."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">770</span>."}
                ]
            }
        ],
        # Nivel 4: El Punto de Equilibrio - Media Aritmética
        (3, 4): [
            {
                "enunciado": "Calcula el promedio de libros leídos por tres niños: <span class=\"keyword-highlight\">3, 7 y 5 libros</span>.<br/>"
                             "<svg width='300' height='120' viewBox='0 0 200 80' style='margin:10px auto; display:block;'>"
                             "  <!-- Tres torres de 3, 7, 5 bloques -->"
                             "  <text x='25' y='75' fill='#FFF' font-size='10' text-anchor='middle'>3</text>"
                             "  <rect x='15' y='50' width='20' height='10' fill='#F59E0B' stroke='#78350F'/>"
                             "  <rect x='15' y='60' width='20' height='10' fill='#F59E0B' stroke='#78350F'/>"
                             "  "
                             "  <text x='75' y='75' fill='#FFF' font-size='10' text-anchor='middle'>7</text>"
                             "  <rect x='65' y='10' width='20' height='10' fill='#EC4899' stroke='#5B21B6'/>"
                             "  <rect x='65' y='20' width='20' height='10' fill='#EC4899' stroke='#5B21B6'/>"
                             "  <rect x='65' y='30' width='20' height='10' fill='#EC4899' stroke='#5B21B6'/>"
                             "  <rect x='65' y='40' width='20' height='10' fill='#EC4899' stroke='#5B21B6'/>"
                             "  <rect x='65' y='50' width='20' height='10' fill='#EC4899' stroke='#5B21B6'/>"
                             "  <rect x='65' y='60' width='20' height='10' fill='#EC4899' stroke='#5B21B6'/>"
                             "  "
                             "  <text x='125' y='75' fill='#FFF' font-size='10' text-anchor='middle'>5</text>"
                             "  <rect x='115' y='30' width='20' height='10' fill='#10B981' stroke='#064E3B'/>"
                             "  <rect x='115' y='40' width='20' height='10' fill='#10B981' stroke='#064E3B'/>"
                             "  <rect x='115' y='50' width='20' height='10' fill='#10B981' stroke='#064E3B'/>"
                             "  <rect x='115' y='60' width='20' height='10' fill='#10B981' stroke='#064E3B'/>"
                             "  "

                             "</svg>",
                "pasos": [
                    {"orden": 1, "texto": "<b>Paso 1 (Sumar):</b> Juntamos todos los libros en una sola gran pila: <span class=\"keyword-highlight\">3 + 7 + 5 = 15</span> libros."},
                    {"orden": 2, "texto": "<b>Paso 2 (Dividir):</b> Repartimos la pila entre la cantidad de niños (3): <span class=\"keyword-highlight\">15 ÷ 3 = 5</span> libros."},
                    {"orden": 3, "texto": "Resultado: El promedio equilibrado es <span class=\"keyword-highlight\">5 libros</span>."}
                ]
            },
            {
                "enunciado": "Calcula el promedio de edad entre dos hermanos de <span class=\"keyword-highlight\">10 y 20 años</span>.",
                "pasos": [
                    {"orden": 1, "texto": "Paso 1: Sumamos las edades de ambos: <span class=\"keyword-highlight\">10 + 20 = 30</span>."},
                    {"orden": 2, "texto": "Paso 2: Dividimos la suma entre los 2 hermanos: <span class=\"keyword-highlight\">30 ÷ 2 = 15</span>."},
                    {"orden": 3, "texto": "Resultado: El promedio es <span class=\"keyword-highlight\">15 años</span>."}
                ]
            },
            {
                "enunciado": "Calcula el promedio de las siguientes cuatro notas: <span class=\"keyword-highlight\">2, 4, 6 y 8</span>.",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos las cuatro notas obtenidas: <span class=\"keyword-highlight\">2 + 4 + 6 + 8 = 20</span>."},
                    {"orden": 2, "texto": "Dividimos el total entre las 4 notas: <span class=\"keyword-highlight\">20 ÷ 4 = 5</span>."},
                    {"orden": 3, "texto": "Resultado: El promedio es <span class=\"keyword-highlight\">5</span>."}
                ]
            },
            {
                "enunciado": "Si tienes tres bolsas con dulces: 6, 8 y 10. ¿Cuál es el promedio de dulces por bolsa?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos los dulces de las tres bolsas: <span class=\"keyword-highlight\">6 + 8 + 10 = 24</span>."},
                    {"orden": 2, "texto": "Dividimos la suma entre las 3 bolsas: <span class=\"keyword-highlight\">24 ÷ 3 = 8</span>."},
                    {"orden": 3, "texto": "El promedio de dulces es: <span class=\"keyword-highlight\">8 dulces</span>."}
                ]
            }
        ],

        # --- MÓDULO 4: RAZÓN Y MEZCLAS ---
        # Nivel 1: Razones simples (a:b) y proporcionalidad directa
        (4, 1): [
            {
                "enunciado": "La receta de limonada exige <span class=\"keyword-highlight\">3 tazas de agua por 1 de limón</span> (3:1). Si pones <span class=\"keyword-highlight\">2 de limón</span>, ¿cuánta agua necesitas?<br/>"
                             "<svg width='240' height='135' viewBox='0 0 160 90' style='margin:10px auto; display:block;'>\n"
                             "  <!-- Receta base vs receta duplicada -->\n"
                             "  <text x='10' y='20' fill='#FFE082' font-size='9' font-weight='bold'>Base (3:1)</text>\n"
                             "  <rect x='10' y='30' width='12' height='12' fill='#FBBF24' rx='2'/><rect x='25' y='30' width='12' height='12' fill='#3B82F6' rx='2'/><rect x='40' y='30' width='12' height='12' fill='#3B82F6' rx='2'/><rect x='55' y='30' width='12' height='12' fill='#3B82F6' rx='2'/>\n"
                             "  \n"
                             "  <text x='90' y='20' fill='#A855F7' font-size='9' font-weight='bold'>Duplicado (6:2)</text>\n"
                             "  <rect x='90' y='30' width='12' height='12' fill='#FBBF24' rx='2'/><rect x='105' y='30' width='12' height='12' fill='#FBBF24' rx='2'/>\n"
                             "  <rect x='90' y='45' width='12' height='12' fill='#3B82F6' rx='2'/><rect x='105' y='45' width='12' height='12' fill='#3B82F6' rx='2'/><rect x='120' y='45' width='12' height='12' fill='#3B82F6' rx='2'/>\n"
                             "  <rect x='135' y='45' width='12' height='12' fill='#3B82F6' rx='2'/><rect x='120' y='30' width='12' height='12' fill='#3B82F6' rx='2'/><rect x='135' y='30' width='12' height='12' fill='#3B82F6' rx='2'/>\n"
                             "  \n"
                             "  <!-- Leyenda de ingredientes -->\n"
                             "  <rect x='30' y='75' width='8' height='8' fill='#FBBF24' rx='1'/><text x='42' y='81' fill='#94a3b8' font-size='7' font-weight='bold'>Limón</text>\n"
                             "  <rect x='90' y='75' width='8' height='8' fill='#3B82F6' rx='1'/><text x='102' y='81' fill='#94a3b8' font-size='7' font-weight='bold'>Agua</text>\n"
                             "</svg>",
                "pasos": [
                    {"orden": 1, "texto": "Identificamos la escala: la receta original pide 1 de limón y ahora usamos 2. La receta se duplicó (×2)."},
                    {"orden": 2, "texto": "Multiplicamos la cantidad original de agua por 2: <span class=\"keyword-highlight\">3 × 2 = 6</span> tazas."},
                    {"orden": 3, "texto": "Resultado: Necesitas <span class=\"keyword-highlight\">6 tazas de agua</span>."}
                ]
            },
            {
                "enunciado": "Una pared se pinta combinando <span class=\"keyword-highlight\">2 litros de rojo y 3 de blanco</span> (2:3). Si compras <span class=\"keyword-highlight\">6 litros de rojo</span>, ¿cuántos de blanco necesitas?",
                "pasos": [
                    {"orden": 1, "texto": "Hallamos el factor multiplicador: el rojo pasó de 2 a 6. Esto es el triple: <span class=\"keyword-highlight\">6 ÷ 2 = 3</span> veces."},
                    {"orden": 2, "texto": "Multiplicamos el blanco por el mismo factor de 3: <span class=\"keyword-highlight\">3 × 3 = 9</span> litros."},
                    {"orden": 3, "texto": "Resultado: Necesitas <span class=\"keyword-highlight\">9 litros de blanco</span>."}
                ]
            },
            {
                "enunciado": "Para preparar cemento se usa <span class=\"keyword-highlight\">1 porción de cemento por 4 de arena</span>. Si usas <span class=\"keyword-highlight\">2 de cemento</span>, ¿cuánta arena aportas?",
                "pasos": [
                    {"orden": 1, "texto": "El cemento se duplicó (de 1 a 2)."},
                    {"orden": 2, "texto": "Multiplicamos la arena por 2: <span class=\"keyword-highlight\">4 × 2 = 8</span>."},
                    {"orden": 3, "texto": "Resultado: <span class=\"keyword-highlight\">8 porciones de arena</span>."}
                ]
            },
            {
                "enunciado": "La masa de galletas requiere <span class=\"keyword-highlight\">1 vaso de leche por 2 de harina</span> (1:2). Si pones <span class=\"keyword-highlight\">4 vasos de harina</span>, ¿cuántos de leche usarás?",
                "pasos": [
                    {"orden": 1, "texto": "La harina requerida aumentó de 2 a 4 vasos (se duplicó)."},
                    {"orden": 2, "texto": "Para balancear, dividimos la harina entre 2 para saber la leche: <span class=\"keyword-highlight\">4 ÷ 2 = 2</span>."},
                    {"orden": 3, "texto": "Resultado: Usarás <span class=\"keyword-highlight\">2 vasos de leche</span>."}
                ]
            }
        ],
        # Nivel 2: Reparto proporcional de volúmenes macro
        (4, 2): [
            {
                "enunciado": "Para hacer pintura verde mezclas <span class=\"keyword-highlight\">2 litros de azul y 3 de amarillo</span> (haciendo 5 litros en total). Si quieres <span class=\"keyword-highlight\">30 litros de verde</span>, ¿cuántos de azul usas?<br/>"
                             "<svg width='180' height='60' viewBox='0 0 180 60' style='margin:10px auto; display:block;'>"
                             "  <!-- Tubo medidor con azul y amarillo -->"
                             "  <rect x='10' y='10' width='160' height='25' fill='none' stroke='#FFF' stroke-width='2' rx='5'/>"
                             "  <rect x='11' y='11' width='64' height='23' fill='#3B82F6' rx='4'/>"
                             "  <rect x='75' y='11' width='94' height='23' fill='#FBBF24' rx='4'/>"
                             "  <text x='43' y='26' fill='#FFF' font-size='9' font-weight='black' text-anchor='middle'>Azul (12L)</text>"
                             "  <text x='122' y='26' fill='#111827' font-size='9' font-weight='black' text-anchor='middle'>Amarillo (18L)</text>"
                             "  <text x='90' y='50' fill='#FFF' font-size='10' text-anchor='middle'>Verde total = 30 Litros</text>"
                             "</svg>",
                "pasos": [
                    {"orden": 1, "texto": "<b>Paso 1 (Escala):</b> Dividimos la cantidad total deseada entre la receta base: <span class=\"keyword-highlight\">30 ÷ 5 = 6 veces</span> la receta."},
                    {"orden": 2, "texto": "<b>Paso 2 (Multiplicar):</b> Escalamos el ingrediente azul por el factor 6: <span class=\"keyword-highlight\">2 × 6 = 12</span> litros."},
                    {"orden": 3, "texto": "Resultado: Necesitas <span class=\"keyword-highlight\">12 litros de azul</span>."}
                ]
            },
            {
                "enunciado": "Haces pintura rosa con <span class=\"keyword-highlight\">1 litro de rojo y 4 de blanco</span> (5 litros total). Para un lote de <span class=\"keyword-highlight\">50 litros</span>, ¿cuánto blanco comprarás?",
                "pasos": [
                    {"orden": 1, "texto": "Escala de la mezcla: dividimos el total entre la receta base: <span class=\"keyword-highlight\">50 ÷ 5 = 10 lotes</span>."},
                    {"orden": 2, "texto": "Multiplicamos el ingrediente blanco por 10: <span class=\"keyword-highlight\">4 × 10 = 40</span>."},
                    {"orden": 3, "texto": "Resultado: Comprarás <span class=\"keyword-highlight\">40 litros de blanco</span>."}
                ]
            },
            {
                "enunciado": "Una mezcla de concreto tiene <span class=\"keyword-highlight\">3 paladas de arena y 7 de grava</span> (10 en total). Si necesitas <span class=\"keyword-highlight\">40 paladas</span> de mezcla total, ¿cuántas son de arena?",
                "pasos": [
                    {"orden": 1, "texto": "Escala de mezcla: dividimos el total deseado entre la base: <span class=\"keyword-highlight\">40 ÷ 10 = 4 veces</span>."},
                    {"orden": 2, "texto": "Multiplicamos la arena por 4: <span class=\"keyword-highlight\">3 × 4 = 12</span> paladas."},
                    {"orden": 3, "texto": "Resultado: Aportarás <span class=\"keyword-highlight\">12 paladas de arena</span>."}
                ]
            },
            {
                "enunciado": "Un jarabe se hace con <span class=\"keyword-highlight\">1 taza de agua y 1 de jugo concentrado de fruta</span> (2 en total). Si quieres hacer <span class=\"keyword-highlight\">20 litros</span> de jarabe, ¿cuánto concentrado lleva?",
                "pasos": [
                    {"orden": 1, "texto": "Escala de la mezcla: dividimos los litros finales entre la base: <span class=\"keyword-highlight\">20 ÷ 2 = 10 veces</span>."},
                    {"orden": 2, "texto": "Multiplicamos el jugo concentrado por 10: <span class=\"keyword-highlight\">1 × 10 = 10</span>."},
                    {"orden": 3, "texto": "Resultado: Lleva <span class=\"keyword-highlight\">10 litros de concentrado</span>."}
                ]
            }
        ],
        # Nivel 3: Homogeneización de mezclas complejas
        (4, 3): [
            {
                "enunciado": "Un frasco de perfume mezcla <span class=\"keyword-highlight\">1 parte de esencia por 4 partes de alcohol</span> (1:4). ¿Qué porcentaje representa la esencia?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos todas las partes de la mezcla: <span class=\"keyword-highlight\">1 + 4 = 5 partes en total</span>."},
                    {"orden": 2, "texto": "La esencia representa 1 de esas 5 partes, es decir, la fracción: <span class=\"keyword-highlight\">1/5</span>."},
                    {"orden": 3, "texto": "Convertimos 1/5 a porcentaje: (1 ÷ 5) × 100 = <span class=\"keyword-highlight\">20%</span>. Resultado: <span class=\"keyword-highlight\">20%</span>."}
                ]
            },
            {
                "enunciado": "Si tienes una bebida de 300 ml que contiene <span class=\"keyword-highlight\">10% de jugo real</span>, ¿cuántos ml de jugo real tiene?",
                "pasos": [
                    {"orden": 1, "texto": "El 10% representa una décima parte del líquido total (dividir entre 10)."},
                    {"orden": 2, "texto": "Dividimos el total de la bebida: <span class=\"keyword-highlight\">300 ÷ 10 = 30</span>."},
                    {"orden": 3, "texto": "Resultado: Tiene <span class=\"keyword-highlight\">30 ml</span> de jugo real."}
                ]
            },
            {
                "enunciado": "En una aleación de oro y cobre de 100 gramos, el 75% es oro. ¿Cuántos gramos de cobre hay?",
                "pasos": [
                    {"orden": 1, "texto": "Si el 75% es oro, el cobre restante es: <span class=\"keyword-highlight\">100% - 75% = 25%</span> (un cuarto)."},
                    {"orden": 2, "texto": "Calculamos el 25% de 100 gramos: <span class=\"keyword-highlight\">100 ÷ 4 = 25</span> gramos."},
                    {"orden": 3, "texto": "Resultado: Hay <span class=\"keyword-highlight\">25 gramos de cobre</span>."}
                ]
            },
            {
                "enunciado": "Una mezcla de agua salada de 80 gramos contiene <span class=\"keyword-highlight\">10% de sal</span>. Si se evaporan 30 gramos de agua pura, ¿cuánta sal queda?",
                "pasos": [
                    {"orden": 1, "texto": "La sal no se evapora, solo el agua pura. Así que la sal sigue siendo la misma masa."},
                    {"orden": 2, "texto": "Calculamos la sal inicial: 10% de 80 g = <span class=\"keyword-highlight\">8 gramos</span> de sal."},
                    {"orden": 3, "texto": "Resultado final: Quedan exactamente <span class=\"keyword-highlight\">8 gramos de sal</span>."}
                ]
            }
        ]
    }
    return ejemplos_db.get((modulo_id, nivel_id), [])
