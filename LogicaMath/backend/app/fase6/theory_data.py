"""
Guión pedagógico de teoría para los 15 niveles de la Fase 6 (Geometría Plana Multiforme y Áreas).
Cumple con las Secciones 8, 9 y 12 de docs/reestructuraciondefases.md.

Contiene:
  - 15 niveles en niveles_teoria_pool (M1: 4 niveles, M2: 3 niveles, M3: 5 niveles, M4: 3 niveles).
  - 5 ejemplos guiados por nivel (los 2 últimos son TJS resueltos paso a paso).
  - 3 interactivos de evocación por nivel (cálculo directo).
  - Diccionario pedagógico y trampas advertencia.
"""

from app.utils.svg_figuras import (
    escalera_unidades, tabla_datos, color_modulo
)

FASE6_TEORIA_DATA = [
    # =========================================================================
    # MÓDULO 1: Reconocimiento y Perímetros Simples (secciones 101, 102, 103, 104)
    # =========================================================================
    {
        "modulo_id": 1, "nivel_id": 1, "seccion": 101,
        "titulo": "Figuras planas: nombrar, contar vértices y lados",
        "texto_descubrimiento": (
            "¡Bienvenida a la Geometría Plana! 🔺 Hoy descubres las figuras bidimensionales: "
            "formas planas que viven en una hoja de papel. Aprenderás a reconocerlas por su cantidad de lados rectos y vértices "
            "(las esquinas donde se cruzan dos lados). Recordatorio: aquí solo exploramos figuras planas 2D, ¡cero cuerpos 3D!"
        ),
        "cuerpo_teoria": (
            "Elementos básicos de las figuras planas:\n"
            "1. Lado: segmento de recta que forma el borde de la figura.\n"
            "2. Vértice: punto de encuentro donde se unen dos lados (las esquinas).\n"
            "3. Nombres por cantidad de lados:\n"
            "   - 3 lados / 3 vértices: Triángulo\n"
            "   - 4 lados / 4 vértices: Cuadrilátero\n"
            "   - 5 lados / 5 vértices: Pentágono\n"
            "   - 6 lados / 6 vértices: Hexágono\n"
            "   - 8 lados / 8 vértices: Octágono"
        ),
        "advertencia": (
            "¡Atención, exploradora! No confundas los lados con los vértices. Los lados son las líneas del borde; "
            "los vértices son las esquinas puntudas. En todo polígono cerrado, la cantidad de lados siempre es idéntica a la de vértices."
        ),
        "diccionario": {
            "Polígono": "Figura plana cerrada formada por segmentos de recta.",
            "Lado": "Segmento recto que limita la figura.",
            "Vértice": "Punto de unión entre dos lados rectos."
        },
        "ejemplos": [
            {
                "enunciado": "Un triángulo dibujado en la pizarra. ¿Cuántos vértices tiene?",
                "pasos": [
                    {"orden": 1, "texto": "Contamos las esquinas del triángulo: 1, 2, 3."},
                    {"orden": 2, "texto": "Un triángulo siempre tiene 3 vértices."}
                ]
            },
            {
                "enunciado": "Una figura cerrada tiene 6 lados rectos. ¿Cómo se llama?",
                "pasos": [
                    {"orden": 1, "texto": "6 lados rectos corresponden a un hexágono."},
                    {"orden": 2, "texto": "Se llama Hexágono."}
                ]
            },
            {
                "enunciado": "Contar los lados y vértices de un rectángulo.",
                "pasos": [
                    {"orden": 1, "texto": "Lados: 4 líneas rectos. Vértices: 4 esquinas."},
                    {"orden": 2, "texto": "Tiene 4 lados y 4 vértices."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Bruno dice que un octágono tiene 6 vértices. ¿Tiene razón?",
                "pasos": [
                    {"orden": 1, "texto": "Un octágono se define por tener 8 lados y 8 vértices."},
                    {"orden": 2, "texto": "Bruno se equivocó: confundió octágono con hexágono."},
                    {"orden": 3, "texto": "Respuesta: No, el octágono tiene 8 vértices."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Ana dibuja una figura de 5 vértices. ¿Qué nombre recibe?",
                "pasos": [
                    {"orden": 1, "texto": "5 vértices implican 5 lados rectos."},
                    {"orden": 2, "texto": "Respuesta: Pentágono."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "¿Cuántos vértices tiene un cuadrilátero?",
                "respuesta": "4",
                "feedback_acierto": "¡Correcto! Todo cuadrilátero tiene 4 vértices.",
                "feedback_error": "Un cuadrilátero tiene 4 lados y 4 vértices."
            },
            {
                "enunciado": "¿Cuántos lados rectos tiene un hexágono?",
                "respuesta": "6",
                "feedback_acierto": "¡Excelente! Hexá = 6 lados.",
                "feedback_error": "Un hexágono tiene 6 lados."
            },
            {
                "enunciado": "¿Cuántos vértices tiene un triángulo?",
                "respuesta": "3",
                "feedback_acierto": "¡Brillante! Tri = 3 vértices.",
                "feedback_error": "Un triángulo tiene 3 vértices."
            }
        ]
    },

    {
        "modulo_id": 1, "nivel_id": 2, "seccion": 102,
        "titulo": "Clasificación de polígonos y cuadriláteros",
        "texto_descubrimiento": (
            "¡Clasifica polígonos como una experta! 📐 Los polígonos se clasifican en **regulares** (todos sus lados y ángulos iguales) "
            "e **irregulares** (lados de distintas medidas). Entre los cuadriláteros (4 lados), tenemos paralelogramos, trapecios y trapezoides."
        ),
        "cuerpo_teoria": (
            "Clasificación esencial:\n"
            "1. Polígono Regular: todos sus lados miden exactamente lo mismo (ej. cuadrado, triángulo equilátero).\n"
            "2. Polígono Irregular: sus lados tienen medidas distintas.\n"
            "3. Cuadriláteros:\n"
            "   - Paralelogramo: 2 pares de lados opuestos paralelos (cuadrado, rectángulo, rombo).\n"
            "   - Trapecio: solo 1 par de lados paralelos.\n"
            "   - Trapezoide: ningún par de lados paralelos."
        ),
        "advertencia": (
            "¡Cuidado! Todo cuadrado es un rectángulo y un paralelogramo, pero no todo rectángulo es un cuadrado. El cuadrado exige 4 lados de igual longitud."
        ),
        "diccionario": {
            "Polígono Regular": "Polígono con todos sus lados y ángulos iguales.",
            "Paralelogramo": "Cuadrilátero con lados opuestos paralelos dos a dos.",
            "Trapecio": "Cuadrilátero con exactamente un par de lados paralelos."
        },
        "ejemplos": [
            {
                "enunciado": "Un rectángulo mide 8 cm de base y 4 cm de altura. ¿Es regular o irregular?",
                "pasos": [
                    {"orden": 1, "texto": "Sus lados no miden todos igual (8 y 4)."},
                    {"orden": 2, "texto": "Respuesta: Irregular."}
                ]
            },
            {
                "enunciado": "Un triángulo tiene sus 3 lados de 5 cm cada uno. ¿Cómo se clasifica?",
                "pasos": [
                    {"orden": 1, "texto": "Todos los lados son iguales."},
                    {"orden": 2, "texto": "Respuesta: Triángulo equilátero o regular."}
                ]
            },
            {
                "enunciado": "Figura de 4 lados con solo 2 lados paralelos. ¿Qué tipo de cuadrilátero es?",
                "pasos": [
                    {"orden": 1, "texto": "Tiene exactamente 1 par de lados paralelos."},
                    {"orden": 2, "texto": "Respuesta: Trapecio."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Leo afirma que un rectángulo de 6 cm × 3 cm es un polígono regular. ¿Tiene razón?",
                "pasos": [
                    {"orden": 1, "texto": "Un polígono regular requiere 4 lados de idéntica medida."},
                    {"orden": 2, "texto": "6 ≠ 3, por lo que es un polígono irregular."},
                    {"orden": 3, "texto": "Leo está equivocado."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: ¿En qué se diferencia un rombo de un rectángulo?",
                "pasos": [
                    {"orden": 1, "texto": "El rombo tiene 4 lados iguales; el rectángulo tiene ángulos rectos pero lados opuestos iguales."},
                    {"orden": 2, "texto": "Ambos son paralelogramos."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "¿Un cuadrado de 4 cm de lado es un polígono regular o irregular?",
                "respuesta": "regular",
                "feedback_acierto": "¡Correcto! Sus 4 lados miden igual.",
                "feedback_error": "Tiene lados iguales, es regular."
            },
            {
                "enunciado": "¿Cuántos pares de lados paralelos tiene un trapecio?",
                "respuesta": "1",
                "feedback_acierto": "¡Excelente! Solo 1 par de lados paralelos.",
                "feedback_error": "El trapecio tiene exactamente 1 par de lados paralelos."
            },
            {
                "enunciado": "¿Cómo se llama el cuadrilátero con lados opuestos paralelos dos a dos?",
                "respuesta": "paralelogramo",
                "feedback_acierto": "¡Brillante! Paralelogramo.",
                "feedback_error": "Se llama paralelogramo."
            }
        ]
    },

    {
        "modulo_id": 1, "nivel_id": 3, "seccion": 103,
        "titulo": "Ejes de simetría",
        "texto_descubrimiento": (
            "¡Encuentra el espejo secreto de las figuras! 🪞 El **eje de simetría** es una línea imaginaria que divide a una figura "
            "en dos mitades idénticas que encajan perfectamente si las doblas una sobre la otra."
        ),
        "cuerpo_teoria": (
            "Conceptos de simetría:\n"
            "1. Eje de simetría: línea recta que corta la figura en dos partes especulares (reflejadas).\n"
            "2. Cantidad de ejes por figura:\n"
            "   - Cuadrado: 4 ejes de simetría.\n"
            "   - Rectángulo (no cuadrado): 2 ejes de simetría.\n"
            "   - Triángulo equilátero: 3 ejes.\n"
            "   - Círculo: infinitos ejes de simetría (cualquier diámetro)."
        ),
        "advertencia": (
            "¡Ojo con la diagonal del rectángulo! Doblar un rectángulo no cuadrado por su diagonal NO hace coincidir los bordes, "
            "por lo que la diagonal NO es un eje de simetría en el rectángulo (solo lo es en el cuadrado)."
        ),
        "diccionario": {
            "Eje de simetría": "Línea que divide una figura en dos mitades exactamente superponibles por doblez.",
            "Simetría": "Correspondencia exacta en forma, tamaño y posición de las partes de un todo."
        },
        "ejemplos": [
            {
                "enunciado": "¿Cuántos ejes de simetría tiene un cuadrado?",
                "pasos": [
                    {"orden": 1, "texto": "Tiene 2 ejes verticales/horizontales y 2 ejes diagonales."},
                    {"orden": 2, "texto": "En total: 4 ejes de simetría."}
                ]
            },
            {
                "enunciado": "¿Cuántos ejes de simetría tiene un círculo?",
                "pasos": [
                    {"orden": 1, "texto": "Cualquier recta que pase por el centro divide al círculo en mitades iguales."},
                    {"orden": 2, "texto": "Tiene infinitos ejes de simetría."}
                ]
            },
            {
                "enunciado": "¿Cuántos ejes de simetría tiene un rectángulo de 6 cm × 4 cm?",
                "pasos": [
                    {"orden": 1, "texto": "Tiene 1 eje vertical y 1 horizontal. Las diagonales no coinciden al doblar."},
                    {"orden": 2, "texto": "Tiene 2 ejes de simetría."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Mía dice que la diagonal de un rectángulo es un eje de simetría. ¿Tiene razón?",
                "pasos": [
                    {"orden": 1, "texto": "Al doblar un rectángulo por la diagonal, los vértices no coinciden."},
                    {"orden": 2, "texto": "Respuesta: No, el rectángulo solo tiene 2 ejes de simetría."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Comparar los ejes de simetría de un triángulo equilátero y un cuadrado. ¿Quién tiene más?",
                "pasos": [
                    {"orden": 1, "texto": "Triángulo equilátero = 3 ejes. Cuadrado = 4 ejes."},
                    {"orden": 2, "texto": "El cuadrado tiene más ejes."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "¿Cuántos ejes de simetría tiene un cuadrado?",
                "respuesta": "4",
                "feedback_acierto": "¡Correcto! 2 principales y 2 diagonales.",
                "feedback_error": "El cuadrado tiene 4 ejes de simetría."
            },
            {
                "enunciado": "¿Cuántos ejes de simetría tiene un rectángulo no cuadrado?",
                "respuesta": "2",
                "feedback_acierto": "¡Excelente! 1 vertical y 1 horizontal.",
                "feedback_error": "El rectángulo tiene 2 ejes."
            },
            {
                "enunciado": "¿Cuántos ejes de simetría tiene un triángulo equilátero?",
                "respuesta": "3",
                "feedback_acierto": "¡Brillante! 1 por cada vértice.",
                "feedback_error": "Un triángulo equilátero tiene 3 ejes."
            }
        ]
    },

    {
        "modulo_id": 1, "nivel_id": 4, "seccion": 104,
        "titulo": "Perímetro sumando lados con decimales",
        "texto_descubrimiento": (
            "¡Aprende a medir el contorno exacto! 📏 El **perímetro** es la suma de las longitudes de todos los lados "
            "que forman el borde exterior de una figura plana. Como los bordes reales miden con decimales, aplicas la suma alineando la coma."
        ),
        "cuerpo_teoria": (
            "Reglas para calcular el perímetro:\n"
            "1. Identifica las medidas de TODOS los lados exteriores de la figura.\n"
            "2. Suma todos los lados alineando las comas decimales.\n"
            "3. En polígonos regulares: multiplica la medida de un lado por la cantidad total de lados."
        ),
        "advertencia": (
            "¡No olvides ningún lado! Si una figura tiene 5 lados, debes sumar 5 números. Y en el perímetro la unidad se mantiene lineal (cm, m), jamás cm²."
        ),
        "diccionario": {
            "Perímetro": "Suma de las longitudes de todos los lados que forman el borde de una figura plana.",
            "Contorno": "Línea o límite exterior de una figura."
        },
        "ejemplos": [
            {
                "enunciado": "Un rectángulo tiene lados de 4,5 cm y 2,3 cm. ¿Cuál es su perímetro?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos sus 4 lados: 4,5 + 2,3 + 4,5 + 2,3."},
                    {"orden": 2, "texto": "4,5 + 2,3 = 6,8; 6,8 × 2 = 13,6 cm."},
                    {"orden": 3, "texto": "Perímetro = 13,6 cm."}
                ]
            },
            {
                "enunciado": "Un pentágono regular tiene lados de 3,2 cm. ¿Cuál es su perímetro?",
                "pasos": [
                    {"orden": 1, "texto": "Tiene 5 lados de 3,2 cm."},
                    {"orden": 2, "texto": "3,2 × 5 = 16,0 cm."},
                    {"orden": 3, "texto": "Perímetro = 16,0 cm."}
                ]
            },
            {
                "enunciado": "Un triángulo con lados de 5,1 cm, 4,2 cm y 6,3 cm. ¿Perímetro?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos los 3 lados: 5,1 + 4,2 + 6,3 = 15,6 cm."},
                    {"orden": 2, "texto": "Perímetro = 15,6 cm."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Para un rectángulo de 5 cm por 3 cm, Hugo escribió Perímetro = 15 cm. ¿En qué falló?",
                "pasos": [
                    {"orden": 1, "texto": "Hugo multiplicó 5 × 3 (calculó el área en vez del perímetro)."},
                    {"orden": 2, "texto": "El perímetro suma todos los bordes: 5 + 3 + 5 + 3 = 16 cm."},
                    {"orden": 3, "texto": "Hugo confundió perímetro con área."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Un cuadrado tiene un perímetro de 20,4 cm. ¿Cuánto mide cada lado?",
                "pasos": [
                    {"orden": 1, "texto": "Un cuadrado tiene 4 lados iguales."},
                    {"orden": 2, "texto": "Dividimos 20,4 ÷ 4 = 5,1 cm."},
                    {"orden": 3, "texto": "Cada lado mide 5,1 cm."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Cuadrado de 3,5 cm de lado. ¿Cuál es su perímetro?",
                "respuesta": "14",
                "feedback_acierto": "¡Correcto! 3,5 × 4 = 14 cm.",
                "feedback_error": "Multiplica 3,5 por 4."
            },
            {
                "enunciado": "Rectángulo de 6,0 cm por 2,5 cm. ¿Cuál es su perímetro?",
                "respuesta": "17",
                "feedback_acierto": "¡Excelente! (6,0 + 2,5) × 2 = 17 cm.",
                "feedback_error": "Suma los 4 lados: 6+2,5+6+2,5 = 17."
            },
            {
                "enunciado": "Triángulo equilátero de 4,2 cm de lado. ¿Perímetro?",
                "respuesta": "12,6",
                "feedback_acierto": "¡Brillante! 4,2 × 3 = 12,6 cm.",
                "feedback_error": "Multiplica 4,2 por 3."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 2: Perímetro de Figuras Compuestas (secciones 201, 202, 203)
    # =========================================================================
    {
        "modulo_id": 2, "nivel_id": 1, "seccion": 201,
        "titulo": "Figuras en L, T y escaleras",
        "texto_descubrimiento": (
            "¡Calcula perímetros de contornos multiformes! 🧩 Las figuras compuestas en L, T o escaleras "
            "tienen más de 4 lados. Para hallar su perímetro debes recorrer todo el contorno exterior sumando cada uno de sus tramos rectos."
        ),
        "cuerpo_teoria": (
            "Pasos para perímetro de compuestas:\n"
            "1. Empieza en una esquina de la figura y avanza en sentido horario.\n"
            "2. Anota la medida de cada segmento del borde exterior.\n"
            "3. Suma todos los segmentos. ¡No cuentes líneas internas que corten la figura!"
        ),
        "advertencia": (
            "¡Cuidado con las líneas internas! Si la figura está dividida en dos rectángulos con una línea de puntos adentro, "
            "esa línea interna NO forma parte del contorno exterior y no se suma al perímetro."
        ),
        "diccionario": {
            "Contorno multiforme": "Borde exterior formado por varios segmentos rectos perpendiculares.",
            "Línea interna": "Segmento de corte imaginario dentro de la figura (no se suma al perímetro)."
        },
        "ejemplos": [
            {
                "enunciado": "Una figura en L tiene bordes de 8 cm, 5 cm, 3 cm, 2 cm, 5 cm y 3 cm. ¿Perímetro?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos los 6 bordes exteriores: 8 + 5 + 3 + 2 + 5 + 3."},
                    {"orden": 2, "texto": "Perímetro = 26 cm."}
                ]
            },
            {
                "enunciado": "Una figura en T con 8 tramos exteriores que miden 6, 2, 2, 4, 2, 4, 2 y 2 cm. ¿Perímetro?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos los 8 tramos exteriores: 6+2+2+4+2+4+2+2 = 24 cm."}
                ]
            },
            {
                "enunciado": "Escalera de 3 escalones de 2 cm por 2 cm. ¿Perímetro?",
                "pasos": [
                    {"orden": 1, "texto": "Cuenta 6 tramos verticales/horizontales de 2 cm más las bases de 6 cm y 6 cm."},
                    {"orden": 2, "texto": "Perímetro = 24 cm."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: En una figura en L, Sofía sumó una línea divisoria interna de 4 cm. ¿Tiene razón?",
                "pasos": [
                    {"orden": 1, "texto": "El perímetro incluye únicamente bordes exteriores."},
                    {"orden": 2, "texto": "Las líneas internas de partición no se suman."},
                    {"orden": 3, "texto": "Sofía se equivocó al sumar la línea interna."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Comparar el perímetro de un rectángulo 8 × 5 con una L de contorno 8, 5, 3, 2, 5, 3. ¿Son iguales?",
                "pasos": [
                    {"orden": 1, "texto": "Rectángulo = 2(8+5) = 26 cm. Figura en L = 8+5+3+2+5+3 = 26 cm."},
                    {"orden": 2, "texto": "¡Tienen el mismo perímetro!"}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Suma los tramos exteriores de la L: 6, 4, 2, 2, 4, 2 cm. ¿Perímetro?",
                "respuesta": "20",
                "feedback_acierto": "¡Correcto! 6+4+2+2+4+2 = 20 cm.",
                "feedback_error": "Suma todos los segmentos exteriores."
            },
            {
                "enunciado": "Figura en T de tramos: 8, 2, 3, 4, 2, 4, 3, 2. ¿Perímetro?",
                "respuesta": "28",
                "feedback_acierto": "¡Excelente! Total = 28 cm.",
                "feedback_error": "Suma los 8 tramos exteriores."
            },
            {
                "enunciado": "Si una L tiene lados de 10, 8, 4, 3, 6, 5. ¿Perímetro?",
                "respuesta": "36",
                "feedback_acierto": "¡Brillante! 10+8+4+3+6+5 = 36 cm.",
                "feedback_error": "10+8+4+3+6+5 = 36 cm."
            }
        ]
    },

    {
        "modulo_id": 2, "nivel_id": 2, "seccion": 202,
        "titulo": "Lados ocultos deducidos por paralelismo",
        "texto_descubrimiento": (
            "¡Conviértete en Detective de Lados Ocultos! 🔍 En muchas figuras compuestas faltan cotas. "
            "Para descubrir la medida de un lado oculto, usas el paralelismo: la suma de los tramos horizontales superiores "
            "es igual al ancho total horizontal inferior (y lo mismo con los tramos verticales)."
        ),
        "cuerpo_teoria": (
            "Regla del Paralelismo para Lados Ocultos:\n"
            "1. Tramos Horizontales: Ancho Total = Tramo Horizontal 1 + Tramo Horizontal 2.\n"
            "2. Tramos Verticales: Alto Total = Tramo Vertical 1 + Tramo Vertical 2.\n"
            "3. Lado Oculto = Total − Tramo Conocido."
        ),
        "advertencia": (
            "¡No intentes adivinar 'a ojo'! Aplica siempre la resta: Total menos la parte conocida te da exactamente la medida del lado oculto."
        ),
        "diccionario": {
            "Lado oculto": "Segmento del borde cuya medida no está escrita en el dibujo y debe deducirse.",
            "Paralelismo": "Propiedad de los lados opuestos en figuras rectilíneas perpendiculares."
        },
        "ejemplos": [
            {
                "enunciado": "En una L de ancho total 10 cm, un escalón mide 6 cm. ¿Cuánto mide el lado oculto horizontal?",
                "pasos": [
                    {"orden": 1, "texto": "Lado Oculto = Ancho Total − Tramo Conocido."},
                    {"orden": 2, "texto": "10 − 6 = 4 cm."},
                    {"orden": 3, "texto": "El lado oculto mide 4 cm."}
                ]
            },
            {
                "enunciado": "Alto total = 8 cm, tramo vertical conocido = 3 cm. ¿Lado vertical oculto?",
                "pasos": [
                    {"orden": 1, "texto": "8 − 3 = 5 cm."},
                    {"orden": 2, "texto": "Mide 5 cm."}
                ]
            },
            {
                "enunciado": "Hallar el perímetro completo de una L con cotas 12 m, 9 m, 5 m y 4 m (dos ocultos).",
                "pasos": [
                    {"orden": 1, "texto": "Oculto horizontal: 12 − 5 = 7 m. Oculto vertical: 9 − 4 = 5 m."},
                    {"orden": 2, "texto": "Perímetro = 12 + 9 + 5 + 4 + 7 + 5 = 42 m."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Mateo supuso que el lado oculto de una L de ancho 10 m era 5 m sin mirar el escalón de 7 m. ¿Es correcto?",
                "pasos": [
                    {"orden": 1, "texto": "Mateo asumió que se dividía a la mitad a ojo."},
                    {"orden": 2, "texto": "Cálculo real: 10 − 7 = 3 m."},
                    {"orden": 3, "texto": "Mateo está equivocado; mide 3 m."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: ¿Por qué en una figura en L recta el perímetro es igual a 2 × (Ancho Total + Alto Total)?",
                "pasos": [
                    {"orden": 1, "texto": "Porque la suma de los dos escalones horizontales equivale al ancho total, y los dos verticales al alto total."},
                    {"orden": 2, "texto": "Perímetro = 2 × (Ancho + Alto)."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Ancho total = 12 cm, escalón conocido = 8 cm. ¿Lado oculto?",
                "respuesta": "4",
                "feedback_acierto": "¡Correcto! 12 − 8 = 4 cm.",
                "feedback_error": "Resta 12 − 8."
            },
            {
                "enunciado": "Alto total = 15 m, escalón conocido = 6 m. ¿Lado oculto?",
                "respuesta": "9",
                "feedback_acierto": "¡Excelente! 15 − 6 = 9 m.",
                "feedback_error": "Resta 15 − 6."
            },
            {
                "enunciado": "Ancho total = 20 cm, escalón conocido = 13 cm. ¿Lado oculto?",
                "respuesta": "7",
                "feedback_acierto": "¡Brillante! 20 − 13 = 7 cm.",
                "feedback_error": "20 − 13 = 7 cm."
            }
        ]
    },

    {
        "modulo_id": 2, "nivel_id": 3, "seccion": 203,
        "titulo": "La circunferencia: perímetro del círculo",
        "texto_descubrimiento": (
            "¡Mide la vuelta completa del círculo! ⭕ El perímetro de un círculo recibe un nombre especial: **circunferencia**. "
            "Para medir la longitud de esa línea curva usamos la fórmula **Circunferencia = 2 × π × radio** (o **π × diámetro**), donde π ≈ 3,14."
        ),
        "cuerpo_teoria": (
            "Fórmulas de la Circunferencia:\n"
            "1. Circunferencia = 2 × π × radio\n"
            "2. Circunferencia = π × diámetro (ya que Diámetro = 2 × radio)\n"
            "3. En esta fase la constante π vale siempre 3,14.\n"
            "4. Recuerda: la circunferencia mide la línea del borde (longitud en cm o m), no la superficie interior."
        ),
        "advertencia": (
            "¡No confundas circunferencia con área del círculo! La circunferencia es la vuelta del borde (2 × π × r); "
            "el área es la superficie interior (π × r²), que se estudia en el Módulo 3."
        ),
        "diccionario": {
            "Circunferencia": "Longitud de la línea curva cerrada que forma el borde del círculo (su perímetro).",
            "Radio": "Distancia del centro a cualquier punto del borde.",
            "Diámetro": "Segmento que une dos puntos del borde pasando por el centro (Diámetro = 2 × radio)."
        },
        "ejemplos": [
            {
                "enunciado": "Un círculo tiene un radio de 5 cm (π = 3,14). ¿Cuál es su circunferencia?",
                "pasos": [
                    {"orden": 1, "texto": "Fórmula: 2 × 3,14 × 5."},
                    {"orden": 2, "texto": "2 × 5 = 10; 10 × 3,14 = 31,4 cm."},
                    {"orden": 3, "texto": "Circunferencia = 31,4 cm."}
                ]
            },
            {
                "enunciado": "Una rueda tiene un diámetro de 10 cm (π = 3,14). ¿Longitud de una vuelta?",
                "pasos": [
                    {"orden": 1, "texto": "Fórmula con diámetro: π × diámetro = 3,14 × 10 = 31,4 cm."}
                ]
            },
            {
                "enunciado": "Un estanque redondo tiene 2 m de radio. ¿Perímetro del borde?",
                "pasos": [
                    {"orden": 1, "texto": "2 × 3,14 × 2 = 12,56 m."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Alba calculó el perímetro de un círculo de radio 4 cm haciendo 3,14 × 16 = 50,24 cm. ¿Dónde se equivocó?",
                "pasos": [
                    {"orden": 1, "texto": "Alba calculó el Área (π × r² = 3,14 × 16) en lugar de la Circunferencia (2 × π × r = 25,12)."},
                    {"orden": 2, "texto": "La circunferencia del borde es 25,12 cm."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Si el radio de una rueda se duplica, ¿qué ocurre con su circunferencia?",
                "pasos": [
                    {"orden": 1, "texto": "Como la fórmula es 2 × π × r, la circunferencia también se duplica."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Radio = 10 cm, π = 3,14. ¿Circunferencia?",
                "respuesta": "62,8",
                "feedback_acierto": "¡Correcto! 2 × 3,14 × 10 = 62,8 cm.",
                "feedback_error": "Multiplica 2 × 3,14 × 10."
            },
            {
                "enunciado": "Diámetro = 20 cm, π = 3,14. ¿Circunferencia?",
                "respuesta": "62,8",
                "feedback_acierto": "¡Excelente! 3,14 × 20 = 62,8 cm.",
                "feedback_error": "Multiplica 3,14 por 20."
            },
            {
                "enunciado": "Radio = 1 cm, π = 3,14. ¿Circunferencia?",
                "respuesta": "6,28",
                "feedback_acierto": "¡Brillante! 2 × 3,14 × 1 = 6,28 cm.",
                "feedback_error": "2 × 3,14 × 1 = 6,28."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 3: Fundamentos de Área (secciones 301, 302, 303, 304, 305)
    # =========================================================================
    {
        "modulo_id": 3, "nivel_id": 1, "seccion": 301,
        "titulo": "El área es contar cuadrados: enteros y mitades",
        "texto_descubrimiento": (
            "¡Hola, cazadora de superficies! 🟦 Hoy desbloqueas un superpoder tranquilo pero poderosísimo: "
            "medir cuánto espacio ocupa una figura contando cuadraditos de 1 cm². Vas a aprender que el área es cuántos cuadrados caben dentro."
        ),
        "cuerpo_teoria": (
            "Pasos para medir área en malla cuadriculada:\n"
            "1. Cuenta los cuadrados enteros totalmente dentro del contorno.\n"
            "2. Empareja las mitades (medios cuadrados): ½ + ½ = 1 cuadrado entero.\n"
            "3. Suma los enteros más las parejas de mitades para obtener el área total en cm²."
        ),
        "advertencia": (
            "¡Cuidado con los medios! Cada triángulo que corta un cuadrado en diagonal es medio cuadrado (½). Dos mitades hacen un entero."
        ),
        "diccionario": {
            "Área": "Cantidad de unidades cuadradas que caben dentro de una figura.",
            "Unidad cuadrada (cm²)": "Cuadrado de 1 cm por 1 cm usado como patrón de medida.",
            "Medio cuadrado": "Triángulo formado por la diagonal de una celda de la malla (vale ½)."
        },
        "ejemplos": [
            {
                "enunciado": "Rectángulo de 4 × 3 celdas sobre malla. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "3 filas de 4 cuadrados enteros."},
                    {"orden": 2, "texto": "4 + 4 + 4 = 12 cm²."}
                ]
            },
            {
                "enunciado": "Figura con 6 cuadrados enteros y 2 mitades. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "2 mitades = 1 entero."},
                    {"orden": 2, "texto": "6 + 1 = 7 cm²."}
                ]
            },
            {
                "enunciado": "Bandera junina de 8 enteros y 4 mitades. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "4 mitades = 2 enteros."},
                    {"orden": 2, "texto": "8 + 2 = 10 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Sofía contó 6 enteros y 4 mitades y dijo 10 cm². ¿Dónde falló?",
                "pasos": [
                    {"orden": 1, "texto": "Sofía contó cada mitad como un entero."},
                    {"orden": 2, "texto": "4 mitades equivalen a 2 enteros. El área real es 6 + 2 = 8 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Figura A (9 enteros) vs Figura B (8 enteros + 2 mitades). ¿Quién ocupa más espacio?",
                "pasos": [
                    {"orden": 1, "texto": "Figura B: 8 + 1 = 9 cm²."},
                    {"orden": 2, "texto": "Ambas ocupan exactamente lo mismo: 9 cm²."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Malla con 5 × 2 cuadrados enteros. ¿Área?",
                "respuesta": "10",
                "feedback_acierto": "¡Correcto! 5 × 2 = 10 cm².",
                "feedback_error": "Cuenta 5 + 5 = 10."
            },
            {
                "enunciado": "4 cuadrados enteros y 2 mitades. ¿Área?",
                "respuesta": "5",
                "feedback_acierto": "¡Excelente! 4 + 1 = 5 cm².",
                "feedback_error": "2 mitades = 1 entero. Total: 4 + 1 = 5."
            },
            {
                "enunciado": "8 cuadrados enteros y 2 mitades. ¿Área?",
                "respuesta": "9",
                "feedback_acierto": "¡Brillante! 8 + 1 = 9 cm².",
                "feedback_error": "8 + 1 = 9."
            }
        ]
    },

    {
        "modulo_id": 3, "nivel_id": 2, "seccion": 302,
        "titulo": "Área de cuadrado y rectángulo",
        "texto_descubrimiento": (
            "¡Multiplica para hallar la superficie! 📐 En vez de contar cuadradito por cuadradito, "
            "aplicas el atajo rápido: Área del rectángulo = base × altura, y Área del cuadrado = lado × lado."
        ),
        "cuerpo_teoria": (
            "Fórmulas de área de cuadriláteros rectos:\n"
            "1. Rectángulo: Área = base × altura\n"
            "2. Cuadrado: Área = lado × lado (o lado²)\n"
            "3. La unidad resultante siempre se expresa al cuadrado (cm², m², etc.)."
        ),
        "advertencia": (
            "¡No confundas área con perímetro! Perímetro suma los lados del borde; Área multiplica base por altura."
        ),
        "diccionario": {
            "Base": "Lado inferior o de referencia horizontal.",
            "Altura": "Distancia vertical perpendicular a la base.",
            "Área del rectángulo": "base × altura."
        },
        "ejemplos": [
            {
                "enunciado": "Un cuadrado de 5 cm de lado. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "5 × 5 = 25 cm²."}
                ]
            },
            {
                "enunciado": "Un rectángulo de 6 cm de base y 4 cm de altura. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "6 × 4 = 24 cm²."}
                ]
            },
            {
                "enunciado": "Una pantalla de 70 cm por 40 cm. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "70 × 40 = 2800 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Pedro calculó un cuadrado de 4 cm de lado y puso 16 cm. ¿Tiene razón?",
                "pasos": [
                    {"orden": 1, "texto": "4 × 4 = 16, pero la unidad debe ser cm²."},
                    {"orden": 2, "texto": "No tiene razón: son 16 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Cuadrado 5×5 vs Rectángulo 6×3. ¿Cuál cubre más superficie?",
                "pasos": [
                    {"orden": 1, "texto": "Cuadrado = 25 cm². Rectángulo = 18 cm²."},
                    {"orden": 2, "texto": "Cubre más el cuadrado."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Rectángulo 8 cm × 5 cm. ¿Área?",
                "respuesta": "40",
                "feedback_acierto": "¡Correcto! 8 × 5 = 40 cm².",
                "feedback_error": "8 × 5 = 40."
            },
            {
                "enunciado": "Cuadrado de 7 cm de lado. ¿Área?",
                "respuesta": "49",
                "feedback_acierto": "¡Excelente! 7 × 7 = 49 cm².",
                "feedback_error": "7 × 7 = 49."
            },
            {
                "enunciado": "Rectángulo 3,5 cm × 2 cm. ¿Área?",
                "respuesta": "7",
                "feedback_acierto": "¡Brillante! 3,5 × 2 = 7 cm².",
                "feedback_error": "3,5 × 2 = 7."
            }
        ]
    },

    {
        "modulo_id": 3, "nivel_id": 3, "seccion": 303,
        "titulo": "Área del triángulo",
        "texto_descubrimiento": (
            "¡El triángulo es medio rectángulo! 🔺 Todo triángulo es exactamente la mitad del rectángulo que lo contiene. "
            "Por eso su fórmula es: Área = (base × altura) ÷ 2."
        ),
        "cuerpo_teoria": (
            "Pasos para área del triángulo:\n"
            "1. Identifica la base y la altura perpendicular (la que forma ángulo recto de 90°).\n"
            "2. Multiplica base × altura.\n"
            "3. Divide el resultado entre 2."
        ),
        "advertencia": (
            "¡No uses el lado inclinado como altura! La altura debe ser siempre el segmento perpendicular a la base."
        ),
        "diccionario": {
            "Área del triángulo": "(base × altura) ÷ 2.",
            "Altura perpendicular": "Segmento que cae formando 90° sobre la base."
        },
        "ejemplos": [
            {
                "enunciado": "Triángulo de base 6 cm y altura 4 cm. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "(6 × 4) ÷ 2 = 24 ÷ 2 = 12 cm²."}
                ]
            },
            {
                "enunciado": "Triángulo de base 10 cm y altura 3 cm. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "(10 × 3) ÷ 2 = 15 cm²."}
                ]
            },
            {
                "enunciado": "Vela triangular de base 8 m, altura 5 m y lado inclinado 7 m. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "El lado de 7 m es un distractor. (8 × 5) ÷ 2 = 20 m²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Ana hizo 6 × 4 = 24 cm² para un triángulo. ¿Dónde erró?",
                "pasos": [
                    {"orden": 1, "texto": "Olvidó dividir entre 2. El área real es 12 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Triángulo con base 8 cm, altura 3 cm y lado inclinado 5 cm. ¿Qué datos se usan?",
                "pasos": [
                    {"orden": 1, "texto": "Se usan la base (8) y la altura perpendicular (3). El 5 no se usa."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Triángulo base 4 cm, altura 6 cm. ¿Área?",
                "respuesta": "12",
                "feedback_acierto": "¡Correcto! (4 × 6) ÷ 2 = 12 cm².",
                "feedback_error": "(4 × 6) ÷ 2 = 12."
            },
            {
                "enunciado": "Triángulo base 10 cm, altura 4 cm. ¿Área?",
                "respuesta": "20",
                "feedback_acierto": "¡Excelente! (10 × 4) ÷ 2 = 20 cm².",
                "feedback_error": "10 × 4 ÷ 2 = 20."
            },
            {
                "enunciado": "Triángulo base 7 cm, altura 2 cm. ¿Área?",
                "respuesta": "7",
                "feedback_acierto": "¡Brillante! (7 × 2) ÷ 2 = 7 cm².",
                "feedback_error": "7 × 2 ÷ 2 = 7."
            }
        ]
    },

    {
        "modulo_id": 3, "nivel_id": 4, "seccion": 304,
        "titulo": "Paralelogramo, rombo y trapecio",
        "texto_descubrimiento": (
            "¡Tres figuras especiales sin aprender nada de memoria! 🔷 "
            "Paralelogramo (base × altura), Rombo (Diagonal mayor × diagonal menor ÷ 2), Trapecio ((Base mayor + base menor) ÷ 2 × altura)."
        ),
        "cuerpo_teoria": (
            "Fórmulas de figuras especiales:\n"
            "1. Paralelogramo: Área = base × altura perpendicular.\n"
            "2. Rombo: Área = (Diagonal mayor × diagonal menor) ÷ 2.\n"
            "3. Trapecio: Área = [(Base mayor + base menor) ÷ 2] × altura."
        ),
        "advertencia": (
            "En el trapecio se usa el PROMEDIO de las dos bases, no su suma directa sin dividir."
        ),
        "diccionario": {
            "Rombo": "Paralelogramo de 4 lados iguales; área = (D × d) ÷ 2.",
            "Trapecio": "Cuadrilátero con 2 bases paralelas; área = (B + b) ÷ 2 × h."
        },
        "ejemplos": [
            {
                "enunciado": "Paralelogramo de base 8 cm y altura 5 cm. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "8 × 5 = 40 cm²."}
                ]
            },
            {
                "enunciado": "Rombo con diagonales de 10 cm y 6 cm. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "(10 × 6) ÷ 2 = 30 cm²."}
                ]
            },
            {
                "enunciado": "Trapecio: base mayor 10 cm, base menor 6 cm, altura 4 cm. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "(10 + 6) ÷ 2 = 8; 8 × 4 = 32 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Luis hizo 10 × 6 = 60 cm² para un rombo. ¿Qué le faltó?",
                "pasos": [
                    {"orden": 1, "texto": "Le faltó dividir entre 2. El área es 30 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Ema sumó las bases del trapecio (10+6=16) y multiplicó por 4 dando 64. ¿Es correcto?",
                "pasos": [
                    {"orden": 1, "texto": "Faltó promediar las bases dividiendo entre 2. El área real es 32 cm²."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Paralelogramo base 7 cm, altura 4 cm. ¿Área?",
                "respuesta": "28",
                "feedback_acierto": "¡Correcto! 7 × 4 = 28 cm².",
                "feedback_error": "7 × 4 = 28."
            },
            {
                "enunciado": "Rombo diagonales 8 cm y 6 cm. ¿Área?",
                "respuesta": "24",
                "feedback_acierto": "¡Excelente! (8 × 6) ÷ 2 = 24 cm².",
                "feedback_error": "8 × 6 ÷ 2 = 24."
            },
            {
                "enunciado": "Trapecio bases 8 cm y 4 cm, altura 5 cm. ¿Área?",
                "respuesta": "30",
                "feedback_acierto": "¡Brillante! [(8 + 4) ÷ 2] × 5 = 30 cm².",
                "feedback_error": "12 ÷ 2 × 5 = 30."
            }
        ]
    },

    {
        "modulo_id": 3, "nivel_id": 5, "seccion": 305,
        "titulo": "Área del círculo",
        "texto_descubrimiento": (
            "¡El área del círculo! ⭕ Para calcular la superficie interior del círculo "
            "usamos el radio y la constante π ≈ 3,14: **Área = π × radio²**."
        ),
        "cuerpo_teoria": (
            "Fórmula del área del círculo:\n"
            "1. Área = 3,14 × radio × radio (π × r²).\n"
            "2. Si te dan el diámetro, primero divídelo entre 2 para obtener el radio.\n"
            "3. Recuerda: Circunferencia es el borde (2πr); Área es el interior (πr²)."
        ),
        "advertencia": (
            "¡No uses el diámetro directo en la fórmula! El diámetro es el doble del radio. Divide el diámetro entre 2 primero."
        ),
        "diccionario": {
            "Área del círculo": "π × radio² (superficie encerrada por la circunferencia).",
            "Radio": "La mitad del diámetro."
        },
        "ejemplos": [
            {
                "enunciado": "Círculo de radio 5 cm (π = 3,14). ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "5 × 5 = 25; 25 × 3,14 = 78,5 cm²."}
                ]
            },
            {
                "enunciado": "Plato de radio 10 cm. ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "10 × 10 = 100; 100 × 3,14 = 314 cm²."}
                ]
            },
            {
                "enunciado": "Pizza de 30 cm de diámetro (π = 3,14). ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "Radio = 30 ÷ 2 = 15 cm. 15 × 15 = 225; 225 × 3,14 = 706,5 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Tomás hizo 20 × 20 × 3,14 = 1256 para un plato de 20 cm de diámetro. ¿Error?",
                "pasos": [
                    {"orden": 1, "texto": "Usó el diámetro 20 en vez del radio 10. El área real es 314 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Nadia hizo 2 × 3,14 × 5 = 31,4 para un mantel de radio 5 cm. ¿Qué calculó?",
                "pasos": [
                    {"orden": 1, "texto": "Calculó la circunferencia (el borde). El área es 78,5 cm²."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Círculo de radio 2 cm (π = 3,14). ¿Área?",
                "respuesta": "12,56",
                "feedback_acierto": "¡Correcto! 3,14 × 4 = 12,56 cm².",
                "feedback_error": "3,14 × 2 × 2 = 12,56."
            },
            {
                "enunciado": "Círculo de radio 10 cm (π = 3,14). ¿Área?",
                "respuesta": "314",
                "feedback_acierto": "¡Excelente! 3,14 × 100 = 314 cm².",
                "feedback_error": "3,14 × 100 = 314."
            },
            {
                "enunciado": "Círculo de diámetro 12 cm (π = 3,14). ¿Área?",
                "respuesta": "113,04",
                "feedback_acierto": "¡Brillante! Radio = 6. 3,14 × 36 = 113,04 cm².",
                "feedback_error": "Radio = 6. 3,14 × 36 = 113,04."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 4: Áreas Compuestas y Sombreadas (secciones 401, 402, 403)
    # =========================================================================
    {
        "modulo_id": 4, "nivel_id": 1, "seccion": 401,
        "titulo": "Compuestas por suma",
        "texto_descubrimiento": (
            "¡Divide y sumarás! 🧩 Las figuras compuestas en L, T o escaleras no tienen una fórmula directa; "
            "se descomponen en rectángulos o triángulos más simples y se suman sus áreas."
        ),
        "cuerpo_teoria": (
            "Pasos para compuestas por suma:\n"
            "1. Traza líneas imaginarias para partir la figura en rectángulos simples.\n"
            "2. Calcula el área de cada rectángulo por separado.\n"
            "3. Suma las áreas parciales."
        ),
        "advertencia": (
            "No cuentes dos veces el solape ni sumes la línea interna de corte al área."
        ),
        "diccionario": {
            "Descomposición": "Dividir una figura compleja en partes simples conocidas.",
            "Área total": "Suma de las áreas parciales de cada componente."
        },
        "ejemplos": [
            {
                "enunciado": "Figura en L partida en rectángulos de 8×5 y 4×3. ¿Área total?",
                "pasos": [
                    {"orden": 1, "texto": "8 × 5 = 40; 4 × 3 = 12. Total = 40 + 12 = 52 cm²."}
                ]
            },
            {
                "enunciado": "Figura en T: travesaño 6×2 y pie 2×3. ¿Área total?",
                "pasos": [
                    {"orden": 1, "texto": "6 × 2 = 12; 2 × 3 = 6. Total = 12 + 6 = 18 cm²."}
                ]
            },
            {
                "enunciado": "Escalera de 3 escalones de 2×2. ¿Área total?",
                "pasos": [
                    {"orden": 1, "texto": "4 + 4 + 4 = 12 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Marcos hizo 8×5 + 8×3 = 64 para una L de piezas 8×5 y 4×3. ¿Error?",
                "pasos": [
                    {"orden": 1, "texto": "Usó la cota 8 para la segunda pieza en vez de 4. El total es 52 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: ¿Se suma o se resta para hallar el área de un piso en L?",
                "pasos": [
                    {"orden": 1, "texto": "Se suman las piezas; no hay hueco que restar."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "L = rect 6×4 + rect 2×3. ¿Área?",
                "respuesta": "30",
                "feedback_acierto": "¡Correcto! 24 + 6 = 30 cm².",
                "feedback_error": "24 + 6 = 30."
            },
            {
                "enunciado": "T = rect 8×2 + rect 2×4. ¿Área?",
                "respuesta": "24",
                "feedback_acierto": "¡Excelente! 16 + 8 = 24 cm².",
                "feedback_error": "16 + 8 = 24."
            },
            {
                "enunciado": "Dos cuadrados juntos de 3×3. ¿Área?",
                "respuesta": "18",
                "feedback_acierto": "¡Brillante! 9 + 9 = 18 cm².",
                "feedback_error": "9 + 9 = 18."
            }
        ]
    },

    {
        "modulo_id": 4, "nivel_id": 2, "seccion": 402,
        "titulo": "Compuestas por resta",
        "texto_descubrimiento": (
            "¡Resta el hueco! ✂️ Para hallar la superficie de un marco o una placa perforada, "
            "calculamos el área de la figura completa exterior y le restamos el área del hueco interior."
        ),
        "cuerpo_teoria": (
            "Fórmula de compuestas por resta:\n"
            "1. Área sombreada = Área exterior − Área del hueco interior.\n"
            "2. Funciona para marcos, ventanas en paredes y huecos circulares."
        ),
        "advertencia": (
            "¡No sumes el hueco! El hueco es espacio vacío que se quita, por lo que siempre se resta."
        ),
        "diccionario": {
            "Hueco": "Región interior sin material o vacía.",
            "Área sombreada": "Superficie remanente tras restar el hueco."
        },
        "ejemplos": [
            {
                "enunciado": "Marco: cartón de 10×8 cm, hueco de 6×4 cm. ¿Área sombreada?",
                "pasos": [
                    {"orden": 1, "texto": "10 × 8 = 80; 6 × 4 = 24. 80 − 24 = 56 cm²."}
                ]
            },
            {
                "enunciado": "Placa 10×10 cm con hueco circular de radio 3 cm (π = 3,14). ¿Área?",
                "pasos": [
                    {"orden": 1, "texto": "100 − (3,14 × 9) = 100 − 28,26 = 71,74 cm²."}
                ]
            },
            {
                "enunciado": "Pared 12×9 m con ventana de 4×3 m. ¿Pared cubierta?",
                "pasos": [
                    {"orden": 1, "texto": "108 − 12 = 96 m²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Lucía sumó 80 + 24 = 104 para un marco de 10×8 con hueco 6×4. ¿Error?",
                "pasos": [
                    {"orden": 1, "texto": "El hueco se resta: 80 − 24 = 56 cm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Placa 10×10 con hueco circular de diámetro 6. Nico usó d=6 en la fórmula. ¿Error?",
                "pasos": [
                    {"orden": 1, "texto": "Debió usar radio r = 3. 100 − 28,26 = 71,74 cm²."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Marco 8×6, hueco 4×2. ¿Área?",
                "respuesta": "40",
                "feedback_acierto": "¡Correcto! 48 − 8 = 40 cm².",
                "feedback_error": "48 − 8 = 40."
            },
            {
                "enunciado": "Placa 10×10, hueco circular radio 2 (π = 3,14). ¿Área?",
                "respuesta": "87,44",
                "feedback_acierto": "¡Excelente! 100 − 12,56 = 87,44 cm².",
                "feedback_error": "100 − 12,56 = 87,44."
            },
            {
                "enunciado": "Rectángulo 9×5, hueco 3×3. ¿Área?",
                "respuesta": "36",
                "feedback_acierto": "¡Brillante! 45 − 9 = 36 cm².",
                "feedback_error": "45 − 9 = 36."
            }
        ]
    },

    {
        "modulo_id": 4, "nivel_id": 3, "seccion": 403,
        "titulo": "Inscritas y sombreadas",
        "texto_descubrimiento": (
            "¡Halla lo que queda entre dos figuras! 🎯 Cuando una figura está metida dentro de otra "
            "(como un círculo en un cuadrado), identificamos qué región está sombreada para calcular exactamente su área."
        ),
        "cuerpo_teoria": (
            "Pasos para figuras inscritas:\n"
            "1. Calcula el área de la figura exterior y de la figura interior.\n"
            "2. Si la región sombreada es el borde exterior: Resta Exterior − Interior.\n"
            "3. Si la región sombreada es el objeto interior: El área es directamente el objeto interior."
        ),
        "advertencia": (
            "Lee bien qué parte está pintada antes de decidir si restas o no."
        ),
        "diccionario": {
            "Figura inscrita": "Figura dibujada dentro de los límites de otra.",
            "Región sombreada": "Zona pintada que exige el problema."
        },
        "ejemplos": [
            {
                "enunciado": "Cuadrado de 10 cm con círculo inscrito de radio 5 cm (π = 3,14). Esquinas sombreadas.",
                "pasos": [
                    {"orden": 1, "texto": "100 − 78,5 = 21,5 cm²."}
                ]
            },
            {
                "enunciado": "Rectángulo 8×6 con triángulo inscrito (base 8, altura 6) sin pintar. Área sombreada afuera.",
                "pasos": [
                    {"orden": 1, "texto": "48 − 24 = 24 cm²."}
                ]
            },
            {
                "enunciado": "Jardín 12×12 m con estanque circular de radio 4 m (π = 3,14). Césped alrededor.",
                "pasos": [
                    {"orden": 1, "texto": "144 − 50,24 = 93,76 m²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: En cuadrado de 10 cm con círculo inscrito de radio 5, Sara pintó el CÍRCULO y dio 21,5 cm². ¿Error?",
                "pasos": [
                    {"orden": 1, "texto": "El círculo sombreado mide 78,5 cm². 21,5 es el área de las esquinas no pintadas."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Patio 10×8 con pileta de radio 2 (π = 3,14) y reposera de 1 m². ¿Piso libre de pileta?",
                "pasos": [
                    {"orden": 1, "texto": "80 − 12,56 = 67,44 m². La reposera es dato irrelevante."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Cuadrado 8 cm con círculo inscrito radio 4 (π = 3,14). Esquinas sombreadas.",
                "respuesta": "13,76",
                "feedback_acierto": "¡Correcto! 64 − 50,24 = 13,76 cm².",
                "feedback_error": "64 − 50,24 = 13,76."
            },
            {
                "enunciado": "Rectángulo 10×6 con triángulo inscrito base 10 altura 6 sin pintar. Área afuera.",
                "respuesta": "30",
                "feedback_acierto": "¡Excelente! 60 − 30 = 30 cm².",
                "feedback_error": "60 − 30 = 30."
            },
            {
                "enunciado": "Cuadrado 6 m con estanque circular radio 2 (π = 3,14). Césped.",
                "respuesta": "23,44",
                "feedback_acierto": "¡Brillante! 36 − 12,56 = 23,44 m².",
                "feedback_error": "36 − 12,56 = 23,44."
            }
        ]
    }
]
