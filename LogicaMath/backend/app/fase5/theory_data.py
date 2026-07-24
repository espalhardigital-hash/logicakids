"""
Guión pedagógico de teoría para los 15 niveles de la Fase 5 (Operatoria Decimal y Conversiones).
Cumple con las Secciones 5 y 6 de docs/reestructuraciondefases.md.

Contiene:
  - 15 niveles en niveles_teoria_pool (3 por módulo, M1 a M5).
  - 5 ejemplos guiados por nivel (los 2 últimos son TJS resueltos paso a paso).
  - 3 interactivos de evocación por nivel (cálculo directo).
  - Diccionario pedagógico y trampas advertencia.
"""

from app.utils.svg_figuras import (
    escalera_unidades, tabla_datos, comparador_opciones, color_modulo
)

FASE5_TEORIA_DATA = [
    # =========================================================================
    # MÓDULO 1: Suma y Resta de Decimales (secciones 101, 102, 103)
    # =========================================================================
    {
        "modulo_id": 1, "nivel_id": 1, "seccion": 101,
        "titulo": "Suma alineando la coma",
        "texto_descubrimiento": (
            "¡Bienvenida, guardiana de las comas! 🪙 Hoy despiertas tu primer superpoder de la Fase de los Decimales: "
            "el Alineador de Comas. Cada vez que dos cantidades de dinero se juntan, sus comas decimales deben mirarse cara a cara, "
            "en la misma columna, como soldaditos formados en fila. Si una coma se desalinea aunque sea un paso, todo el ejército "
            "de números se desordena y el resultado sale mal. Tu misión: alinear siempre por la coma, nunca por el borde derecho de los números."
        ),
        "cuerpo_teoria": (
            "Para sumar números decimales correctamente:\n"
            "1. Alinea los números en columna haciendo coincidir las comas verticales.\n"
            "2. Si un número tiene menos cifras decimales que otro, completa con ceros a la derecha (por ejemplo, 5,3 pasa a 5,30).\n"
            "3. Suma columna por columna de derecha a izquierda (centésimas, décimas, unidades, decenas), llevando el acarreo cuando una columna pase de 9.\n"
            "4. Coloca la coma decimal en el resultado exactamente debajo de la columna de las comas."
        ),
        "advertencia": (
            "¡Atención, alineadora! Si sumas 2,7 + 1,45 sin igualar antes las cifras decimales, tu cerebro puede tentarte a sumar 7 + 45 "
            "como si fueran del mismo tamaño, y eso te da un resultado falso. Antes de sumar, revisa: ¿los dos números tienen la misma cantidad "
            "de cifras después de la coma? Si no, completa con un cero a la derecha del que tiene menos. Recién ahí alinea las comas y suma."
        ),
        "diccionario": {
            "Número decimal": "Número que tiene parte entera y parte decimal separadas por una coma (ej. 3,25).",
            "Coma decimal": "Signo que separa la parte entera de las décimas y centésimas.",
            "Décimas": "Primera cifra a la derecha de la coma (partes de 10).",
            "Centésimas": "Segunda cifra a la derecha de la coma (partes de 100).",
            "Alinear": "Colocar los números uno debajo del otro con sus comas en la misma línea vertical.",
            "Completar con cero": "Agregar un cero a la derecha de la parte decimal (5,3 = 5,30) sin alterar su valor."
        },
        "ejemplos": [
            {
                "enunciado": "Mía compra un chicle a R$ 3,25 y un caramelo a R$ 1,40. ¿Cuánto pagó en total?",
                "pasos": [
                    {"orden": 1, "texto": "Alineamos por la coma: 3,25 + 1,40."},
                    {"orden": 2, "texto": "Sumamos centésimas: 5+0=5. Décimas: 2+4=6. Unidades: 3+1=4."},
                    {"orden": 3, "texto": "Resultado final: R$ 4,65."}
                ]
            },
            {
                "enunciado": "Hugo ahorra R$ 5,30 el lunes y R$ 2,45 el martes. ¿Cuánto ahorró en total?",
                "pasos": [
                    {"orden": 1, "texto": "Completamos 5,3 como 5,30 para igualar decimales."},
                    {"orden": 2, "texto": "Alineamos: 5,30 + 2,45."},
                    {"orden": 3, "texto": "Sumamos centésimas (0+5=5), décimas (3+4=7) y unidades (5+2=7). Resultado: R$ 7,75."}
                ]
            },
            {
                "enunciado": "Leo compra tres útiles: R$ 1,20, R$ 0,75 y R$ 2,05. ¿Cuánto gastó en total?",
                "pasos": [
                    {"orden": 1, "texto": "Alineamos los tres números por la coma: 1,20 + 0,75 + 2,05."},
                    {"orden": 2, "texto": "Centésimas: 0+5+5=10 (escribo 0, llevo 1). Décimas: 2+7+0+1=10 (escribo 0, llevo 1). Unidades: 1+0+2+1=4."},
                    {"orden": 3, "texto": "Resultado final: R$ 4,00."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Bruno suma 2,70 + 1,45 sin alinear y dice 3,52. Ana dice que es 4,15. ¿Quién tiene razón?",
                "pasos": [
                    {"orden": 1, "texto": "Situación: Bruno desalineó la coma sumando 7+45 por la derecha."},
                    {"orden": 2, "texto": "Resolución: alineamos 2,70 + 1,45. Centésimas 0+5=5; décimas 7+4=11 (escribo 1, llevo 1); unidades 2+1+1=4."},
                    {"orden": 3, "texto": "Ana tiene razón: R$ 4,15. Bruno cometió la confusión DESALINEACION_COMA."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Nina debe sumar 6,4 + 2,35 + 0,8. ¿Cuál es el primer paso correcto?",
                "pasos": [
                    {"orden": 1, "texto": "Situación: decidir cómo preparar los sumandos antes de calcular."},
                    {"orden": 2, "texto": "Paso correcto: completar 6,4 a 6,40 y 0,8 a 0,80 para igualar decimales."},
                    {"orden": 3, "texto": "Alineamos 6,40 + 2,35 + 0,80 = 9,55."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Zoe compra una carpeta a R$ 2,15 y un cuaderno a R$ 3,60. ¿Cuánto pagó en total?",
                "respuesta": "5,75",
                "feedback_acierto": "¡Correcto! Alineaste la coma: 2,15 + 3,60 = 5,75.",
                "feedback_error": "Alinea las comas antes de sumar: 2,15 + 3,60."
            },
            {
                "enunciado": "Dante ahorra R$ 4,80 el sábado y R$ 1,25 el domingo. ¿Cuánto ahorró en total?",
                "respuesta": "6,05",
                "feedback_acierto": "¡Excelente! 4,80 + 1,25 = 6,05.",
                "feedback_error": "Completa 4,8 con cero (4,80) y suma 1,25."
            },
            {
                "enunciado": "Iker compra tres estampillas: R$ 0,45, R$ 0,30 y R$ 0,25. ¿Cuánto gastó en total?",
                "respuesta": "1,00",
                "feedback_acierto": "¡Brillante! 0,45 + 0,30 + 0,25 = 1,00.",
                "feedback_error": "Suma las centésimas llevando acarreo cuando pase de 9."
            }
        ]
    },

    {
        "modulo_id": 1, "nivel_id": 2, "seccion": 102,
        "titulo": "Resta con completado de ceros",
        "texto_descubrimiento": (
            "¡Ahora despiertas tu segundo superpoder! 🕵️‍♀️ Eres la Completadora de Ceros. A veces un número decimal parece tener menos "
            "cifras que otro, pero en realidad esconde ceros invisibles que hay que revelar antes de restar. 8 es lo mismo que 8,00, y 5,4 es lo mismo "
            "que 5,40. Si no revelas esos ceros antes de restar, tu resultado sale mal aunque hayas restado perfecto los dígitos que sí veías."
        ),
        "cuerpo_teoria": (
            "Para restar números decimales:\n"
            "1. Completa con ceros a la derecha del minuendo o sustraendo si tienen diferente cantidad de cifras decimales.\n"
            "2. Alinea verticalmente las comas.\n"
            "3. Resta de derecha a izquierda. Si el dígito superior es menor que el inferior, pide prestado 1 a la columna izquierda.\n"
            "4. Coloca la coma decimal en el resultado alineada con los números superiores."
        ),
        "advertencia": (
            "¡Atención, completadora! Si en 6,4 − 2,75 dejas la columna de las centésimas del 6,4 vacía en vez de escribir su cero escondido (6,40), "
            "tu resta va a salir mal. Antes de restar SIEMPRE completa con ceros el número que tenga menos cifras decimales."
        ),
        "diccionario": {
            "Minuendo": "Número del que se resta (cantidad inicial).",
            "Sustraendo": "Número que se resta (cantidad gastada o quitada).",
            "Diferencia": "Resultado de una resta.",
            "Préstamo": "Tomar 1 unidad de la columna izquierda cuando el dígito superior es menor."
        },
        "ejemplos": [
            {
                "enunciado": "Bruno tiene R$ 8,00 ahorrados y compra un cuaderno de R$ 3,45. ¿Cuánto dinero le queda?",
                "pasos": [
                    {"orden": 1, "texto": "Alineamos 8,00 − 3,45."},
                    {"orden": 2, "texto": "Centésimas: 0−5 (pedimos prestado). 10−5=5. Décimas: 9−4=5. Unidades: 7−3=4."},
                    {"orden": 3, "texto": "Resultado: R$ 4,55."}
                ]
            },
            {
                "enunciado": "Salma tiene R$ 6,40 y regala R$ 2,75. ¿Cuánto le queda?",
                "pasos": [
                    {"orden": 1, "texto": "Completamos 6,4 como 6,40."},
                    {"orden": 2, "texto": "Alineamos 6,40 − 2,75 y restamos con préstamo en décimas y unidades."},
                    {"orden": 3, "texto": "Resultado: R$ 3,65."}
                ]
            },
            {
                "enunciado": "Dante paga con un billete de R$ 20,00 un boleto de R$ 12,50. ¿Cuánto vuelto recibe?",
                "pasos": [
                    {"orden": 1, "texto": "Completamos 20 como 20,00."},
                    {"orden": 2, "texto": "20,00 − 12,50 = 7,50."},
                    {"orden": 3, "texto": "Resultado: R$ 7,50."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Owen resto 9,3 − 4,25 y escribió 5,08 por no completar el cero de 9,3. Lía dice 5,05. ¿Quién acertó?",
                "pasos": [
                    {"orden": 1, "texto": "Situación: Owen cometió CERO_OMITIDO al dejar vacía la columna centésimas."},
                    {"orden": 2, "texto": "Resolución: 9,30 − 4,25. Centésimas 10−5=5; décimas 2−2=0; unidades 9−4=5."},
                    {"orden": 3, "texto": "Lía tiene razón: R$ 5,05."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Nina debe resolver 15 − 6,8. ¿Cuál es el primer paso correcto?",
                "pasos": [
                    {"orden": 1, "texto": "Situación: el minuendo 15 es un número entero."},
                    {"orden": 2, "texto": "Primer paso: escribir 15 como 15,0 para igualar decimales."},
                    {"orden": 3, "texto": "Calculamos 15,0 − 6,8 = R$ 8,20."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Iker tiene R$ 7,00 y gasta R$ 2,35 en un helado. ¿Cuánto le queda?",
                "respuesta": "4,65",
                "feedback_acierto": "¡Correcto! 7,00 − 2,35 = 4,65.",
                "feedback_error": "Completa 7 como 7,00 antes de restar."
            },
            {
                "enunciado": "Zoe tenía R$ 5,60 y presta R$ 1,85. ¿Cuánto le queda?",
                "respuesta": "3,75",
                "feedback_acierto": "¡Excelente! 5,60 − 1,85 = 3,75.",
                "feedback_error": "Completa 5,6 como 5,60 y resta pidiendo prestado."
            },
            {
                "enunciado": "Emma paga con R$ 10,00 una merienda de R$ 4,25. ¿Cuánto vuelto recibe?",
                "respuesta": "5,75",
                "feedback_acierto": "¡Brillante! 10,00 − 4,25 = 5,75.",
                "feedback_error": "Escribe 10 como 10,00 y resta."
            }
        ]
    },

    {
        "modulo_id": 1, "nivel_id": 3, "seccion": 103,
        "titulo": "Combinadas en contexto",
        "texto_descubrimiento": (
            "¡Tu tercer superpoder te convierte en Detective de Dos Pistas! 🔍 Algunos problemas esconden dos operaciones, y hasta un dato "
            "falso que no sirve para nada. Un buen detective no calcula apenas ve un número: primero lee la pregunta final, decide qué datos sirven "
            "y en qué orden debe combinarlos, y recién ahí calcula."
        ),
        "cuerpo_teoria": (
            "Para resolver problemas combinados en contexto:\n"
            "1. Lee detenidamente la última oración (la pregunta final).\n"
            "2. Identifica los datos necesarios y descarta los datos irrelevantes.\n"
            "3. Agrupa las cantidades del mismo tipo (por ejemplo, suma todos los gastos primero).\n"
            "4. Aplica las restas necesarias respecto al monto inicial o dinero entregado."
        ),
        "advertencia": (
            "¡Cuidado, detective! No calcules apenas veas un número. Si un precio o un detalle no tiene relación con lo que se pregunta, déjalo de lado. "
            "Y antes de operar, decide: ¿qué hay que juntar primero y qué hay que restar al final?"
        ),
        "diccionario": {
            "Operación combinada": "Problema que requiere encadenar suma y resta.",
            "Dato irrelevante": "Dato numérico o descriptivo del enunciado que no se utiliza para responder.",
            "Total parcial": "Resultado intermedio (ej. suma de gastos) necesario antes del resultado final."
        },
        "ejemplos": [
            {
                "enunciado": "Hugo tiene R$ 10,00. Compra un jugo de R$ 2,35 y un pan de R$ 1,50. ¿Cuánto dinero le queda?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos los dos gastos: 2,35 + 1,50 = 3,85."},
                    {"orden": 2, "texto": "Restamos del total inicial: 10,00 − 3,85 = 6,15."},
                    {"orden": 3, "texto": "Le quedan R$ 6,15."}
                ]
            },
            {
                "enunciado": "Alba ahorró R$ 4,20 el lunes y R$ 3,75 el martes. El miércoles gastó R$ 2,90. ¿Cuánto tiene ahora?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos ahorros: 4,20 + 3,75 = 7,95."},
                    {"orden": 2, "texto": "Restamos gasto: 7,95 − 2,90 = 5,05."},
                    {"orden": 3, "texto": "Tiene R$ 5,05."}
                ]
            },
            {
                "enunciado": "Bruno compra una mochila roja de R$ 18,50 y una cartuchera de R$ 4,25. Paga con R$ 25,00. ¿Cuánto vuelto recibe?",
                "pasos": [
                    {"orden": 1, "texto": "El color 'roja' es un dato no numérico irrelevante. Gastos: 18,50 + 4,25 = 22,75."},
                    {"orden": 2, "texto": "Vuelto: 25,00 − 22,75 = 2,25."},
                    {"orden": 3, "texto": "Recibe R$ 2,25."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Nina compró manzanas por R$ 3,40 y peras por R$ 2,15. Vio duraznos a R$ 1,80 pero no compró. ¿Cuánto gastó?",
                "pasos": [
                    {"orden": 1, "texto": "Situación: identificar el dato irrelevante (los duraznos no comprados)."},
                    {"orden": 2, "texto": "Resolución: sumamos solo lo comprado: 3,40 + 2,15 = 5,55."},
                    {"orden": 3, "texto": "Gastó R$ 5,55. El precio de los duraznos no se utiliza."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Iker ahorra R$ 5,00, gasta R$ 2,30 en el cine y recibe R$ 1,50 de regalo. ¿Cuál es el orden de cálculo?",
                "pasos": [
                    {"orden": 1, "texto": "Situación: decidir el orden de suma y resta."},
                    {"orden": 2, "texto": "Procedimiento: restar el gasto al ahorro inicial (5,00 − 2,30 = 2,70) y sumar el regalo (2,70 + 1,50 = 4,20)."},
                    {"orden": 3, "texto": "Resultado: R$ 4,20."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Dante tiene R$ 8,00. Gasta R$ 3,15 en un cómic y R$ 1,40 en un jugo. ¿Cuánto le queda?",
                "respuesta": "3,45",
                "feedback_acierto": "¡Correcto! 8,00 − (3,15 + 1,40) = 3,45.",
                "feedback_error": "Suma primero los dos gastos y réstalos de 8,00."
            },
            {
                "enunciado": "Mía ahorró R$ 6,50 y R$ 2,25. Luego gastó R$ 4,00. ¿Cuánto le queda?",
                "respuesta": "4,75",
                "feedback_acierto": "¡Excelente! (6,50 + 2,25) − 4,00 = 4,75.",
                "feedback_error": "Suma los dos ahorros y resta el gasto."
            },
            {
                "enunciado": "Leo compra 2 cuadernos de R$ 2,10 cada uno y paga con R$ 5,00. ¿Cuánto vuelto recibe?",
                "respuesta": "0,80",
                "feedback_acierto": "¡Brillante! 2,10 + 2,10 = 4,20; 5,00 − 4,20 = 0,80.",
                "feedback_error": "Suma los dos cuadernos (4,20) y resta de 5,00."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 2: Multiplicación y División de Decimales (secciones 201, 202, 203)
    # =========================================================================
    {
        "modulo_id": 2, "nivel_id": 1, "seccion": 201,
        "titulo": "Multiplicación con conteo de posiciones",
        "texto_descubrimiento": (
            "¡Bienvenido al Módulo de Multiplicación y División! ✖️ Hoy activas el <span class=\"keyword-highlight\">Contador de Cifras Decimales</span>. "
            "Para multiplicar un número decimal por un entero, primero multiplicas los dígitos como si no hubiera coma. Al final, cuentas cuántos decimales "
            "tenía el factor original y colocas la coma en el resultado contando la misma cantidad de lugares desde la derecha."
        ),
        "cuerpo_teoria": (
            "Reglas para multiplicar decimales:\n"
            "1. Multiplica los números ignorando la coma como si fuesen enteros.\n"
            "2. Cuenta la cantidad total de cifras decimales que hay en los factores.\n"
            "3. En el producto final, cuenta de derecha a izquierda esa misma cantidad de cifras y coloca la coma."
        ),
        "advertencia": (
            "¡Ojo con la coma! No intentes adivinar la posición de la coma durante la multiplicación. Haz la multiplicación de enteros completa "
            "y recién en la última línea coloca la coma contando lugares desde la derecha."
        ),
        "diccionario": {
            "Factor decimal": "Número con coma que se multiplica.",
            "Producto": "Resultado de la multiplicación.",
            "Posiciones decimales": "Cantidad de dígitos ubicados a la derecha de la coma."
        },
        "ejemplos": [
            {
                "enunciado": "Cada bala de caramelo cuesta R$ 0,25. Si Thiago compra 6 balas, ¿cuánto paga?",
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos enteros: 25 × 6 = 150."},
                    {"orden": 2, "texto": "0,25 tiene 2 cifras decimales."},
                    {"orden": 3, "texto": "Contamos 2 lugares desde la derecha: 1,50. Paga R$ 1,50."}
                ]
            },
            {
                "enunciado": "Un kilo de queso cuesta R$ 6,80. La familia compra 3 kilos. ¿Cuánto pagan?",
                "pasos": [
                    {"orden": 1, "texto": "680 × 3 = 2040."},
                    {"orden": 2, "texto": "6,80 tiene 2 decimales."},
                    {"orden": 3, "texto": "Ubicamos la coma: R$ 20,40."}
                ]
            },
            {
                "enunciado": "Una hora de estacionamiento cuesta R$ 2,15. Si se estaciona 5 horas, ¿cuánto paga?",
                "pasos": [
                    {"orden": 1, "texto": "215 × 5 = 1075."},
                    {"orden": 2, "texto": "2,15 tiene 2 decimales → R$ 10,75."},
                    {"orden": 3, "texto": "Resultado: R$ 10,75."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Salma multiplica 4,25 × 6 y coloca la coma obteniendo 255,0 por error. ¿Dónde falló?",
                "pasos": [
                    {"orden": 1, "texto": "425 × 6 = 2550."},
                    {"orden": 2, "texto": "4,25 tiene 2 decimales, por lo que se deben contar 2 lugares desde la derecha."},
                    {"orden": 3, "texto": "El resultado correcto es R$ 25,50, no 255,0 (confusión CONTEO_DECIMALES_ERRADO)."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Para calcular 15 unidades a R$ 2,40 cada una, ¿cuál es el procedimiento correcto?",
                "pasos": [
                    {"orden": 1, "texto": "Multiplicar 240 × 15 = 3600."},
                    {"orden": 2, "texto": "Contar 2 cifras decimales desde la derecha: 36,00."},
                    {"orden": 3, "texto": "Costo total: R$ 36,00."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Cada lápiz cuesta R$ 1,20. ¿Cuánto cuestan 5 lápices?",
                "respuesta": "6,00",
                "feedback_acierto": "¡Correcto! 120 × 5 = 600 → R$ 6,00.",
                "feedback_error": "Multiplica 120 por 5 y coloca la coma a 2 lugares."
            },
            {
                "enunciado": "Cada copia cuesta R$ 0,15. ¿Cuánto cuestan 8 copias?",
                "respuesta": "1,20",
                "feedback_acierto": "¡Excelente! 15 × 8 = 120 → R$ 1,20.",
                "feedback_error": "15 × 8 = 120, con 2 decimales es 1,20."
            },
            {
                "enunciado": "El kilo de manzanas cuesta R$ 4,80. ¿Cuánto cuestan 2 kilos?",
                "respuesta": "9,60",
                "feedback_acierto": "¡Brillante! 4,80 × 2 = 9,60.",
                "feedback_error": "480 × 2 = 960 → R$ 9,60."
            }
        ]
    },

    {
        "modulo_id": 2, "nivel_id": 2, "seccion": 202,
        "titulo": "División con desplazamiento de la coma",
        "texto_descubrimiento": (
            "¡Desbloqueas el poder del <span class=\"keyword-highlight\">Desplazador de Coma</span>! ➗ Dividir entre 10, 100 o 1000 es súper fácil: "
            "la coma camina hacia la izquierda tantas posiciones como ceros tenga el divisor (1 lugar para 10, 2 para 100, 3 para 1000). Y para repartir "
            "un monto decimal entre personas, divides normalmente y colocas la coma en el cociente al bajar la primera cifra decimal."
        ),
        "cuerpo_teoria": (
            "Para dividir números decimales:\n"
            "1. Entre 10, 100, 1000: mueve la coma hacia la izquierda 1, 2 o 3 lugares.\n"
            "2. Reparto entre entero: divide la parte entera; pon la coma en el cociente justo antes de bajar la cifra de las décimas.\n"
            "3. Si la división no se detiene, agrega ceros al resto para continuar dividiendo."
        ),
        "advertencia": (
            "¡No muevas la coma para la derecha al dividir! Multiplicar agranda el número (coma a la derecha); dividir achica el número (coma a la izquierda)."
        ),
        "diccionario": {
            "Dividendo": "Cantidad total a dividir.",
            "Divisor": "Número de partes en que se reparte.",
            "Cociente": "Resultado de la división."
        },
        "ejemplos": [
            {
                "enunciado": "Tres amigos reparten una cuenta de R$ 13,50 en partes iguales. ¿Cuánto paga cada uno?",
                "pasos": [
                    {"orden": 1, "texto": "Dividimos 13,50 entre 3."},
                    {"orden": 2, "texto": "13 ÷ 3 = 4 (resto 1). Ponemos la coma en el cociente (4,)."},
                    {"orden": 3, "texto": "Bajamos el 5: 15 ÷ 3 = 5. Resultado: R$ 4,50 cada uno."}
                ]
            },
            {
                "enunciado": "Un paquete de 5 chicles cuesta R$ 3,75. ¿Cuánto cuesta cada chicle?",
                "pasos": [
                    {"orden": 1, "texto": "Dividimos 3,75 ÷ 5."},
                    {"orden": 2, "texto": "3 ÷ 5 = 0, escribimos 0, en el cociente."},
                    {"orden": 3, "texto": "37 ÷ 5 = 7 (resto 2); 25 ÷ 5 = 5. Cada chicle cuesta R$ 0,75."}
                ]
            },
            {
                "enunciado": "Un premio de R$ 45,00 se reparte entre 6 ganadores. ¿Cuánto recibe cada uno?",
                "pasos": [
                    {"orden": 1, "texto": "45 ÷ 6 = 7 (resto 3)."},
                    {"orden": 2, "texto": "Colocamos coma y agregamos cero al resto: 30 ÷ 6 = 5."},
                    {"orden": 3, "texto": "Cada uno recibe R$ 7,50."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Hugo dividió 27,5 entre 100 y obtuvo 2750. ¿Cuál fue su error?",
                "pasos": [
                    {"orden": 1, "texto": "Hugo movió la coma a la derecha en lugar de la izquierda."},
                    {"orden": 2, "texto": "Al dividir por 100, el número se achica: la coma debe correr 2 lugares a la izquierda."},
                    {"orden": 3, "texto": "Resultado correcto: 0,275 (confusión DESPLAZAMIENTO_DIRECCION_ERRADA)."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Salma afirma que 8 metros de tela por R$ 36,00 significa R$ 288,00 el metro. ¿Es correcto?",
                "pasos": [
                    {"orden": 1, "texto": "Salma multiplicó 36 × 8 en lugar de dividir."},
                    {"orden": 2, "texto": "Para obtener el costo unitario hay que dividir: 36,00 ÷ 8 = 4,50."},
                    {"orden": 3, "texto": "Salma está equivocada; el metro cuesta R$ 4,50."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Dividir 24,00 entre 4 hermanos. ¿Cuánto le toca a cada uno?",
                "respuesta": "6,00",
                "feedback_acierto": "¡Correcto! 24,00 ÷ 4 = 6,00.",
                "feedback_error": "24 ÷ 4 = 6 → R$ 6,00."
            },
            {
                "enunciado": "Calcula 45,0 ÷ 10.",
                "respuesta": "4,5",
                "feedback_acierto": "¡Excelente! Corre la coma 1 lugar a la izquierda: 4,5.",
                "feedback_error": "Dividir entre 10 mueve la coma 1 lugar a la izquierda."
            },
            {
                "enunciado": "Una caja de 12 jugos cuesta R$ 36,00. ¿Cuánto cuesta 1 jugo?",
                "respuesta": "3,00",
                "feedback_acierto": "¡Brillante! 36,00 ÷ 12 = 3,00.",
                "feedback_error": "36 ÷ 12 = 3 → R$ 3,00."
            }
        ]
    },

    {
        "modulo_id": 2, "nivel_id": 3, "seccion": 203,
        "titulo": "Repartición y costo unitario",
        "texto_descubrimiento": (
            "¡Bienvenido al nivel de Juicio de Costos! 🛒 Aquí decides si la situación exige multiplicar (para saber el COSTO TOTAL de varias cosas) "
            "o dividir (para saber el PRECIO UNITARIO de una sola cosa o repartir). El secreto está en responder: ¿busco el precio de UNA parte o de TODAS juntas?"
        ),
        "cuerpo_teoria": (
            "Guía de decisión en problemas de multiplicación/división:\n"
            "1. Si conoces el precio de una unidad y quieres el TOTAL de varias → MULTIPLICA.\n"
            "2. Si conoces el total y quieres el valor de UNA unidad (o repartir en partes iguales) → DIVIDE.\n"
            "3. En problemas de varios pasos, resuelve primero el total parcial antes de repartir."
        ),
        "advertencia": (
            "¡No te dejes engañar por las palabras! Decir 'cada uno' a veces pide multiplicar (si te dan el unitario) y a veces pide dividir (si te piden hallarlo)."
        ),
        "diccionario": {
            "Costo unitario": "Precio de un solo objeto o kilo.",
            "Costo total": "Precio acumulado de todas las unidades.",
            "Reparto equitativo": "Dividir una cantidad en partes exactamente iguales."
        },
        "ejemplos": [
            {
                "enunciado": "Una escuela compra 12 sillas por R$ 324,00. Compró también 4 mesas a R$ 58,50 cada una. ¿Cuánto cuesta UNA silla?",
                "pasos": [
                    {"orden": 1, "texto": "Identificamos el dato relevante: R$ 324,00 por 12 sillas. Las mesas son un dato irrelevante."},
                    {"orden": 2, "texto": "Dividimos total ÷ cantidad: 324,00 ÷ 12 = 27,00."},
                    {"orden": 3, "texto": "Una silla cuesta R$ 27,00."}
                ]
            },
            {
                "enunciado": "Emma gana R$ 9,50 por hora. Trabajó 6 horas la primera semana y 8 horas la segunda. Le descuentan R$ 4,00 de transporte. ¿Cuánto le queda?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos horas trabajadas: 6 + 8 = 14 horas."},
                    {"orden": 2, "texto": "Ganancia bruta: 14 × 9,50 = 133,00."},
                    {"orden": 3, "texto": "Restamos descuento: 133,00 − 4,00 = R$ 129,00."}
                ]
            },
            {
                "enunciado": "Un mayorista vende 12 jugos por R$ 39,00. ¿Cuál es el precio unitario de cada jugo?",
                "pasos": [
                    {"orden": 1, "texto": "Dividimos R$ 39,00 ÷ 12 = 3,25."},
                    {"orden": 2, "texto": "Cada jugo cuesta R$ 3,25."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Niñera a R$ 8,50/hora trabajó 3 horas el lunes. No informan horas del martes. ¿Alcanzan los datos para el total de 2 días?",
                "pasos": [
                    {"orden": 1, "texto": "Situación: falta la cantidad de horas del martes."},
                    {"orden": 2, "texto": "No se puede calcular sin ese dato."},
                    {"orden": 3, "texto": "Decisión correcta: No alcanzan los datos."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Kermés recauda R$ 540,00 con 6 puestos. Tuvo R$ 45,00 de decoración y 12 voluntarios. ¿Cuánto recaudó en promedio cada puesto?",
                "pasos": [
                    {"orden": 1, "texto": "Datos relevantes: R$ 540,00 recaudación y 6 puestos. Decoración y voluntarios son datos irrelevantes."},
                    {"orden": 2, "texto": "Promedio por puesto: 540,00 ÷ 6 = 90,00."},
                    {"orden": 3, "texto": "Cada puesto recaudó R$ 90,00."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Se compran 5 cuadernos por R$ 36,25 en total. ¿Cuánto cuesta 1 cuaderno?",
                "respuesta": "7,25",
                "feedback_acierto": "¡Correcto! 36,25 ÷ 5 = 7,25.",
                "feedback_error": "Divide 36,25 entre 5."
            },
            {
                "enunciado": "Un cine vende 4 entradas a R$ 18,50 cada una. ¿Cuánto recauda en total?",
                "respuesta": "74,00",
                "feedback_acierto": "¡Excelente! 18,50 × 4 = 74,00.",
                "feedback_error": "Multiplica 18,50 por 4."
            },
            {
                "enunciado": "Un sueldo de R$ 240,00 se reparte entre 5 mozos. ¿Cuánto recibe cada uno?",
                "respuesta": "48,00",
                "feedback_acierto": "¡Brillante! 240,00 ÷ 5 = 48,00.",
                "feedback_error": "Divide 240 entre 5."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 3: Medidas de Longitud (secciones 301, 302, 303)
    # =========================================================================
    {
        "modulo_id": 3, "nivel_id": 1, "seccion": 301,
        "titulo": "Escalera métrica lineal",
        "texto_descubrimiento": (
            "¡Bienvenido a la Escalera Métrica Lineal! 📏 En este módulo mides estaturas, lápices y tramos de ruta. "
            "Las unidades de longitud son: milímetro (mm), centímetro (cm), decímetro (dm), metro (m) y kilómetro (km). "
            "Cada peldaño que bajas hacia una unidad más chica multiplica por 10; cada peldaño que subes hacia una unidad más grande divide entre 10 (¡salvo de m a km que salta 1000!)."
        ),
        "cuerpo_teoria": (
            "Reglas de conversión lineal:\n"
            "1. De unidad grande a chica (ej. m → cm): MULTIPLICA por 10 por peldaño (m→cm son 2 peldaños = ×100).\n"
            "2. De unidad chica a grande (ej. cm → m): DIVIDE entre 10 por peldaño (cm→m son 2 peldaños = ÷100).\n"
            "3. De m a km hay 1000 metros (1 km = 1000 m)."
        ),
        "advertencia": (
            "¡Atención! La palabra 'perímetro' está PROHIBIDA en esta fase. Aquí hablamos de 'longitud', 'distancia total' o 'contorno'."
        ),
        "diccionario": {
            "Kilómetro (km)": "1000 metros.",
            "Metro (m)": "Unidad base de longitud.",
            "Centímetro (cm)": "La centésima parte de un metro (1 m = 100 cm).",
            "Milímetro (mm)": "La milésima parte de un metro (1 cm = 10 mm)."
        },
        "ejemplos": [
            {
                "enunciado": "Un niño mide 1,42 m de estatura. " + escalera_unidades("lineal", ["cm","dm","m"], "m", "cm", 1.42, color_modulo(5,3)) + "<br/>¿Cuántos centímetros son?",
                "pasos": [
                    {"orden": 1, "texto": "De metros a centímetros bajamos 2 peldaños: m → dm → cm (×100)."},
                    {"orden": 2, "texto": "1,42 × 100 = 142 cm."},
                    {"orden": 3, "texto": "Mide 142 cm."}
                ]
            },
            {
                "enunciado": "Un lápiz gastado mide 12,5 cm. ¿Cuántos milímetros son?",
                "pasos": [
                    {"orden": 1, "texto": "De cm a mm bajamos 1 peldaño (×10)."},
                    {"orden": 2, "texto": "12,5 × 10 = 125 mm."},
                    {"orden": 3, "texto": "Mide 125 mm."}
                ]
            },
            {
                "enunciado": "Vive a 1,2 km de la escuela. ¿Cuántos metros son?",
                "pasos": [
                    {"orden": 1, "texto": "1 km = 1000 m → multiplicamos por 1000."},
                    {"orden": 2, "texto": "1,2 × 1000 = 1200 m."},
                    {"orden": 3, "texto": "Son 1200 m."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Para pasar 85 cm a metros, Bruno multiplicó por 100 y obtuvo 8500 m. ¿Qué cometió?",
                "pasos": [
                    {"orden": 1, "texto": "De cm a m se pasa de unidad chica a grande, por lo que se debe DIVIDIR entre 100."},
                    {"orden": 2, "texto": "85 ÷ 100 = 0,85 m."},
                    {"orden": 3, "texto": "Bruno cometió la confusión MULTIPLICAR_AL_SUBIR."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Comparar 1,35 m y 148 cm. ¿Cuál es mayor?",
                "pasos": [
                    {"orden": 1, "texto": "Convertimos a la misma unidad: 1,35 m = 135 cm."},
                    {"orden": 2, "texto": "Comparación: 135 cm < 148 cm."},
                    {"orden": 3, "texto": "148 cm es mayor."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Convierte 2,5 m a centímetros.",
                "respuesta": "250",
                "feedback_acierto": "¡Correcto! 2,5 × 100 = 250 cm.",
                "feedback_error": "De m a cm multiplica por 100."
            },
            {
                "enunciado": "Convierte 450 cm a metros.",
                "respuesta": "4,5",
                "feedback_acierto": "¡Excelente! 450 ÷ 100 = 4,5 m.",
                "feedback_error": "De cm a m divide entre 100."
            },
            {
                "enunciado": "Convierte 3 km a metros.",
                "respuesta": "3000",
                "feedback_acierto": "¡Brillante! 3 × 1000 = 3000 m.",
                "feedback_error": "1 km = 1000 m."
            }
        ]
    },

    {
        "modulo_id": 3, "nivel_id": 2, "seccion": 302,
        "titulo": "Operaciones con unidades mixtas",
        "texto_descubrimiento": (
            "¡Aprende la Regla de Oro del Medidor! ⚠️ NUNCA sumes ni restes números que estén en distintas unidades sin convertirlos primero. "
            "Sumar 1,5 metros con 45 centímetros directamente da un disparate. Primero convierte todo a la misma unidad (todo a m o todo a cm) y recién ahí calcula."
        ),
        "cuerpo_teoria": (
            "Pasos para operar con unidades mixtas:\n"
            "1. Lee la unidad solicitada en la pregunta.\n"
            "2. Convierte todas las medidas del enunciado a esa misma unidad objetivo.\n"
            "3. Realiza la suma o resta requerida."
        ),
        "advertencia": (
            "¡Cuidado con la trampa de sumar directo! 1,5 m + 45 cm NO es 46,5. Pasa 1,5 m a 150 cm primero."
        ),
        "diccionario": {
            "Unidades mixtas": "Medidas dadas en diferentes unidades (ej. metros y centímetros en el mismo problema).",
            "Unidad objetivo": "La unidad en la que la pregunta pide la respuesta final."
        },
        "ejemplos": [
            {
                "enunciado": "Un pasillo mide 12,40 m y una alfombra mide 950 cm. ¿Cuántos metros de pasillo quedan sin cubrir?",
                "pasos": [
                    {"orden": 1, "texto": "Convertimos 950 cm a m: 950 ÷ 100 = 9,50 m."},
                    {"orden": 2, "texto": "Restamos: 12,40 − 9,50 = 2,90 m."},
                    {"orden": 3, "texto": "Quedan 2,90 m."}
                ]
            },
            {
                "enunciado": "Una cuerda de 2,5 m se une a otra de 180 cm. ¿Qué largo total tienen en metros?",
                "pasos": [
                    {"orden": 1, "texto": "Convertimos 180 cm a m: 180 ÷ 100 = 1,80 m."},
                    {"orden": 2, "texto": "Sumamos: 2,50 + 1,80 = 4,30 m."},
                    {"orden": 3, "texto": "Miden 4,30 m."}
                ]
            },
            {
                "enunciado": "Un ciclista recorre tramos de 0,8 km, 650 m y 1,2 km. ¿Cuántos km recorrió?",
                "pasos": [
                    {"orden": 1, "texto": "650 m a km: 650 ÷ 1000 = 0,65 km."},
                    {"orden": 2, "texto": "Sumamos: 0,80 + 0,65 + 1,20 = 2,65 km."},
                    {"orden": 3, "texto": "Recorrió 2,65 km."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Sofía sumó 1,5 m + 45 cm obteniendo 46,5 cm. ¿Cuál fue su fallo?",
                "pasos": [
                    {"orden": 1, "texto": "Sumó directamente los valores numéricos sin igualar unidades."},
                    {"orden": 2, "texto": "1,5 m = 150 cm; 150 + 45 = 195 cm."},
                    {"orden": 3, "texto": "Cometió UNIDADES_MIXTAS_SIN_IGUALAR."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Para unir un tramo de 3,2 m con uno de 80 cm, ¿cuál es el cálculo en metros?",
                "pasos": [
                    {"orden": 1, "texto": "Convertir 80 cm a metros: 80 ÷ 100 = 0,80 m."},
                    {"orden": 2, "texto": "Sumar 3,20 + 0,80 = 4,00 m."},
                    {"orden": 3, "texto": "Total: 4,00 m."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Suma 1,2 m + 80 cm en centímetros.",
                "respuesta": "200",
                "feedback_acierto": "¡Correcto! 120 cm + 80 cm = 200 cm.",
                "feedback_error": "1,2 m = 120 cm. Luego 120 + 80 = 200."
            },
            {
                "enunciado": "Resta 5 m − 250 cm en metros.",
                "respuesta": "2,5",
                "feedback_acierto": "¡Excelente! 5,0 − 2,5 = 2,5 m.",
                "feedback_error": "250 cm = 2,5 m. Luego 5 − 2,5 = 2,5."
            },
            {
                "enunciado": "Suma 0,5 km + 400 m en metros.",
                "respuesta": "900",
                "feedback_acierto": "¡Brillante! 500 m + 400 m = 900 m.",
                "feedback_error": "0,5 km = 500 m. Luego 500 + 400 = 900."
            }
        ]
    },

    {
        "modulo_id": 3, "nivel_id": 3, "seccion": 303,
        "titulo": "Escalas de mapas y rutas por tramos",
        "texto_descubrimiento": (
            "¡Conviértete en Cartógrafo Experto! 🗺️ En mapas y planos las distancias se dibujan reducidas mediante una escala. "
            "Si el mapa dice '1 cm = 5 km', cada centímetro medido con la regla representa 5 kilómetros reales. Y para la distancia total de una ruta, se suman todos sus tramos."
        ),
        "cuerpo_teoria": (
            "Reglas de escalas y rutas:\n"
            "1. Escala simple (1 cm = X km): multiplica los cm medidos por X para obtener la distancia real.\n"
            "2. Escala 1:100 (planos): 1 cm del plano = 100 cm reales (1 metro real).\n"
            "3. Ruta por tramos: suma todos los tramos recorridos."
        ),
        "advertencia": (
            "¡Atención en escalas 1:100! 1 cm en el plano son 100 cm reales, es decir, 1 metro real. No lo confundas con 100 metros."
        ),
        "diccionario": {
            "Escala": "Relación entre la medida del dibujo y la medida real.",
            "Ruta por tramos": "Recorrido dividido en varias etapas que se suman."
        },
        "ejemplos": [
            {
                "enunciado": "En un mapa escala 1 cm = 5 km, dos ciudades están a 4 cm de distancia. ¿Cuál es la distancia real?",
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos cm del mapa por el valor real de 1 cm: 4 × 5 = 20 km."},
                    {"orden": 2, "texto": "Distancia real: 20 km."}
                ]
            },
            {
                "enunciado": "Una mudanza recorre tramos de 12,5 km, 8,75 km y 15,0 km. ¿Distancia total?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos los tres tramos: 12,50 + 8,75 + 15,00 = 36,25 km."},
                    {"orden": 2, "texto": "Distancia total: 36,25 km."}
                ]
            },
            {
                "enunciado": "En un plano 1:100 una pared mide 3,5 cm. ¿Cuánto mide en metros reales?",
                "pasos": [
                    {"orden": 1, "texto": "1 cm = 1 metro real en 1:100."},
                    {"orden": 2, "texto": "3,5 cm = 3,5 metros real."},
                    {"orden": 3, "texto": "Mide 3,5 m."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Para saber la distancia si 1 cm = 10 km y hay 3 cm, Mateo dividió 3 ÷ 10. ¿Es correcto?",
                "pasos": [
                    {"orden": 1, "texto": "Mateo invirtió la escala dividiendo en vez de multiplicar."},
                    {"orden": 2, "texto": "Con la escala hay que multiplicar: 3 × 10 = 30 km."},
                    {"orden": 3, "texto": "Cometió la confusión ESCALA_INVERTIDA."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Una carrera tiene etapas de 1,5 km, 2,0 km y 1,75 km. ¿Alcanza un circuito de 6 km?",
                "pasos": [
                    {"orden": 1, "texto": "Sumamos etapas: 1,50 + 2,00 + 1,75 = 5,25 km."},
                    {"orden": 2, "texto": "5,25 km < 6 km."},
                    {"orden": 3, "texto": "Sí alcanza."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "En mapa 1 cm = 4 km, distan 3 cm. ¿Distancia real en km?",
                "respuesta": "12",
                "feedback_acierto": "¡Correcto! 3 × 4 = 12 km.",
                "feedback_error": "Multiplica los cm del mapa por 4."
            },
            {
                "enunciado": "Suma tramos de 2,5 km y 3,8 km.",
                "respuesta": "6,3",
                "feedback_acierto": "¡Excelente! 2,5 + 3,8 = 6,3 km.",
                "feedback_error": "Suma 2,5 + 3,8 = 6,3."
            },
            {
                "enunciado": "En plano 1:100 una mesa mide 2 cm. ¿Metros reales?",
                "respuesta": "2",
                "feedback_acierto": "¡Brillante! 2 cm en 1:100 son 2 m.",
                "feedback_error": "1 cm en 1:100 equivale a 1 metro real."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 4: Medidas de Volumen (secciones 401, 402, 403)
    # =========================================================================
    {
        "modulo_id": 4, "nivel_id": 1, "seccion": 401,
        "titulo": "Escalera cúbica",
        "texto_descubrimiento": (
            "¡Bienvenido a la Escalera Cúbica! 🧃 Medimos volumen y capacidad. A diferencia de la escalera de longitud, "
            "¡aquí cada peldaño salta de **1000 en 1000**! Porque el volumen tiene 3 dimensiones: 10×10×10 = 1000. 1 Litro son 1000 mililitros."
        ),
        "cuerpo_teoria": (
            "Reglas de conversión cúbica:\n"
            "1. Capacidad: 1 Litro (L) = 1000 mililitros (mL).\n"
            "2. Volumen: 1 dm³ = 1000 cm³; 1 m³ = 1000 dm³.\n"
            "3. Bajar peldaño → MULTIPLICA por 1000; Subir peldaño → DIVIDE entre 1000."
        ),
        "advertencia": (
            "¡No uses el factor 10 ni 100! En volumen y capacidad cada salto vale 1000."
        ),
        "diccionario": {
            "Litro (L)": "Unidad de capacidad; 1000 mL = 1 L.",
            "Mililitro (mL)": "Milésima parte de un litro.",
            "Centímetro cúbico (cm³)": "Cubo de 1 cm de lado.",
            "Decímetro cúbico (dm³)": "Cubo de 1 dm de lado (1000 cm³)."
        },
        "ejemplos": [
            {
                "enunciado": "Una botella tiene 1,5 L de agua. " + escalera_unidades("cubica", ["mL","L"], "L", "mL", 1.5, color_modulo(5,4)) + "<br/>¿Cuántos mL son?",
                "pasos": [
                    {"orden": 1, "texto": "De L a mL bajamos 1 peldaño cúbico (×1000)."},
                    {"orden": 2, "texto": "1,5 × 1000 = 1500 mL."},
                    {"orden": 3, "texto": "Tiene 1500 mL."}
                ]
            },
            {
                "enunciado": "Un balde tiene 8 L. ¿Cuántos mL son?",
                "pasos": [
                    {"orden": 1, "texto": "8 × 1000 = 8000 mL."},
                    {"orden": 2, "texto": "Son 8000 mL."}
                ]
            },
            {
                "enunciado": "Junta 6 latas de 350 mL. ¿Cuántos litros suman?",
                "pasos": [
                    {"orden": 1, "texto": "6 × 350 = 2100 mL."},
                    {"orden": 2, "texto": "De mL a L dividimos entre 1000: 2100 ÷ 1000 = 2,1 L."},
                    {"orden": 3, "texto": "Suman 2,1 L."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Iker convierte 4 L a mL y dice que son 400 mL. ¿Cuál es su error?",
                "pasos": [
                    {"orden": 1, "texto": "Iker usó el factor 100 en vez de 1000."},
                    {"orden": 2, "texto": "4 × 1000 = 4000 mL."},
                    {"orden": 3, "texto": "Cometió SALTO_CUBICO_10 / factor 100."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Meli convierte 3500 mL a L y responde 350 L. ¿Qué ocurrió?",
                "pasos": [
                    {"orden": 1, "texto": "Meli dividió entre 10 en vez de 1000."},
                    {"orden": 2, "texto": "3500 ÷ 1000 = 3,5 L."},
                    {"orden": 3, "texto": "Respuesta correcta: 3,5 L."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Convierte 2,3 L a mililitros.",
                "respuesta": "2300",
                "feedback_acierto": "¡Correcto! 2,3 × 1000 = 2300 mL.",
                "feedback_error": "De L a mL multiplica por 1000."
            },
            {
                "enunciado": "Convierte 750 mL a litros.",
                "respuesta": "0,75",
                "feedback_acierto": "¡Excelente! 750 ÷ 1000 = 0,75 L.",
                "feedback_error": "De mL a L divide entre 1000."
            },
            {
                "enunciado": "Convierte 2 dm³ a cm³.",
                "respuesta": "2000",
                "feedback_acierto": "¡Brillante! 2 × 1000 = 2000 cm³.",
                "feedback_error": "De dm³ a cm³ multiplica por 1000."
            }
        ]
    },

    {
        "modulo_id": 4, "nivel_id": 2, "seccion": 402,
        "titulo": "Volumen y capacidad: dm³=L, cm³=mL",
        "texto_descubrimiento": (
            "¡El truco mágico del espacio y el líquido! ✨ Un decímetro cúbico (dm³) y un litro (L) son EXACTAMENTE la misma cantidad. "
            "Igual pasa entre centímetro cúbico (cm³) y mililitro (mL). El número NO cambia: 30 dm³ = 30 L."
        ),
        "cuerpo_teoria": (
            "Equivalencias fundamentales 1:1:\n"
            "1. 1 dm³ = 1 L (conversión directa, el número es igual).\n"
            "2. 1 cm³ = 1 mL (conversión directa, el número es igual).\n"
            "3. Ancla del metro cúbico: 1 m³ = 1000 L (como mil botellas de 1 litro)."
        ),
        "advertencia": (
            "¡No multipliques de dm³ a L! Son la misma cantidad: 30 dm³ son 30 L (sin cuentas)."
        ),
        "diccionario": {
            "dm³ = L": "1 decímetro cúbico de volumen equivale a 1 litro de capacidad.",
            "cm³ = mL": "1 centímetro cúbico equivale a 1 mililitro.",
            "Metro cúbico (m³)": "Cubo de 1 m de lado; almacena 1000 litros de agua."
        },
        "ejemplos": [
            {
                "enunciado": "Un acuario ocupa 30 dm³. ¿Cuántos litros de agua caben?",
                "pasos": [
                    {"orden": 1, "texto": "1 dm³ = 1 L (equivalencia 1:1)."},
                    {"orden": 2, "texto": "30 dm³ = 30 L."},
                    {"orden": 3, "texto": "Caben 30 L."}
                ]
            },
            {
                "enunciado": "Un envase mide 500 cm³. ¿Cuántos mililitros contiene?",
                "pasos": [
                    {"orden": 1, "texto": "1 cm³ = 1 mL (equivalencia 1:1)."},
                    {"orden": 2, "texto": "500 cm³ = 500 mL."},
                    {"orden": 3, "texto": "Contiene 500 mL."}
                ]
            },
            {
                "enunciado": "Una caja de agua mide 2 m³. ¿Cuántos litros almacena?",
                "pasos": [
                    {"orden": 1, "texto": "1 m³ = 1000 L."},
                    {"orden": 2, "texto": "2 × 1000 = 2000 L."},
                    {"orden": 3, "texto": "Almacena 2000 L."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Dani dice que 30 dm³ a L requiere multiplicar 30 × 10 = 300 L. ¿Tiene razón?",
                "pasos": [
                    {"orden": 1, "texto": "Dani inventó un factor donde no lo hay."},
                    {"orden": 2, "texto": "dm³ y L son la misma cantidad (1:1). 30 dm³ = 30 L."},
                    {"orden": 3, "texto": "Dani no tiene razón."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Fran calcula litros en 2 m³ y responde 2 L creyendo que m³ también es 1:1. ¿Qué error cometió?",
                "pasos": [
                    {"orden": 1, "texto": "El atajo 1:1 es solo para dm³=L y cm³=mL."},
                    {"orden": 2, "texto": "Para m³ a L se multiplica por 1000: 2 m³ = 2000 L."},
                    {"orden": 3, "texto": "Cometió m3_A_L_MAL_ESCALADO."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Un estanque ocupa 15 dm³. ¿Cuántos litros de agua caben?",
                "respuesta": "15",
                "feedback_acierto": "¡Correcto! 1 dm³ = 1 L → 15 L.",
                "feedback_error": "1 dm³ es lo mismo que 1 L, el número no cambia."
            },
            {
                "enunciado": "Un vaso de jarabe mide 250 cm³. ¿Cuántos mL son?",
                "respuesta": "250",
                "feedback_acierto": "¡Excelente! 1 cm³ = 1 mL → 250 mL.",
                "feedback_error": "1 cm³ es lo mismo que 1 mL."
            },
            {
                "enunciado": "Un tanque de 3 m³. ¿Cuántos litros almacena?",
                "respuesta": "3000",
                "feedback_acierto": "¡Brillante! 3 × 1000 = 3000 L.",
                "feedback_error": "1 m³ = 1000 L."
            }
        ]
    },

    {
        "modulo_id": 4, "nivel_id": 3, "seccion": 403,
        "titulo": "Problemas de capacidad en contexto",
        "texto_descubrimiento": (
            "¡Resuelve casos reales de capacidad! 🧪 Frascos de medicamentos, consumo de combustible y mezclas de jugos. "
            "Decide cuándo restar lo consumido y cuándo dividir para saber cuántas dosis caben."
        ),
        "cuerpo_teoria": (
            "Estrategias de problemas de capacidad:\n"
            "1. Capacidad restante: Capacidad total − Consumo.\n"
            "2. Cantidad de dosis: Capacidad del frasco ÷ Dosis unitaria.\n"
            "3. Mezclas: Suma de los volúmenes de los ingredientes."
        ),
        "advertencia": (
            "¡Ojo con mezclar L y mL! Si tienes 1,2 L y 800 mL, pasa 1,2 L a 1200 mL antes de sumar."
        ),
        "diccionario": {
            "Dosis": "Cantidad de líquido que se administra de una vez.",
            "Consumo": "Líquido gastado o retirado de un recipiente."
        },
        "ejemplos": [
            {
                "enunciado": "Mezcla 1,2 L de agua con 800 mL de concentrado. ¿Cuántos litros de jugo obtiene?",
                "pasos": [
                    {"orden": 1, "texto": "800 mL = 0,8 L."},
                    {"orden": 2, "texto": "1,2 + 0,8 = 2,0 L."},
                    {"orden": 3, "texto": "Obtiene 2,0 L."}
                ]
            },
            {
                "enunciado": "Un frasco de 120 mL y cada dosis es de 5 mL. ¿Cuántas dosis tiene?",
                "pasos": [
                    {"orden": 1, "texto": "120 ÷ 5 = 24."},
                    {"orden": 2, "texto": "Tiene 24 dosis."}
                ]
            },
            {
                "enunciado": "Un bidón de 20 L perdió 12,5 L. ¿Cuánto queda?",
                "pasos": [
                    {"orden": 1, "texto": "20,0 − 12,5 = 7,5 L."},
                    {"orden": 2, "texto": "Quedan 7,5 L."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Frasco de 200 mL con dosis de 15 mL 3 veces al día. ¿Alcanza para un día?",
                "pasos": [
                    {"orden": 1, "texto": "Dosis diaria: 15 × 3 = 45 mL."},
                    {"orden": 2, "texto": "45 mL < 200 mL → Sí alcanza."},
                    {"orden": 3, "texto": "Sí alcanza."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Repartir 60 L en cajitas de 200 mL. ¿Cuántas cajitas se llenan?",
                "pasos": [
                    {"orden": 1, "texto": "60 L = 60000 mL."},
                    {"orden": 2, "texto": "60000 ÷ 200 = 300 cajitas."},
                    {"orden": 3, "texto": "Se llenan 300 cajitas."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Un cartón de 1 L pierde 350 mL. ¿Cuántos mL quedan?",
                "respuesta": "650",
                "feedback_acierto": "¡Correcto! 1000 − 350 = 650 mL.",
                "feedback_error": "1 L = 1000 mL. 1000 − 350 = 650."
            },
            {
                "enunciado": "Un frasco de 150 mL con dosis de 10 mL. ¿Cuántas dosis tiene?",
                "respuesta": "15",
                "feedback_acierto": "¡Excelente! 150 ÷ 10 = 15.",
                "feedback_error": "Divide 150 entre 10."
            },
            {
                "enunciado": "Un tanque de 45 L carga 28,5 L. ¿Cuánto falta para llenarlo?",
                "respuesta": "16,5",
                "feedback_acierto": "¡Brillante! 45,0 − 28,5 = 16,5 L.",
                "feedback_error": "45,0 − 28,5 = 16,5."
            }
        ]
    },

    # =========================================================================
    # MÓDULO 5: Unidades de Superficie (secciones 501, 502, 503)
    # =========================================================================
    {
        "modulo_id": 5, "nivel_id": 1, "seccion": 501,
        "titulo": "Escalera cuadrada",
        "texto_descubrimiento": (
            "¡Bienvenido a la Escalera Cuadrada! 🟨 Medimos superficies (azulejos, cartulinas, carpetas). "
            "En superficie cada peldaño salta de **100 en 100** porque 10×10 = 100. 1 m² son 100 dm², y 1 dm² son 100 cm²."
        ),
        "cuerpo_teoria": (
            "Reglas de la escalera cuadrada:\n"
            "1. De unidad grande a chica (ej. m² → cm²): MULTIPLICA por 100 por peldaño (m²→cm² son 2 peldaños = ×10000).\n"
            "2. De unidad chica a grande (ej. cm² → dm²): DIVIDE entre 100 por peldaño.\n"
            "3. Recordatorio: en esta fase la superficie YA viene dada, nunca se calcula con fórmula base×altura (eso es Fase 6)."
        ),
        "advertencia": (
            "¡Cuidado con usar el factor 10! En superficie cada peldaño vale 100, no 10."
        ),
        "diccionario": {
            "Metro cuadrado (m²)": "Unidad base de superficie (cuadrado de 1 m de lado).",
            "Decímetro cuadrado (dm²)": "La centésima parte de un metro cuadrado (1 m² = 100 dm²).",
            "Centímetro cuadrado (cm²)": "La centésima parte de un decímetro cuadrado (1 dm² = 100 cm²)."
        },
        "ejemplos": [
            {
                "enunciado": "Un azulejo tiene 400 cm². " + escalera_unidades("cuadrada", ["cm²","dm²","m²"], "cm²", "dm²", 400, color_modulo(5,5)) + "<br/>¿Cuántos dm² son?",
                "pasos": [
                    {"orden": 1, "texto": "De cm² a dm² subimos 1 peldaño cuadrado (÷100)."},
                    {"orden": 2, "texto": "400 ÷ 100 = 4 dm²."},
                    {"orden": 3, "texto": "Son 4 dm²."}
                ]
            },
            {
                "enunciado": "Un post-it mide 49 cm². ¿Cuántos mm² son?",
                "pasos": [
                    {"orden": 1, "texto": "De cm² a mm² bajamos 1 peldaño (×100)."},
                    {"orden": 2, "texto": "49 × 100 = 4900 mm²."},
                    {"orden": 3, "texto": "Son 4900 mm²."}
                ]
            },
            {
                "enunciado": "El aula tiene 48 m² de piso. ¿Cuántos dm² son?",
                "pasos": [
                    {"orden": 1, "texto": "48 × 100 = 4800 dm²."},
                    {"orden": 2, "texto": "Son 4800 dm²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Mateo convierte 2 m² a cm² multiplicando por 100 y obtiene 200 cm². ¿Qué cometió?",
                "pasos": [
                    {"orden": 1, "texto": "De m² a cm² hay 2 peldaños cuadrados (m² → dm² → cm²)."},
                    {"orden": 2, "texto": "El factor es 100 × 100 = 10000. 2 × 10000 = 20000 cm²."},
                    {"orden": 3, "texto": "Cometió SALTO_CUADRADO_10 / factor lineal."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Una cartulina mide 600 cm² y se cortan 250 cm². ¿Cuánto queda?",
                "pasos": [
                    {"orden": 1, "texto": "Restamos la parte recortada: 600 − 250 = 350 cm²."},
                    {"orden": 2, "texto": "Quedan 350 cm²."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Convierte 5 m² a decímetros cuadrados (dm²).",
                "respuesta": "500",
                "feedback_acierto": "¡Correcto! 5 × 100 = 500 dm².",
                "feedback_error": "De m² a dm² multiplica por 100."
            },
            {
                "enunciado": "Convierte 300 cm² a decímetros cuadrados (dm²).",
                "respuesta": "3",
                "feedback_acierto": "¡Excelente! 300 ÷ 100 = 3 dm².",
                "feedback_error": "De cm² a dm² divide entre 100."
            },
            {
                "enunciado": "Una servilleta mide 100 cm². ¿Cuántos dm² son?",
                "respuesta": "1",
                "feedback_acierto": "¡Brillante! 100 ÷ 100 = 1 dm².",
                "feedback_error": "100 cm² = 1 dm²."
            }
        ]
    },

    {
        "modulo_id": 5, "nivel_id": 2, "seccion": 502,
        "titulo": "Pulgadas y pies a cm",
        "texto_descubrimiento": (
            "¡Conoce las unidades no métricas! 📐 En pantallas de TV y celulares se mide la diagonal en **pulgadas** (1 pulg = 2,54 cm). "
            "En muebles y arquitectura se usa el **pie** (1 pie = 30,48 cm). Aquí aprendes a pasarlas a centímetros."
        ),
        "cuerpo_teoria": (
            "Factores de conversión no métrica a cm:\n"
            "1. Pulgadas a cm: multiplica las pulgadas por 2,54.\n"
            "2. Pies a cm: multiplica los pies por 30,48.\n"
            "3. Las pulgadas de una pantalla miden su diagonal, solo se convierten a cm."
        ),
        "advertencia": (
            "¡Usa los factores exactos! 1 pulgada = 2,54 cm (no lo redondees a 2,5)."
        ),
        "diccionario": {
            "Pulgada (pulg)": "Unidad de longitud equivalente a 2,54 cm.",
            "Pie": "Unidad de longitud equivalente a 30,48 cm (o 12 pulgadas)."
        },
        "ejemplos": [
            {
                "enunciado": "Un celular tiene una pantalla de 6 pulgadas de diagonal. ¿Cuántos cm son?",
                "pasos": [
                    {"orden": 1, "texto": "6 × 2,54 = 15,24 cm."},
                    {"orden": 2, "texto": "Mide 15,24 cm de diagonal."}
                ]
            },
            {
                "enunciado": "Una TV tiene 32 pulgadas de diagonal. ¿Cuántos cm son?",
                "pasos": [
                    {"orden": 1, "texto": "32 × 2,54 = 81,28 cm."},
                    {"orden": 2, "texto": "Mide 81,28 cm."}
                ]
            },
            {
                "enunciado": "Un mueble mide 5 pies de ancho. ¿Cuántos cm son?",
                "pasos": [
                    {"orden": 1, "texto": "5 × 30,48 = 152,4 cm."},
                    {"orden": 2, "texto": "Mide 152,4 cm."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Para pasar 10 pulgadas a cm, Leo redondeó 2,54 a 2,5 y respondió 25 cm. ¿Qué ocurrió?",
                "pasos": [
                    {"orden": 1, "texto": "Leo cometió la confusión PULGADA_MAL_REDONDEADA."},
                    {"orden": 2, "texto": "10 × 2,54 = 25,4 cm exactos."},
                    {"orden": 3, "texto": "Resultado exacto: 25,4 cm."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: ¿Cuántos cm son 2 pies?",
                "pasos": [
                    {"orden": 1, "texto": "2 × 30,48 = 60,96 cm."},
                    {"orden": 2, "texto": "Mide 60,96 cm."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Convierte 10 pulgadas a centímetros (1 pulg = 2,54 cm).",
                "respuesta": "25,4",
                "feedback_acierto": "¡Correcto! 10 × 2,54 = 25,4 cm.",
                "feedback_error": "Multiplica 10 por 2,54."
            },
            {
                "enunciado": "Convierte 2 pies a centímetros (1 pie = 30,48 cm).",
                "respuesta": "60,96",
                "feedback_acierto": "¡Excelente! 2 × 30,48 = 60,96 cm.",
                "feedback_error": "Multiplica 2 por 30,48."
            },
            {
                "enunciado": "Una pantalla de 5 pulgadas de diagonal. ¿Centímetros?",
                "respuesta": "12,7",
                "feedback_acierto": "¡Brillante! 5 × 2,54 = 12,7 cm.",
                "feedback_error": "5 × 2,54 = 12,7."
            }
        ]
    },

    {
        "modulo_id": 5, "nivel_id": 3, "seccion": 503,
        "titulo": "Hectáreas, m² y reparto en lotes",
        "texto_descubrimiento": (
            "¡El nivel formal de la tierra y los lotes! 🏞️ Aprendes a medir terrenos grandes en **hectáreas (ha)** y a repartir parcelas "
            "en lotes iguales. 1 hectárea son **10 000 metros cuadrados** (un cuadrado de 100 m por 100 m)."
        ),
        "cuerpo_teoria": (
            "Reglas de hectáreas y lotes:\n"
            "1. 1 hectárea (ha) = 10 000 m² (multiplica por 10 000 para pasar ha → m²).\n"
            "2. 1 kilómetro cuadrado (km²) = 100 hectáreas (ha).\n"
            "3. Reparto en lotes: Superficie total ÷ Cantidad de lotes iguales."
        ),
        "advertencia": (
            "¡Cuidado! 1 ha no son 1000 m², son 10 000 m². No le olvides un cero."
        ),
        "diccionario": {
            "Hectárea (ha)": "Unidad agraria de superficie (10 000 m²).",
            "Loteo": "Dividir un terreno grande en partes iguales."
        },
        "ejemplos": [
            {
                "enunciado": "Un terreno mide 4,5 ha. ¿Cuántos m² son?",
                "pasos": [
                    {"orden": 1, "texto": "4,5 × 10 000 = 45 000 m²."},
                    {"orden": 2, "texto": "Son 45 000 m²."}
                ]
            },
            {
                "enunciado": "Un terreno de 4,5 ha se reparte en 15 lotes iguales. ¿Cuántos m² cada lote?",
                "pasos": [
                    {"orden": 1, "texto": "4,5 ha = 45 000 m²."},
                    {"orden": 2, "texto": "45 000 ÷ 15 = 3000 m²."},
                    {"orden": 3, "texto": "Cada lote tiene 3000 m²."}
                ]
            },
            {
                "enunciado": "Una fazenda mide 1,5 km². ¿Cuántas hectáreas son?",
                "pasos": [
                    {"orden": 1, "texto": "1,5 × 100 = 150 ha."},
                    {"orden": 2, "texto": "Son 150 ha."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Terreno de 9000 m² se divide en 12 casas iguales. ¿Cuántos m² tiene cada casa?",
                "pasos": [
                    {"orden": 1, "texto": "Dividimos superficie total ÷ cantidad de casas: 9000 ÷ 12 = 750."},
                    {"orden": 2, "texto": "Cada casa tiene 750 m²."}
                ]
            },
            {
                "enunciado": "TJS Resuelto: Campo de 7140 m². ¿Cuántas hectáreas son?",
                "pasos": [
                    {"orden": 1, "texto": "De m² a ha dividimos entre 10 000: 7140 ÷ 10 000 = 0,714 ha."},
                    {"orden": 2, "texto": "Son 0,714 ha."}
                ]
            }
        ],
        "interactivos": [
            {
                "enunciado": "Convierte 2 ha a metros cuadrados (m²).",
                "respuesta": "20000",
                "feedback_acierto": "¡Correcto! 2 × 10 000 = 20 000 m².",
                "feedback_error": "1 ha = 10 000 m²."
            },
            {
                "enunciado": "Divide un terreno de 5000 m² en 5 lotes iguales. ¿m² por lote?",
                "respuesta": "1000",
                "feedback_acierto": "¡Excelente! 5000 ÷ 5 = 1000 m².",
                "feedback_error": "Divide 5000 entre 5."
            },
            {
                "enunciado": "Convierte 3 km² a hectáreas (ha).",
                "respuesta": "300",
                "feedback_acierto": "¡Brillante! 3 × 100 = 300 ha.",
                "feedback_error": "1 km² = 100 ha."
            }
        ]
    }
]
