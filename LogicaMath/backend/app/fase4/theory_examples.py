# theory_examples.py
# ─────────────────────────────────────────────────────────────
# Base de ejemplos guiados estructurados para Fase 4 (Decimales).
# Cumple con C2.2, C2.4, C3 y §4.3 de docs/reestructuraciondefases.md.
# Exactly 4 guided examples per level (3 calculation + 1 TJS 5-step with active commitment on step 3).

from app.utils.svg_figuras import tabla_datos, comparador_opciones, diagrama_conversion, color_modulo

def obtener_ejemplos_expandidos_fase4(modulo_id: int, nivel_id: int) -> list:
    ejemplos_db = {
        # =========================================================================
        # MÓDULO 1: Suma y Resta de Decimales
        # =========================================================================
        (1, 1): [
            {
                "enunciado": "Mía compra una libreta y un lápiz. ¿Cuánto pagó en total?<br/>" +
                             tabla_datos([("Libreta", "R$ 3,25"), ("Lápiz", "R$ 1,40")], color=color_modulo(1,1)),
                "pasos": [
                    {"orden": 1, "texto": "Alineamos los números haciendo coincidir la coma vertical: 3,25 + 1,40."},
                    {"orden": 2, "texto": "Sumamos centésimas (5+0=5), décimas (2+4=6) y unidades (3+1=4)."},
                    {"orden": 3, "texto": "Resultado final: Mía pagó R$ 4,65 en total."}
                ]
            },
            {
                "enunciado": "Hugo compró jugo y galletas. ¿Cuánto gastó?<br/>" +
                             tabla_datos([("Jugo", "R$ 4,50"), ("Galletas", "R$ 2,30")], color=color_modulo(1,1)),
                "pasos": [
                    {"orden": 1, "texto": "Alineamos por la coma decimal: 4,50 + 2,30."},
                    {"orden": 2, "texto": "Sumamos columna por columna de derecha a izquierda."},
                    {"orden": 3, "texto": "Resultado: Hugo gastó R$ 6,80."}
                ]
            },
            {
                "enunciado": "Leo junta dinero el lunes y el martes. ¿Cuánto ahorró?<br/>" +
                             tabla_datos([("Lunes", "R$ 5,30"), ("Martes", "R$ 2,45")], color=color_modulo(1,1)),
                "pasos": [
                    {"orden": 1, "texto": "Comprobamos que ambos números tienen dos cifras tras la coma."},
                    {"orden": 2, "texto": "Sumamos: 30 + 45 = 75 centésimas, 5 + 2 = 7 unidades."},
                    {"orden": 3, "texto": "Ahorro total: R$ 7,75."}
                ]
            },
            {
                "enunciado": "Mía lleva R$ 10,00 a la tienda. Quiere una carpeta de R$ 6,25 y un sacapuntas de R$ 3,90. ¿Le alcanza el dinero o le falta?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Leemos el caso: Mía tiene R$ 10,00 y los artículos cuestan R$ 6,25 y R$ 3,90."},
                    {"orden": 2, "texto": "Debemos evaluar un juicio situacional: calcular el costo total y comparar con el presupuesto de R$ 10,00."},
                    {
                        "orden": 3,
                        "texto": "¿Qué conclusión es la correcta para Mía?",
                        "opciones": [
                            "Le falta dinero (el total es R$ 10,15)",
                            "Le alcanza justo y no le sobra nada",
                            "Le sobra dinero (el total es R$ 9,15)"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! R$ 6,25 + R$ 3,90 = R$ 10,15. Le faltan R$ 0,15.",
                            "1": "Atención: no alcanza justo porque 6,25 + 3,90 se pasa de 10,00.",
                            "2": "Cuidado: sumar 25 + 90 tienta a olvidar el acarreo de 1 unidad."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: Sumamos 6,25 + 3,90 = 10,15. Como 10,15 > 10,00, a Mía le faltan R$ 0,15."},
                    {"orden": 5, "texto": "Análisis de trampas: El distractor de R$ 9,15 ocurre al olvidar sumar el acarreo (2 décimas + 9 décimas = 11 décimas)."}
                ]
            }
        ],
        (1, 2): [
            {
                "enunciado": "Leo paga una compra con un billete. ¿Cuánto recibe de vuelto?<br/>" +
                             tabla_datos([("Pago", "R$ 10,00"), ("Costo", "R$ 3,40")], color=color_modulo(1,2)),
                "pasos": [
                    {"orden": 1, "texto": "Alineamos por la coma: 10,00 - 3,40."},
                    {"orden": 2, "texto": "Restamos centésimas (0-0=0) y décimas pidiendo prestado (10-4=6)."},
                    {"orden": 3, "texto": "Restamos unidades (9-3=6). Vuelto: R$ 6,60."}
                ]
            },
            {
                "enunciado": "Zoe tenía una cinta y cortó un trozo. ¿Cuánta cinta le queda?<br/>" +
                             tabla_datos([("Cinta inicial", "5,50 m"), ("Cortado", "2,25 m")], color=color_modulo(1,2)),
                "pasos": [
                    {"orden": 1, "texto": "Completamos con cero a 5,50 para tener dos decimales."},
                    {"orden": 2, "texto": "Restamos 5,50 - 2,25 alineando la coma vertical."},
                    {"orden": 3, "texto": "Resultado: Le quedan 3,25 metros de cinta."}
                ]
            },
            {
                "enunciado": "Hugo tenía un ahorro y gastó una parte. ¿Cuánto le sobra?<br/>" +
                             tabla_datos([("Inicial", "R$ 15,80"), ("Gasto", "R$ 7,50")], color=color_modulo(1,2)),
                "pasos": [
                    {"orden": 1, "texto": "Alineamos 15,80 - 7,50 por la coma."},
                    {"orden": 2, "texto": "Restamos 80 - 50 = 30 centésimas y 15 - 7 = 8 unidades."},
                    {"orden": 3, "texto": "Resultado: Le sobra R$ 8,30."}
                ]
            },
            {
                "enunciado": "Sofia tiene R$ 20,00. Compra un libro de R$ 14,30. El vendedor le devuelve R$ 6,70. ¿El vuelto está correcto?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Evaluamos el vuelto entregado a Sofia: pagó R$ 20,00 por R$ 14,30."},
                    {"orden": 2, "texto": "Debemos juzgar si 20,00 - 14,30 es igual a R$ 6,70 o si hay un error en el cambio."},
                    {
                        "orden": 3,
                        "texto": "¿Qué opción describe el estado del vuelto?",
                        "opciones": [
                            "Está equivocado, el vuelto correcto es R$ 5,70",
                            "Está perfecto, el vuelto correcto es R$ 6,70",
                            "Está equivocado, el vuelto correcto es R$ 4,70"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! Al pedir prestado 1 unidad de 20, las decenas quedan en 19. 19 - 14 = 5. Vuelto = R$ 5,70.",
                            "1": "Atención: R$ 6,70 se obtiene si se resta 20 - 14 sin descontar el prestado.",
                            "2": "Cuidado: R$ 4,70 resta de más en las unidades."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: 20,00 - 14,30 = 5,70. El vendedor le dio R$ 1,00 de más por error."},
                    {"orden": 5, "texto": "Análisis de trampas: 6,70 tienta porque 10 - 3 = 7 y se olvida reducir 20 a 19."}
                ]
            }
        ],
        (1, 3): [
            {
                "enunciado": "Mía ahorra, recibe un pago y gasta una parte. ¿Cuánto tiene ahora?<br/>" +
                             tabla_datos([("Ahorro", "R$ 12,50"), ("Recibe", "R$ 5,00"), ("Gasto", "R$ 8,25")], color=color_modulo(1,3)),
                "pasos": [
                    {"orden": 1, "texto": "Sumamos ingresos: 12,50 + 5,00 = 17,50."},
                    {"orden": 2, "texto": "Restamos el gasto: 17,50 - 8,25."},
                    {"orden": 3, "texto": "Resultado final: Mía tiene R$ 9,25."}
                ]
            },
            {
                "enunciado": "Hugo tiene dinero y compra dos artículos iguales. ¿Cuánto vuelto recibe?<br/>" +
                             tabla_datos([("Dinero", "R$ 25,00"), ("Artículos", "2"), ("Precio c/u", "R$ 7,50")], color=color_modulo(1,3)),
                "pasos": [
                    {"orden": 1, "texto": "Calculamos la suma de compras: 7,50 + 7,50 = 15,00."},
                    {"orden": 2, "texto": "Restamos del presupuesto: 25,00 - 15,00."},
                    {"orden": 3, "texto": "Vuelto final: R$ 10,00."}
                ]
            },
            {
                "enunciado": "Zoe lleva dinero, compra un estuche y recibe un pago que le debían. ¿Cuánto tiene?<br/>" +
                             tabla_datos([("Lleva", "R$ 18,00"), ("Estuche", "R$ 11,40"), ("Cobro", "R$ 2,00")], color=color_modulo(1,3)),
                "pasos": [
                    {"orden": 1, "texto": "Restamos la compra: 18,00 - 11,40 = 6,60."},
                    {"orden": 2, "texto": "Sumamos el cobro: 6,60 + 2,00 = 8,60."},
                    {"orden": 3, "texto": "Total actual: R$ 8,60."}
                ]
            },
            {
                "enunciado": "Leo dispone de R$ 30,00. Desea comprar un balón de R$ 18,50 y dos mochilas pequeñas de R$ 6,00 cada una. ¿Le alcanza su dinero?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Analizamos las compras de Leo: 1 balón (18,50) + 2 mochilas (6,00 × 2 = 12,00). Presupuesto: 30,00."},
                    {"orden": 2, "texto": "Debemos sumar todos los costos y contrastar contra R$ 30,00."},
                    {
                        "orden": 3,
                        "texto": "¿Cuál es la situación presupuestaria de Leo?",
                        "opciones": [
                            "Le faltan R$ 0,50 para completar la compra",
                            "Le alcanza exacto y no le sobra nada",
                            "Le sobran R$ 1,50 tras pagar"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! Costo total: 18,50 + 12,00 = 30,50. Supera el presupuesto en R$ 0,50.",
                            "1": "Atención: olvidar contar la segunda mochila hace parecer que 18,50 + 6,00 = 24,50 alcanzaba.",
                            "2": "Cuidado: restar mal 30,50 - 30,00 genera una falsa ganancia."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: 18,50 + 12,00 = 30,50. 30,50 - 30,00 = 0,50 faltantes."},
                    {"orden": 5, "texto": "Análisis de trampas: Omitir el duplicado de la segunda mochila es el error más común."}
                ]
            }
        ],

        # =========================================================================
        # MÓDULO 2: Multiplicación de Decimales
        # =========================================================================
        (2, 1): [
            {
                "enunciado": "Mía compra varios frascos de pintura del mismo precio. ¿Cuánto paga?<br/>" +
                             tabla_datos([("Cantidad", "3"), ("Precio c/u", "R$ 4,20")], color=color_modulo(2,1)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos ignorando la coma: 420 × 3 = 1260."},
                    {"orden": 2, "texto": "Como 4,20 tiene 2 posiciones decimales, contamos 2 lugares desde la derecha."},
                    {"orden": 3, "texto": "Resultado: Mía paga R$ 12,60."}
                ]
            },
            {
                "enunciado": "Hugo necesita varios tramos de cable del mismo largo. ¿Cuántos metros compra?<br/>" +
                             tabla_datos([("Tramos", "4"), ("Largo c/u", "2,3 m")], color=color_modulo(2,1)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos 23 × 4 = 92."},
                    {"orden": 2, "texto": "Contamos 1 posición decimal de 2,3."},
                    {"orden": 3, "texto": "Resultado: Necesita 9,2 metros."}
                ]
            },
            {
                "enunciado": "Zoe compra varios cuadernos del mismo precio. ¿Cuánto gasta?<br/>" +
                             tabla_datos([("Cuadernos", "5"), ("Precio c/u", "R$ 6,10")], color=color_modulo(2,1)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos 610 × 5 = 3050."},
                    {"orden": 2, "texto": "Ubicamos 2 cifras decimales desde la derecha."},
                    {"orden": 3, "texto": "Resultado: Gasta R$ 30,50."}
                ]
            },
            {
                "enunciado": "Un comerciante ofrece un pack de 6 cuadernos a R$ 24,00 en total. Por separado, cada cuaderno cuesta R$ 4,20. ¿Qué conviene comprar?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Leemos las alternativas: Comprar el pack de 6 por R$ 24,00 vs comprar 6 sueltas a R$ 4,20 c/u."},
                    {"orden": 2, "texto": "Calculamos el costo de 6 sueltas: 4,20 × 6 y comparamos con 24,00."},
                    {
                        "orden": 3,
                        "texto": "¿Qué opción le conviene al comprador?",
                        "opciones": [
                            "Conviene el pack de 6 (ahorra R$ 1,20)",
                            "Conviene comprar 6 sueltas (ahorra R$ 1,20)",
                            "Cuestan exactamente lo mismo"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! 6 × 4,20 = R$ 25,20. El pack ahorra R$ 1,20.",
                            "1": "Atención: sueltas cuestan 25,20, que es más caro que 24,00.",
                            "2": "Cuidado: multiplicar 4,20 × 6 sin considerar los 20 centavos da 24,00 engañoso."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: 4,20 × 6 = 25,20. 25,20 - 24,00 = 1,20 de ahorro con el pack."},
                    {"orden": 5, "texto": "Análisis de trampas: Ignorar las décimas (20 centavos × 6 = 1,20) hace creer que salían igual."}
                ]
            }
        ],
        (2, 2): [
            {
                "enunciado": "Calcula el costo total de los estuches.<br/>" +
                             tabla_datos([("Cantidad", "4"), ("Precio c/u", "R$ 12,15")], color=color_modulo(2,2)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos 1215 × 4 = 4860."},
                    {"orden": 2, "texto": "Colocamos 2 posiciones decimales desde la derecha."},
                    {"orden": 3, "texto": "Resultado: R$ 48,60."}
                ]
            },
            {
                "enunciado": "Se compran varios listones de madera del mismo largo. ¿Largo total?<br/>" +
                             tabla_datos([("Listones", "3"), ("Largo c/u", "4,25 m")], color=color_modulo(2,2)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos 425 × 3 = 1275."},
                    {"orden": 2, "texto": "Contamos 2 cifras tras la coma."},
                    {"orden": 3, "texto": "Resultado: 12,75 metros."}
                ]
            },
            {
                "enunciado": "Una caja contiene varios paquetes de harina del mismo peso. ¿Peso total?<br/>" +
                             tabla_datos([("Paquetes", "5"), ("Peso c/u", "1,75 kg")], color=color_modulo(2,2)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos 175 × 5 = 875."},
                    {"orden": 2, "texto": "Colocamos 2 decimales."},
                    {"orden": 3, "texto": "Resultado: 8,75 kg."}
                ]
            },
            {
                "enunciado": "Una imprenta cobra R$ 0,35 por copia a color. Un alumno necesita 25 copias. Presupuesto disponible: R$ 10,00. ¿Le alcanza?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Datos: 25 copias a R$ 0,35 cada una. Presupuesto R$ 10,00."},
                    {"orden": 2, "texto": "Multiplicamos 25 × 0,35 para hallar el total y comparar con 10,00."},
                    {
                        "orden": 3,
                        "texto": "¿Qué ocurre con el presupuesto del alumno?",
                        "opciones": [
                            "Le alcanza y le sobran R$ 1,25",
                            "Le falta dinero para pagar las copias",
                            "Le alcanza justo sin sobrante"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! 25 × 0,35 = R$ 8,75. 10,00 - 8,75 = R$ 1,25 sobrantes.",
                            "1": "Atención: 8,75 es menor que 10,00, por lo que sí alcanza.",
                            "2": "Cuidado: 8,75 no es igual a 10,00."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: 35 × 25 = 875 → R$ 8,75 total. Sobra: 10,00 - 8,75 = R$ 1,25."},
                    {"orden": 5, "texto": "Análisis de trampas: Confundir las 2 posiciones decimales de 0,35 puede llevar a estimar R$ 87,50 por error."}
                ]
            }
        ],
        (2, 3): [
            {
                "enunciado": "Un tren avanza a velocidad constante. Halla la distancia recorrida.<br/>" +
                             tabla_datos([("Velocidad", "1,5 m/s"), ("Tiempo", "0,4 s")], color=color_modulo(2,3)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos números enteros: 15 × 4 = 60."},
                    {"orden": 2, "texto": "Sumamos posiciones decimales: 1,5 (1) + 0,4 (1) = 2 decimales."},
                    {"orden": 3, "texto": "Contamos 2 lugares desde la derecha: 0,60 m."}
                ]
            },
            {
                "enunciado": "Un rollo entero tiene una cinta. ¿Cuánto hay en la porción indicada?<br/>" +
                             tabla_datos([("Rollo entero", "0,25 m"), ("Porción", "0,5")], color=color_modulo(2,3)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos 25 × 5 = 125."},
                    {"orden": 2, "texto": "Sumamos decimales: 0,25 (2) + 0,5 (1) = 3 decimales."},
                    {"orden": 3, "texto": "Resultado: 0,125 m."}
                ]
            },
            {
                "enunciado": "Calcula el producto de los dos factores.<br/>" +
                             tabla_datos([("Factor A", "2,5"), ("Factor B", "1,2")], color=color_modulo(2,3)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos 25 × 12 = 300."},
                    {"orden": 2, "texto": "Sumamos decimales: 1 + 1 = 2 posiciones."},
                    {"orden": 3, "texto": "Resultado: 3,00 (o 3)."}
                ]
            },
            {
                "enunciado": "Una receta requiere 0,75 kg de harina por torta. Si prepara 1,5 tortas, ¿1 kg de harina será suficiente?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Datos: 0,75 kg × 1,5 tortas. Harina disponible: 1,00 kg."},
                    {"orden": 2, "texto": "Calculamos la harina necesaria multiplicando 0,75 × 1,5."},
                    {
                        "orden": 3,
                        "texto": "¿Le alcanza el kilo de harina?",
                        "opciones": [
                            "No alcanza, necesita 1,125 kg en total",
                            "Sí alcanza, necesita exactamente 0,90 kg",
                            "Sí alcanza y le sobra medio kilo"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! 0,75 × 1,5 = 1,125 kg. Falta 0,125 kg de harina.",
                            "1": "Atención: 0,75 + 0,15 da 0,90 por error al sumar en vez de multiplicar.",
                            "2": "Cuidado: asumir que 1,5 veces 0,75 es menor a 1 es falso."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: 75 × 15 = 1125 → 3 posiciones decimales = 1,125 kg. Faltan 0,125 kg."},
                    {"orden": 5, "texto": "Análisis de trampas: Sumar 0,75 + 0,15 engaña creyendo que se necesitaban 0,90 kg."}
                ]
            }
        ],

        # =========================================================================
        # MÓDULO 3: División de Decimales
        # =========================================================================
        (3, 1): [
            {
                "enunciado": "Reparte el monto equitativamente entre los amigos. ¿Cuánto recibe cada uno?<br/>" +
                             tabla_datos([("Monto total", "R$ 8,40"), ("Amigos", "2")], color=color_modulo(3,1)),
                "pasos": [
                    {"orden": 1, "texto": "Dividimos la parte entera: 8 ÷ 2 = 4."},
                    {"orden": 2, "texto": "Colocamos la coma en el cociente (4,) y dividimos las décimas: 4 ÷ 2 = 2."},
                    {"orden": 3, "texto": "Resultado: Cada amigo recibe R$ 4,20."}
                ]
            },
            {
                "enunciado": "Reparte la cinta en trozos iguales. ¿Largo de cada trozo?<br/>" +
                             tabla_datos([("Largo total", "9,6 m"), ("Trozos", "3")], color=color_modulo(3,1)),
                "pasos": [
                    {"orden": 1, "texto": "Dividimos 9 ÷ 3 = 3."},
                    {"orden": 2, "texto": "Ponemos la coma (3,) y dividimos 6 ÷ 3 = 2."},
                    {"orden": 3, "texto": "Resultado: 3,2 metros."}
                ]
            },
            {
                "enunciado": "Reparte el total entre los niños en partes iguales.<br/>" +
                             tabla_datos([("Total", "R$ 6,30"), ("Niños", "3")], color=color_modulo(3,1)),
                "pasos": [
                    {"orden": 1, "texto": "Dividimos 6 ÷ 3 = 2."},
                    {"orden": 2, "texto": "Ponemos coma y dividimos 3 ÷ 3 = 1."},
                    {"orden": 3, "texto": "Resultado: R$ 2,10 cada uno."}
                ]
            },
            {
                "enunciado": "Se desea repartir una soga de 7,5 metros en 5 tramos. El encargado afirma que cada tramo medirá 15 metros. ¿Es correcta su afirmación?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Datos: 7,5 m ÷ 5 tramos. Afirmación: 15 m por tramo."},
                    {"orden": 2, "texto": "Evaluamos la lógica: al dividir una soga de 7,5 m en trozos, cada trozo DEBE ser menor que la soga entera."},
                    {
                        "orden": 3,
                        "texto": "¿Qué error cometió el encargado?",
                        "opciones": [
                            "Olvidó poner la coma decimal (el resultado es 1,5 m)",
                            "La afirmación es correcta",
                            "Multiplicó en vez de sumar"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! 7,5 ÷ 5 = 1,5 m. Olvidó colocar la coma tras la parte entera.",
                            "1": "Atención: un trozo de 15 m en una soga de 7,5 m es imposible.",
                            "2": "Cuidado: 75 ÷ 5 es 15, el error fue de escala decimal."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: 7 ÷ 5 = 1 (sobra 2). Pasamos la coma → 25 ÷ 5 = 5. Resultado = 1,5 m."},
                    {"orden": 5, "texto": "Análisis de trampas: Omitir la coma convierte 1,5 m en 15 m (10 veces más grande)."}
                ]
            }
        ],
        (3, 2): [
            {
                "enunciado": "Reparte el total en partes iguales.<br/>" +
                             tabla_datos([("Total", "R$ 12,48"), ("Partes", "4")], color=color_modulo(3,2)),
                "pasos": [
                    {"orden": 1, "texto": "Dividimos 12 ÷ 4 = 3."},
                    {"orden": 2, "texto": "Ponemos coma (3,) y bajamos 4 → 4 ÷ 4 = 1."},
                    {"orden": 3, "texto": "Bajamos 8 → 8 ÷ 4 = 2. Resultado: R$ 3,12."}
                ]
            },
            {
                "enunciado": "Reparte el alimento entre los recipientes en partes iguales.<br/>" +
                             tabla_datos([("Masa total", "15,35 kg"), ("Recipientes", "5")], color=color_modulo(3,2)),
                "pasos": [
                    {"orden": 1, "texto": "Dividimos 15 ÷ 5 = 3."},
                    {"orden": 2, "texto": "Ponemos coma y bajamos 3 (no alcanza → 0 en cociente)."},
                    {"orden": 3, "texto": "Bajamos 5 → 35 ÷ 5 = 7. Resultado: 3,07 kg."}
                ]
            },
            {
                "enunciado": "Reparte el total entre las personas en partes iguales.<br/>" +
                             tabla_datos([("Total", "R$ 20,50"), ("Personas", "5")], color=color_modulo(3,2)),
                "pasos": [
                    {"orden": 1, "texto": "Dividimos 20 ÷ 5 = 4."},
                    {"orden": 2, "texto": "Ponemos coma y dividimos 50 ÷ 5 = 10."},
                    {"orden": 3, "texto": "Resultado: R$ 4,10."}
                ]
            },
            {
                "enunciado": "Tres socios se reparten R$ 18,09 de ganancias. Uno propone quedarse con R$ 6,30 sosteniendo que es la tercera parte exacta. ¿Es justa la propuesta?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Datos: R$ 18,09 a repartir en 3 partes. Propuesta: R$ 6,30 por socio."},
                    {"orden": 2, "texto": "Calculamos 18,09 ÷ 3 y comparamos con 6,30."},
                    {
                        "orden": 3,
                        "texto": "¿Es justa la división propuesta?",
                        "opciones": [
                            "No es justa: la parte exacta es R$ 6,03",
                            "Es justa: R$ 6,30 es la tercera parte",
                            "No es justa: la parte exacta es R$ 6,33"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! 18 ÷ 3 = 6. Luego 0 ÷ 3 = 0. Luego 9 ÷ 3 = 3 → R$ 6,03.",
                            "1": "Atención: confundir 09 centésimas con 90 centésimas da 6,30 erróneo.",
                            "2": "Cuidado: el 0 en las décimas debe respetarse."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: 18,09 ÷ 3 = 6,03. El socio pedía 27 centavos de más por persona."},
                    {"orden": 5, "texto": "Análisis de trampas: Omitir poner 0 en la posición de las décimas (0 ÷ 3 = 0) confunde 6,03 con 6,30."}
                ]
            }
        ],
        (3, 3): [
            {
                "enunciado": "Calcula el cociente desplazando la coma decimal.<br/>" +
                             tabla_datos([("Dividendo", "6,0"), ("Divisor", "1,5")], color=color_modulo(3,3)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos ambos por 10 para eliminar la coma del divisor: 60 ÷ 15."},
                    {"orden": 2, "texto": "Dividimos 60 ÷ 15 = 4."},
                    {"orden": 3, "texto": "Resultado final: 4."}
                ]
            },
            {
                "enunciado": "Calcula el cociente.<br/>" +
                             tabla_datos([("Dividendo", "4,5"), ("Divisor", "0,5")], color=color_modulo(3,3)),
                "pasos": [
                    {"orden": 1, "texto": "Multiplicamos por 10 ambos lados: 45 ÷ 5."},
                    {"orden": 2, "texto": "Dividimos 45 ÷ 5 = 9."},
                    {"orden": 3, "texto": "Resultado: 9."}
                ]
            },
            {
                "enunciado": "Calcula el cociente.<br/>" +
                             tabla_datos([("Dividendo", "8,4"), ("Divisor", "1,2")], color=color_modulo(3,3)),
                "pasos": [
                    {"orden": 1, "texto": "Desplazamos la coma 1 lugar: 84 ÷ 12."},
                    {"orden": 2, "texto": "Dividimos 84 ÷ 12 = 7."},
                    {"orden": 3, "texto": "Resultado: 7."}
                ]
            },
            {
                "enunciado": "Hugo necesita 2,2 m de cable para decorar una fiesta. Los rollos en la tienda vienen únicamente de 1,0 m. ¿Cuántos rollos debe comprar?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Situación: Hugo necesita 2,2 m. Rollos de 1,0 m. La tienda no vende fracciones de rollo."},
                    {"orden": 2, "texto": "Juicio práctico: 2,2 ÷ 1,0 = 2,2. Pero no se pueden comprar 0,2 rollos. Si compra 2 rollos, tiene 2,0 m y le faltan 0,2 m."},
                    {
                        "orden": 3,
                        "texto": "¿Cuántos rollos completos debe comprar Hugo?",
                        "opciones": [
                            "Debe comprar 3 rollos completos",
                            "Debe comprar 2 rollos completos",
                            "Debe comprar 2,2 rollos"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! Regla de redondeo en contexto: con 2 rollos solo obtiene 2,0 m (le faltaría cable). Necesita 3.",
                            "1": "Atención: con 2 rollos solo junta 2,0 m y la decoración queda corta por 0,2 m.",
                            "2": "Cuidado: la tienda no vende rollos abiertos ni cortados."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: Aunque 2,2 está más cerca de 2 en matemática pura, el contexto real exige cubrir todo el sobrante. Se sube al entero 3."},
                    {"orden": 5, "texto": "Análisis de trampas: Aplicar redondeo matemático estándar (2,2 → 2) deja la necesidad sin cubrir."}
                ]
            }
        ],

        # =========================================================================
        # MÓDULO 4: Conversiones Métricas y Unidades
        # =========================================================================
        (4, 1): [
            {
                "enunciado": "Convierte 2,5 metros a centímetros bajando la escalera métrica.<br/>" +
                             diagrama_conversion("m", "cm", 2.5, color_modulo(4,4)),
                "pasos": [
                    {"orden": 1, "texto": "De m a cm bajamos 2 escalones (m → dm → cm), lo que significa multiplicar por 100."},
                    {"orden": 2, "texto": "Desplazamos la coma 2 lugares a la derecha: 2,5 × 100 = 250."},
                    {"orden": 3, "texto": "Resultado: 2,5 m = 250 cm."}
                ]
            },
            {
                "enunciado": "Convierte 1,8 kilómetros a metros.<br/>" +
                             diagrama_conversion("km", "m", 1.8, color_modulo(4,4)),
                "pasos": [
                    {"orden": 1, "texto": "De km a m bajamos 3 escalones (×1000)."},
                    {"orden": 2, "texto": "Desplazamos la coma 3 lugares a la derecha: 1,8 × 1000 = 1800."},
                    {"orden": 3, "texto": "Resultado: 1,8 km = 1800 m."}
                ]
            },
            {
                "enunciado": "Convierte 3,5 metros a milímetros.<br/>" +
                             diagrama_conversion("m", "mm", 3.5, color_modulo(4,4)),
                "pasos": [
                    {"orden": 1, "texto": "De m a mm bajamos 3 escalones (×1000)."},
                    {"orden": 2, "texto": "Multiplicamos 3,5 × 1000 = 3500."},
                    {"orden": 3, "texto": "Resultado: 3,5 m = 3500 mm."}
                ]
            },
            {
                "enunciado": "Un atleta recorre 1,5 km. Su compañero afirma que 1,5 km son 150 metros. ¿Es correcta la afirmación?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Datos: 1,5 km a metros. Afirmación del compañero: 150 m."},
                    {"orden": 2, "texto": "Evaluamos el factor de conversión: 1 km = 1000 m. Para pasar km → m se multiplica por 1000."},
                    {
                        "orden": 3,
                        "texto": "¿Es correcta la afirmación del compañero?",
                        "opciones": [
                            "Es incorrecta: 1,5 km equivalen a 1500 metros",
                            "Es correcta: 1,5 km equivalen a 150 metros",
                            "Es incorrecta: 1,5 km equivalen a 15 metros"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! 1,5 × 1000 = 1500 m. El compañero solo multiplicó por 100.",
                            "1": "Atención: multiplicar por 100 da 150 m, pero de km a m se baja 3 escalones (×1000).",
                            "2": "Cuidado: 15 m resultaría de multiplicar por 10."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: De km a m hay 3 escalones. 1,5 × 1000 = 1500 m."},
                    {"orden": 5, "texto": "Análisis de trampas: Mover la coma solo 2 lugares en vez de 3 es el error típico."}
                ]
            }
        ],
        (4, 2): [
            {
                "enunciado": "Convierte 450 centímetros a metros subiendo la escalera métrica.<br/>" +
                             diagrama_conversion("cm", "m", 450, color_modulo(4,4)),
                "pasos": [
                    {"orden": 1, "texto": "De cm a m subimos 2 escalones (÷100)."},
                    {"orden": 2, "texto": "Desplazamos la coma 2 lugares a la izquierda: 450,0 ÷ 100 = 4,50."},
                    {"orden": 3, "texto": "Resultado: 450 cm = 4,5 m."}
                ]
            },
            {
                "enunciado": "Convierte 2500 metros a kilómetros.<br/>" +
                             diagrama_conversion("m", "km", 2500, color_modulo(4,4)),
                "pasos": [
                    {"orden": 1, "texto": "De m a km subimos 3 escalones (÷1000)."},
                    {"orden": 2, "texto": "Desplazamos la coma 3 lugares a la izquierda: 2500 ÷ 1000 = 2,5."},
                    {"orden": 3, "texto": "Resultado: 2500 m = 2,5 km."}
                ]
            },
            {
                "enunciado": "Convierte 750 milímetros a metros.<br/>" +
                             diagrama_conversion("mm", "m", 750, color_modulo(4,4)),
                "pasos": [
                    {"orden": 1, "texto": "De mm a m subimos 3 escalones (÷1000)."},
                    {"orden": 2, "texto": "Desplazamos la coma 3 lugares a la izquierda: 750 ÷ 1000 = 0,75."},
                    {"orden": 3, "texto": "Resultado: 750 mm = 0,75 m."}
                ]
            },
            {
                "enunciado": "Una pista mide 800 metros. Para el cartel hay que registrar la distancia en km. El encargado anota 8,0 km. ¿Anotó la distancia correcta?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Datos: 800 m a km. Registro del encargado: 8,0 km."},
                    {"orden": 2, "texto": "Evaluamos: 1 km = 1000 m. Pasar de m a km requiere subir 3 escalones (÷1000)."},
                    {
                        "orden": 3,
                        "texto": "¿Qué error cometió el encargado?",
                        "opciones": [
                            "Dividió entre 100 en vez de 1000 (la distancia real es 0,8 km)",
                            "Anotó la distancia correcta",
                            "Multiplicó por 1000 en vez de dividir"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! 800 ÷ 1000 = 0,8 km. Anotar 8,0 km es 10 veces más largo.",
                            "1": "Atención: 8,0 km equivale a 8000 metros, no 800.",
                            "2": "Cuidado: la división por 100 movió 2 comas en lugar de 3."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: 800 ÷ 1000 = 0,8 km."},
                    {"orden": 5, "texto": "Análisis de trampas: Olvidar un cero al dividir entre 1000 deja el número en 8,0 km por error."}
                ]
            }
        ],
        (4, 3): [
            {
                "enunciado": "Zoe tiene una cinta y le añade otro trozo. ¿Cuántos metros mide en total?<br/>" +
                             tabla_datos([("Cinta inicial", "1,5 m"), ("Añadido", "50 cm")], color=color_modulo(4,4)),
                "pasos": [
                    {"orden": 1, "texto": "Convertimos 50 cm a metros: 50 ÷ 100 = 0,5 m."},
                    {"orden": 2, "texto": "Sumamos ambas cantidades en metros: 1,5 + 0,5 = 2,0 m."},
                    {"orden": 3, "texto": "Resultado: La cinta mide 2,0 metros en total."}
                ]
            },
            {
                "enunciado": "Hugo camina por la mañana y por la tarde. ¿Distancia total en km?<br/>" +
                             tabla_datos([("Mañana", "1,2 km"), ("Tarde", "800 m")], color=color_modulo(4,4)),
                "pasos": [
                    {"orden": 1, "texto": "Convertimos 800 m a km: 800 ÷ 1000 = 0,8 km."},
                    {"orden": 2, "texto": "Sumamos en km: 1,2 + 0,8 = 2,0 km."},
                    {"orden": 3, "texto": "Resultado: Caminó 2,0 km."}
                ]
            },
            {
                "enunciado": "Un rollo de cordón se corta en trozos iguales. ¿Sobra cordón?<br/>" +
                             tabla_datos([("Rollo", "2,5 m"), ("Trozos", "5"), ("Cada trozo", "50 cm")], color=color_modulo(4,4)),
                "pasos": [
                    {"orden": 1, "texto": "Convertimos el rollo a centímetros: 2,5 × 100 = 250 cm."},
                    {"orden": 2, "texto": "Calculamos lo que ocupan los trozos: 5 × 50 cm = 250 cm."},
                    {"orden": 3, "texto": "Resultado: 250 cm − 250 cm = 0. No sobra nada."}
                ]
            },
            {
                "enunciado": "Mía une dos cintas para bordear un cuadro. El borde del cuadro mide 1,5 m. ¿Alcanzarán las cintas para cubrirlo?",
                "es_tjs": True,
                "pasos": [
                    {"orden": 1, "texto": "Datos: Cinta A = 1,2 m; Cinta B = 40 cm; Borde del cuadro = 1,5 m."},
                    {"orden": 2, "texto": "No basta con sumar: primero hay que expresar ambas cintas en la misma unidad y después comparar con el borde."},
                    {
                        "orden": 3,
                        "texto": "¿Qué ocurrirá al colocar las cintas en el borde?",
                        "opciones": [
                            "Sobrará cinta: las dos suman 1,6 m y el borde mide 1,5 m",
                            "Alcanzará exacto, sin sobrante",
                            "Faltará cinta para cubrir el borde"
                        ],
                        "opcion_correcta": 0,
                        "explicacion_opciones": {
                            "0": "¡Correcto! 1,2 m + 0,4 m = 1,6 m. Supera el borde de 1,5 m en 0,1 m (10 cm).",
                            "1": "Atención: 1,2 + 0,4 = 1,6, no 1,5. Sobran 10 cm.",
                            "2": "Cuidado: sumar 1,2 + 40 sin convertir unidades es un error grave de escala."
                        }
                    },
                    {"orden": 4, "texto": "Resolución: 40 cm = 0,4 m. Total = 1,2 + 0,4 = 1,6 m. Como 1,6 m > 1,5 m, sobran 0,1 m."},
                    {"orden": 5, "texto": "Análisis de trampas: Sumar 1,2 + 40 directamente daría 41,2 (error de unidades)." }
                ]
            }
        ]
    }
    return ejemplos_db.get((modulo_id, nivel_id), [])
