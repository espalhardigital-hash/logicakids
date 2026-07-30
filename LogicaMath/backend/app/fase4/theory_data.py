"""
Guión pedagógico de teoría para los 12 niveles de la Fase 4 (Operatoria Decimal y Conversiones).
Cumple con las Secciones 5 y 6 de reestructuracion.md y Criterios C1.3, C2, C3, C5.13, §4.3.

Contiene:
  - 12 niveles en FASE5_TEORIA_DATA (3 por módulo, M1 a M4).
  - Texto narrativo por presupuesto (≤ 800 car. narrativa pura, ≤ 400 car. con SVG).
  - Cero vocabulario de fracciones (décimas = partes de 10, centésimas = partes de 100).
  - Regla de las tres capas (Capa 1: enseñanza de redondeo por contexto).
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
            "¡Bienvenida, guardiana de las comas! 🪙 Hoy despiertas tu primer superpoder decimal: "
            "el Alineador de Comas. Cada vez que dos cantidades de dinero se juntan, sus comas decimales deben mirarse cara a cara, "
            "en la misma columna. Si una coma se desalinea, las décimas y centésimas se confunden con las unidades y la cuenta falla. "
            "Tu regla de oro: alinear siempre por la coma vertical, nunca por el borde derecho."
        ),
        "cuerpo_teoria": (
            "Para sumar números decimales correctamente:\n"
            "1. Alinea los números en columna haciendo coincidir las comas verticales.\n"
            "2. Si un número tiene menos cifras decimales que otro, completa con ceros a la derecha (por ejemplo, 5,3 pasa a 5,30).\n"
            "3. Suma columna por columna de derecha a izquierda (centésimas, décimas, unidades, decenas), llevando el acarreo cuando corresponda.\n"
            "4. Coloca la coma decimal en el resultado exactamente debajo de la columna de las comas."
        ),
        "advertencia": (
            "¡Atención! Si sumas 2,7 + 1,45 sin igualar las cifras decimales, podrías tentar a tu mente a sumar 7 + 45. "
            "Antes de operar, revisa si ambos números tienen la misma cantidad de cifras tras la coma. Si no, pon ceros a la derecha."
        ),
        "diccionario": {
            "Número decimal": "Número que tiene parte entera y parte decimal separadas por una coma (ej. 3,25).",
            "Coma decimal": "Signo que separa la parte entera de las décimas y centésimas.",
            "Décimas": "Primera cifra a la derecha de la coma (partes de 10).",
            "Centésimas": "Segunda cifra a la derecha de la coma (partes de 100).",
            "Alinear": "Colocar los números uno debajo del otro con sus comas en la misma línea vertical.",
            "Completar con cero": "Agregar un cero a la derecha de la parte decimal (5,3 = 5,30) sin alterar su valor."
        }
    },
    {
        "modulo_id": 1, "nivel_id": 2, "seccion": 102,
        "titulo": "Resta con completado de ceros",
        "texto_descubrimiento": (
            "Al restar decimales, completar con ceros es obligatorio. Cuando restas a un entero o a un decimal más corto "
            "(como 10,00 - 3,45), los ceros a la derecha actúan como casilleros listos para pedir prestado a la columna izquierda."
        ),
        "cuerpo_teoria": (
            "Pasos para restar decimales sin tropiezos:\n"
            "1. Escribe el minuendo arriba y el sustraendo abajo, alineando las comas.\n"
            "2. Llena los huecos vacíos a la derecha con ceros hasta que ambos tengan las mismas cifras tras la coma.\n"
            "3. Resta normalmente de derecha a izquierda, pidiendo prestado entre columnas cuando sea necesario.\n"
            "4. Copia la coma decimal al resultado en la misma columna vertical."
        ),
        "advertencia": (
            "¡Cuidado al restar de un número entero! Al hacer 10 - 2,35, no bajes el 35 directamente. "
            "Debes transformar 10 en 10,00 y restar 10,00 - 2,35 pidiendo prestado."
        ),
        "diccionario": {
            "Minuendo": "La cantidad mayor de la cual se resta otra.",
            "Sustraendo": "La cantidad que se resta.",
            "Descomposición": "Pedir 1 a la columna izquierda (1 unidad vale 10 décimas o 1 décima vale 10 centésimas).",
            "Cero auxiliar": "Cero que se añade tras la coma para poder restar cifras faltantes."
        }
    },
    {
        "modulo_id": 1, "nivel_id": 3, "seccion": 103,
        "titulo": "Combinadas en contexto",
        "texto_descubrimiento": (
            "En la vida diaria (compras, vuelto, presupuestos), sumas y restas se combinan. "
            "Para resolver problemas con varias operaciones, calcula primero los ingresos o gastos agrupados y mantén las comas alineadas."
        ),
        "cuerpo_teoria": (
            "Estrategia para operaciones combinadas con decimales:\n"
            "1. Identifica qué sumas representan compras o ahorros totales.\n"
            "2. Resta del dinero disponible o presupuesto el total gastado.\n"
            "3. Mantén siempre el formato con dos cifras decimales si trabajas con dinero (R$ 0,00)."
        ),
        "advertencia": (
            "Al calcular el vuelto de un billete grande, asegura escribir los ceros de centésimas en el billete (R$ 50,00)."
        ),
        "diccionario": {
            "Presupuesto": "Cantidad total de dinero disponible antes de comprar.",
            "Vuelto": "Dinero que se devuelve cuando se paga con un billete mayor al costo.",
            "Balance": "Resultado final tras sumar todos los ingresos y restar todos los gastos."
        }
    },

    # =========================================================================
    # MÓDULO 2: Multiplicación de Decimales (secciones 201, 202, 203)
    # =========================================================================
    {
        "modulo_id": 2, "nivel_id": 1, "seccion": 201,
        "titulo": "Un factor decimal (1 cifra)",
        "texto_descubrimiento": (
            "Para multiplicar un número decimal por un número entero (ej. 4,2 × 3), multiplica normalmente "
            "como si no hubiera coma. Al terminar, cuenta cuántas cifras decimales tenía el factor original y coloca la coma en el resultado."
        ),
        "cuerpo_teoria": (
            "Regla del conteo de posiciones decimales:\n"
            "1. Multiplica las cifras ignorando la coma (42 × 3 = 126).\n"
            "2. Cuenta las cifras decimales en los factores (4,2 tiene 1 cifra decimal).\n"
            "3. Coloca la coma en el producto contando 1 posición desde la derecha (12,6)."
        ),
        "advertencia": (
            "¡No alinees las comas para multiplicar! A diferencia de la suma, en la multiplicación cuentas posiciones al final."
        ),
        "diccionario": {
            "Factor": "Cada uno de los números que se multiplican.",
            "Producto": "El resultado final de una multiplicación.",
            "Posiciones decimales": "Cantidad de dígitos a la derecha de la coma decimal."
        }
    },
    {
        "modulo_id": 2, "nivel_id": 2, "seccion": 202,
        "titulo": "Un factor decimal (2 cifras)",
        "texto_descubrimiento": (
            "Cuando el factor decimal tiene dos cifras a la derecha de la coma (ej. 2,15 × 4), "
            "el producto heredará exactamente 2 posiciones decimales desde la derecha."
        ),
        "cuerpo_teoria": (
            "Procedimiento con 2 cifras decimales:\n"
            "1. Opera los números enteros: 215 × 4 = 860.\n"
            "2. El factor 2,15 tiene 2 cifras decimales.\n"
            "3. Cuenta 2 lugares desde la derecha en 860 $\rightarrow$ 8,60."
        ),
        "advertencia": (
            "Si el resultado termina en cero (como 8,60), conserva la coma 2 lugares antes de simplificar ceros al final."
        ),
        "diccionario": {
            "Centésimas en multiplicación": "Al multiplicar centésimas por enteros, el producto mantiene la escala de partes de 100."
        }
    },
    {
        "modulo_id": 2, "nivel_id": 3, "seccion": 203,
        "titulo": "Ambos factores decimales",
        "texto_descubrimiento": (
            "Al multiplicar dos decimales (ej. 1,5 × 0,3), la suma de las cifras decimales de ambos factores "
            "determina la cantidad de cifras decimales del producto final."
        ),
        "cuerpo_teoria": (
            "Regla suma de posiciones decimales:\n"
            "1. Multiplica 15 × 3 = 45.\n"
            "2. Suma decimales: 1,5 (1 cifra) + 0,3 (1 cifra) = 2 cifras decimales.\n"
            "3. Cuenta 2 lugares desde la derecha en 45 $\rightarrow$ 0,45 (añade 0 si faltan cifras)."
        ),
        "advertencia": (
            "Si el producto tiene menos dígitos que las posiciones decimales requeridas (ej. 3 × 2 = 6 con 2 decimales), "
            "agrega ceros a la izquierda antes de poner la coma: 0,06."
        ),
        "diccionario": {
            "Suma de posiciones": "Conteo total de cifras tras la coma en todos los factores involucrados."
        }
    },

    # =========================================================================
    # MÓDULO 3: División de Decimales (secciones 301, 302, 303)
    # =========================================================================
    {
        "modulo_id": 3, "nivel_id": 1, "seccion": 301,
        "titulo": "Dividendo decimal (1 cifra)",
        "texto_descubrimiento": (
            "Al dividir un decimal entre un entero (ej. 8,4 ÷ 2), divide la parte entera normalmente. "
            "En el instante en que pases la coma del dividendo, coloca una coma en el cociente y continúa dividiendo."
        ),
        "cuerpo_teoria": (
            "Pasos para dividir dividendo decimal:\n"
            "1. Divide la parte entera (8 ÷ 2 = 4).\n"
            "2. Pon la coma en el cociente justo al bajar la primera cifra decimal.\n"
            "3. Divide la parte decimal (4 ÷ 2 = 2) $\rightarrow$ Resultado: 4,2."
        ),
        "advertencia": (
            "No olvides poner la coma en el resultado al cruzar la frontera decimal del dividendo."
        ),
        "diccionario": {
            "Dividendo": "El número que se divide.",
            "Divisor": "El número entre el cual se divide.",
            "Cociente": "El resultado de la división."
        }
    },
    {
        "modulo_id": 3, "nivel_id": 2, "seccion": 302,
        "titulo": "Dividendo decimal (2 cifras)",
        "texto_descubrimiento": (
            "Si el dividendo tiene centésimas (ej. 12,48 ÷ 4), se mantiene la misma regla: "
            "coloca la coma en el cociente al pasar a las décimas y continúa dividiendo hasta las centésimas."
        ),
        "cuerpo_teoria": (
            "Pasos con dos cifras decimales:\n"
            "1. Divide 12 ÷ 4 = 3.\n"
            "2. Pon la coma en el cociente (3,).\n"
            "3. Baja 4 y divide 4 ÷ 4 = 1. Baja 8 y divide 8 ÷ 4 = 2 $\rightarrow$ Resultado: 3,12."
        ),
        "advertencia": (
            "Si una cifra decimal no alcanza para el divisor, coloca un 0 en el cociente antes de bajar la siguiente cifra."
        ),
        "diccionario": {
            "Cero en el cociente": "Se anota cuando una cifra bajada es menor que el divisor."
        }
    },
    {
        "modulo_id": 3, "nivel_id": 3, "seccion": 303,
        "titulo": "Divisor decimal y redondeo por contexto",
        "texto_descubrimiento": (
            "Para dividir entre un número que tiene coma en el divisor (ej. 6 ÷ 1,5), desplaza la coma "
            "hacia la derecha en el divisor y en el dividendo las mismas posiciones hasta volver el divisor entero.\n\n"
            "📦 Regla de redondeo por contexto: A veces la cuenta aritmética da un decimal (ej. 2,4 botellas), "
            "pero los objetos del mundo real no se venden fraccionados. Si falta aunque sea un poquito, "
            "debemos subir al siguiente número entero completo (necesitas 3 botellas)."
        ),
        "cuerpo_teoria": (
            "1. Desplazamiento de coma: Multiplica divisor y dividendo por 10, 100 para eliminar la coma del divisor.\n"
            "2. Redondeo en contexto práctico: Cuando el enunciado pregunte por objetos enteros (botellas, cajas, viajes), "
            "si la división tiene sobrante o decimales, se redondea hacia arriba al entero entero."
        ),
        "advertencia": (
            "¡No confundas la cuenta matemática con la realidad! 2,2 botellas significa que con 2 no alcanza. "
            "Se deben comprar 3 botellas completas."
        ),
        "diccionario": {
            "Desplazamiento de coma": "Mover la coma a la derecha en divisor y dividendo la misma cantidad de lugares.",
            "Redondeo por contexto": "Ajustar el resultado al siguiente entero cuando la unidad representa objetos indivisibles."
        }
    },

    # =========================================================================
    # MÓDULO 4: Conversiones Métricas y Unidades (secciones 401, 402, 403)
    # =========================================================================
    {
        "modulo_id": 4, "nivel_id": 1, "seccion": 401,
        "titulo": "Bajar la escalera métrica",
        "texto_descubrimiento": (
            "Para pasar de una unidad mayor a una menor en la escalera métrica (km $\rightarrow$ m, m $\rightarrow$ cm, kg $\rightarrow$ g, L $\rightarrow$ mL), "
            "bajas escalones. Cada escalón hacia abajo multiplica por 10, desplazando la coma decimal a la derecha."
        ),
        "cuerpo_teoria": (
            "Reglas para bajar la escalera:\n"
            "1. Identifica cuántos escalones bajas (ej. m a cm = 2 escalones = ×100).\n"
            "2. Mueve la coma decimal a la derecha tantos lugares como ceros tenga el multiplicador.\n"
            "3. Si se acaban las cifras tras la coma, completa con ceros a la derecha."
        ),
        "advertencia": (
            "Bajar la escalera aumenta la cantidad numérica (un número mayor de unidades pequeñas)."
        ),
        "diccionario": {
            "Escalera métrica": "Representación visual de unidades de medida ordenadas por tamaño.",
            "Bajar escalón": "Multiplicar por 10 por cada nivel que se desciende hacia unidades menores."
        }
    },
    {
        "modulo_id": 4, "nivel_id": 2, "seccion": 402,
        "titulo": "Subir la escalera métrica",
        "texto_descubrimiento": (
            "Para pasar de una unidad menor a una mayor (cm $\rightarrow$ m, g $\rightarrow$ kg, mL $\rightarrow$ L), "
            "subes escalones. Cada escalón hacia arriba divide entre 10, desplazando la coma decimal a la izquierda."
        ),
        "cuerpo_teoria": (
            "Reglas para subir la escalera:\n"
            "1. Identifica cuántos escalones subes (ej. g a kg = 3 escalones = ÷1000).\n"
            "2. Mueve la coma decimal a la izquierda tantos lugares como ceros tenga el divisor.\n"
            "3. Si faltan lugares a la izquierda, añade ceros y coloca 0, al inicio."
        ),
        "advertencia": (
            "Subir la escalera reduce el valor numérico (un número menor de unidades grandes)."
        ),
        "diccionario": {
            "Subir escalón": "Dividir entre 10 por cada nivel que se asciende hacia unidades mayores."
        }
    },
    {
        "modulo_id": 4, "nivel_id": 3, "seccion": 403,
        "titulo": "Unidades mixtas y contexto",
        "texto_descubrimiento": (
            "En problemas de medidas complejas con recipientes, trayectos o pesos, primero convierte "
            "todas las cantidades a la misma unidad antes de comparar, sumar o dividir."
        ),
        "cuerpo_teoria": (
            "Pasos para operar unidades mixtas:\n"
            "1. Elige una unidad común (generalmente la unidad menor o la solicitada en la pregunta).\n"
            "2. Convierte todas las cantidades usando la escalera métrica.\n"
            "3. Realiza el cálculo y expresa la respuesta en la unidad requerida."
        ),
        "advertencia": (
            "Nunca sumes ni restes valores en unidades distintas (ej. no sumes metros con centímetros directamente)."
        ),
        "diccionario": {
            "Unidad común": "La misma unidad de medida a la que se reducen todas las magnitudes antes de calcular."
        }
    }
]
