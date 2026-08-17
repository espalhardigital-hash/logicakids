"""
E7 · Contenido de teoría real para la Fase 5 (reemplaza los placeholders).

Por cada (módulo, nivel): párrafos de descubrimiento con un mini-ejemplo resuelto,
diccionario de 2-3 términos y un dato "¿Sabías que…?". Los ejemplos guiados con
figura siguen viniendo de theory_examples.py; el interactivo de calentamiento lo
arma el seed con el visualizador del módulo.

`texto_descubrimiento` se guarda con saltos de línea (\n): el frontend lo divide
en párrafos.
"""

TEORIA_FASE5 = {
    (1, 1): {
        "parrafos": [
            "Una fracción representa partes de un todo dividido en partes iguales.",
            "El número de abajo, el denominador, indica en cuántas partes iguales se divide el entero. El número de arriba, el numerador, indica cuántas de esas partes tomamos.",
            "Ejemplo: si una pizza se corta en 8 partes iguales y comes 3, comiste 3/8 de la pizza.",
        ],
        "diccionario": {
            "Fracción": "Una forma de representar partes de un todo.",
            "Numerador": "El número de arriba: cuántas partes se toman.",
            "Denominador": "El número de abajo: en cuántas partes iguales se divide el entero.",
        },
        "sabias": "El denominador nunca puede ser 0: no se puede dividir algo en 0 partes.",
    },
    (1, 2): {
        "parrafos": [
            "Dos fracciones son equivalentes si representan la misma cantidad, aunque se escriban con números distintos.",
            "Para hallar una equivalente, multiplica (amplificar) o divide (simplificar) el numerador y el denominador por el mismo número.",
            "Ejemplo: 1/2 = 2/4 = 3/6, porque todas valen la mitad del entero.",
        ],
        "diccionario": {
            "Equivalente": "Fracciones que valen lo mismo aunque tengan otros números.",
            "Amplificar": "Multiplicar numerador y denominador por el mismo número.",
            "Simplificar": "Dividir numerador y denominador por el mismo número.",
        },
        "sabias": "1/2 y 50/100 son exactamente la misma cantidad.",
    },
    (1, 3): {
        "parrafos": [
            "Para comparar partes de un mismo entero, cuenta cuántas partes tiene cada una.",
            "Con el mismo denominador, la fracción con mayor numerador es la mayor.",
            "Ejemplo: en un chocolate de 8 partes, 5/8 es más que 3/8, porque 5 partes es más que 3.",
        ],
        "diccionario": {
            "Comparar": "Decidir cuál cantidad es mayor, menor o si son iguales.",
            "Mayor que (>)": "Tiene más cantidad.",
            "Menor que (<)": "Tiene menos cantidad.",
        },
        "sabias": "Con igual denominador, más numerador siempre significa más cantidad.",
    },
    (2, 1): {
        "parrafos": [
            "Calcular una fracción unitaria (1/n) de una cantidad es repartirla en n grupos iguales y tomar uno.",
            "Se hace dividiendo la cantidad entre el denominador.",
            "Ejemplo: 1/4 de 20 = 20 ÷ 4 = 5.",
        ],
        "diccionario": {
            "Fracción unitaria": "Una fracción con numerador 1, como 1/4.",
            "Repartir": "Dividir en partes iguales.",
        },
        "sabias": "1/10 de una cantidad es lo mismo que dividirla entre 10.",
    },
    (2, 2): {
        "parrafos": [
            "Para calcular a/b de una cantidad se hace en dos pasos.",
            "Primero divide la cantidad entre b (partes el todo) y luego multiplica por a (tomas a partes).",
            "Ejemplo: 3/4 de 20 = (20 ÷ 4) × 3 = 5 × 3 = 15.",
        ],
        "diccionario": {
            "Operador fraccionario": "Usar una fracción para calcular una parte de una cantidad.",
            "Cantidad": "El total sobre el que se calcula la fracción.",
        },
        "sabias": "Primero divides y luego multiplicas: así los números quedan más pequeños y fáciles.",
    },
    (2, 3): {
        "parrafos": [
            "A veces conocemos la parte que se tomó y buscamos lo que queda (el resto) o el total.",
            "Si tomas a/b, el resto es el complemento hasta el entero.",
            "Ejemplo: de 20 galletas tomaste 3/4 (15), entonces quedan 20 − 15 = 5.",
        ],
        "diccionario": {
            "Resto": "Lo que queda después de tomar una parte.",
            "Complemento": "La parte que falta para completar el entero.",
        },
        "sabias": "Si tomas 3/4, siempre queda 1/4: las dos partes juntas forman el entero.",
    },
    (3, 1): {
        "parrafos": [
            "Un porcentaje es una fracción de 100. Por eso 'por ciento' significa 'de cada cien'.",
            "Los porcentajes clave son fáciles: 50% es la mitad, 25% es la cuarta parte y 10% es dividir entre 10.",
            "Ejemplo: 25% de 80 = 80 ÷ 4 = 20.",
        ],
        "diccionario": {
            "Porcentaje": "Una fracción cuyo denominador es 100.",
            "Por ciento (%)": "De cada cien.",
        },
        "sabias": "50% siempre es la mitad, sin importar la cantidad.",
    },
    (3, 2): {
        "parrafos": [
            "Un descuento resta un porcentaje al precio; un recargo lo suma.",
            "Calcula el porcentaje y luego réstalo (o súmalo) al precio inicial.",
            "Ejemplo: 20% de descuento en 50 = 50 − (50 × 20 ÷ 100) = 50 − 10 = 40.",
        ],
        "diccionario": {
            "Descuento": "Cantidad que se resta al precio.",
            "Recargo": "Cantidad que se suma al precio.",
        },
        "sabias": "Un descuento del 100% significa que el producto es gratis.",
    },
    (3, 3): {
        "parrafos": [
            "El promedio (o media aritmética) reparte todo por igual entre los elementos.",
            "Se calcula sumando todos los valores y dividiendo entre cuántos son.",
            "Ejemplo: el promedio de 7, 8 y 9 es (7 + 8 + 9) ÷ 3 = 24 ÷ 3 = 8.",
        ],
        "diccionario": {
            "Promedio": "El valor que resulta de repartir todo por igual.",
            "Media aritmética": "Otro nombre para el promedio.",
        },
        "sabias": "El promedio siempre queda entre el valor más pequeño y el más grande.",
    },
    (4, 1): {
        "parrafos": [
            "Una razón compara dos cantidades y se escribe con dos puntos, como 1:4.",
            "1:4 significa 'una parte de un ingrediente por cada cuatro del otro'.",
            "Ejemplo: en una limonada con razón 1:4, por 1 taza de concentrado van 4 de agua.",
        ],
        "diccionario": {
            "Razón": "Comparación entre dos cantidades (a:b).",
            "Proporción": "Igualdad entre dos razones.",
        },
        "sabias": "Si duplicas las dos cantidades de una razón, la mezcla sabe igual.",
    },
    (4, 2): {
        "parrafos": [
            "Repartir proporcionalmente es distribuir una cantidad según una razón dada.",
            "Primero halla cuánto vale una parte y luego multiplica por las partes de cada uno.",
            "Ejemplo: repartir 20 en razón 1:4 → 5 partes en total, 1 parte = 4, así 1 recibe 4 y el otro 16.",
        ],
        "diccionario": {
            "Reparto proporcional": "Distribuir según una razón.",
            "Parte": "Cada porción igual en la que se divide el total.",
        },
        "sabias": "La suma de todas las partes repartidas siempre da el total original.",
    },
    (4, 3): {
        "parrafos": [
            "En una mezcla, el porcentaje de un ingrediente es su cantidad sobre el total.",
            "Suma los ingredientes para hallar el total y calcula qué fracción representa cada uno.",
            "Ejemplo: 2 de concentrado en 10 de mezcla = 2/10 = 20% de concentrado.",
        ],
        "diccionario": {
            "Mezcla": "Combinación de dos o más ingredientes.",
            "Concentración": "Qué porcentaje del total es un ingrediente.",
        },
        "sabias": "Si agregas más agua a un jugo, baja su concentración pero sube el total.",
    },
}
