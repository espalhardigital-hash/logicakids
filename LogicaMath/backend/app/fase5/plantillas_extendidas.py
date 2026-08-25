"""Familias de transferencia para la Fase 5.

No son cambios cosméticos de nombres o números: cada una añade una acción
matemática explícita sobre la representación del nivel. Se cargan junto a las
plantillas históricas para que el generador conserve una única API.
"""

from __future__ import annotations


_SPECS: dict[tuple[int, int], list[tuple[str, str, str, str]]] = {
    (1, 1): [
        ("doble_coloreadas", "a*2", "doble de las partes coloreadas", "doble_partes"),
        ("triple_coloreadas", "a*3", "triple de las partes coloreadas", "triple_partes"),
        ("doble_libres", "(b-a)*2", "doble de las partes sin colorear", "doble_complemento"),
        ("partes_y_dos", "a+2", "dos partes más que las coloreadas", "comparar_cantidad"),
        ("producto_partes", "a*b", "el producto entre partes coloreadas y partes totales", "relacion_partes"),
        ("libres_y_dos", "(b-a)+2", "dos partes más que las que quedan libres", "complemento"),
    ],
    (1, 2): [
        ("suma_base", "a+b", "la suma del numerador y el denominador de la fracción base", "leer_fraccion"),
        ("producto_base", "a*b", "el producto entre los términos de la fracción base", "relacion_terminos"),
        ("num_ampliado_mas_den", "(a*c)+b", "el numerador amplificado más el denominador original", "amplificacion_parcial"),
        ("den_ampliado_mas_num", "(b*c)+a", "el denominador amplificado más el numerador original", "amplificacion_parcial"),
        ("suma_ampliada", "(a+b)*c", "la suma de ambos términos después de amplificar", "amplificacion_total"),
        ("triple_num_ampliado", "(a*c)*3", "el triple del numerador después de amplificar", "amplificacion_multietapa"),
    ],
    (1, 3): [
        ("triple_coloreadas", "a*3", "triple de las partes coloreadas", "transferencia_multiplicativa"),
        ("doble_complemento", "(b-a)*2", "doble de las partes sin colorear", "transferencia_complemento"),
        ("triple_complemento", "(b-a)*3", "triple de las partes sin colorear", "transferencia_complemento"),
        ("suma_partes", "a+b", "la suma entre partes coloreadas y totales", "interpretacion_datos"),
        ("producto_coloreadas_libres", "a*(b-a)", "el producto entre las partes coloreadas y las libres", "dos_datos"),
        ("complemento_mas_dos", "(b-a)+2", "dos más que las partes libres", "comparacion"),
    ],
    (2, 1): [
        ("dos_grupos", "(total//b)*2", "la cantidad en dos grupos iguales", "fraccion_unitaria"),
        ("tres_grupos_transferencia", "(total//b)*3", "la cantidad en tres grupos iguales", "fraccion_unitaria"),
        ("grupo_mas_dos", "(total//b)+2", "dos objetos más que en un grupo", "comparacion_grupo"),
        ("cuatro_grupos_transferencia", "(total//b)*4", "la cantidad en cuatro grupos iguales", "fraccion_unitaria"),
        ("grupo_doble_mas_dos", "(total//b)*2+2", "dos grupos y dos objetos adicionales", "dos_pasos"),
        ("triple_grupo_mas_dos", "(total//b)*3+2", "tres grupos y dos objetos adicionales", "dos_pasos"),
    ],
    (2, 2): [
        ("parte_mas_un_grupo", "(total//b)*(a+1)", "la fracción indicada y un grupo adicional", "fraccion_mas_unidad"),
        ("complemento_grupos", "(total//b)*(b-a)", "la parte complementaria de la colección", "complemento_fraccion"),
        ("doble_fraccion", "((total//b)*a)*2", "el doble de la fracción indicada", "doble_fraccion"),
        ("fraccion_mas_dos", "((total//b)*a)+2", "la fracción indicada y dos objetos adicionales", "dos_pasos"),
        ("triple_fraccion", "((total//b)*a)*3", "el triple de la fracción indicada", "triple_fraccion"),
        ("fraccion_mas_grupo", "((total//b)*a)+(total//b)", "la fracción indicada y un grupo adicional", "fraccion_mas_unidad"),
    ],
    (2, 3): [
        ("doble_parte", "((total//b)*a)*2", "el doble de la parte indicada", "transferencia_fraccion"),
        ("triple_parte", "((total//b)*a)*3", "el triple de la parte indicada", "transferencia_fraccion"),
        ("complemento_doble", "(total-((total//b)*a))*2", "el doble de lo que no se utiliza", "complemento"),
        ("parte_mas_dos", "((total//b)*a)+2", "la parte indicada y dos objetos adicionales", "dos_pasos"),
        ("complemento_mas_dos", "(total-((total//b)*a))+2", "lo que queda y dos objetos adicionales", "dos_pasos"),
        ("parte_mas_un_grupo", "((total//b)*a)+(total//b)", "la parte indicada más un grupo igual", "fraccion_mas_unidad"),
    ],
    (3, 1): [
        ("doble_porcentaje_cantidad", "((total*a)//100)*2", "el doble de la cantidad que representa el porcentaje", "porcentaje_cantidad"),
        ("cantidad_mas_diez", "((total*a)//100)+10", "la cantidad del porcentaje y diez unidades más", "dos_pasos"),
        ("total_mas_porcentaje", "total+((total*a)//100)", "el total y la cantidad que representa el porcentaje", "aumento"),
        ("mitad_porcentaje", "((total*a)//100)//2", "la mitad de la cantidad que representa el porcentaje", "mitad_porcentaje"),
        ("complemento_transferencia", "total-((total*a)//100)", "la cantidad que falta para completar el total", "complemento_porcentaje"),
        ("porcentaje_mas_dos", "((total*a)//100)+2", "la cantidad del porcentaje y dos unidades más", "dos_pasos"),
    ],
    (3, 2): [
        ("doble_ahorro", "((total*a)//100)*2", "el doble del ahorro", "descuento_multietapa"),
        ("ahorro_mas_diez", "((total*a)//100)+10", "el ahorro y diez unidades más", "dos_pasos"),
        ("precio_mas_ahorro", "total+((total*a)//100)", "el precio original más el ahorro calculado", "interpretacion_porcentaje"),
        ("mitad_ahorro", "((total*a)//100)//2", "la mitad del ahorro", "mitad_porcentaje"),
        ("precio_final", "total-((total*a)//100)", "el precio después del descuento", "descuento"),
        ("ahorro_mas_dos", "((total*a)//100)+2", "el ahorro y dos unidades más", "dos_pasos"),
    ],
    (3, 3): [
        ("promedio_mas_uno", "((a+b+c)//3)+1", "el promedio de los tres datos y una unidad más", "promedio_transferencia"),
        ("doble_promedio", "((a+b+c)//3)*2", "el doble del promedio", "promedio_multietapa"),
        ("triple_promedio", "((a+b+c)//3)*3", "el triple del promedio", "promedio_multietapa"),
        ("mitad_promedio", "((a+b+c)//3)//2", "la mitad del promedio", "promedio_multietapa"),
        ("suma_mas_dos", "a+b+c+2", "la suma de los tres datos y dos unidades más", "suma_datos"),
        ("promedio_mas_dos", "((a+b+c)//3)+2", "el promedio y dos unidades más", "promedio_transferencia"),
    ],
    (4, 1): [
        ("doble_componente_a", "(a*c)*2", "el doble de la cantidad del primer componente", "razon_escalada"),
        ("triple_componente_b", "(b*c)*3", "el triple de la cantidad del segundo componente", "razon_escalada"),
        ("suma_componentes", "(a*c)+(b*c)", "la suma de ambos componentes escalados", "total_razon"),
        ("diferencia_componentes", "(b*c)-(a*c)", "la diferencia entre los componentes escalados", "comparar_razon"),
        ("a_mas_dos", "(a*c)+2", "el primer componente escalado y dos unidades más", "dos_pasos"),
        ("b_mas_dos", "(b*c)+2", "el segundo componente escalado y dos unidades más", "dos_pasos"),
    ],
    (4, 2): [
        ("unidad_razon", "total//(a+b)", "el tamaño de una unidad de la razón", "unidad_proporcional"),
        ("doble_a", "((total//(a+b))*a)*2", "el doble de la parte A", "reparto_proporcional"),
        ("triple_b", "((total//(a+b))*b)*3", "el triple de la parte B", "reparto_proporcional"),
        ("a_mas_dos", "((total//(a+b))*a)+2", "la parte A y dos unidades más", "dos_pasos"),
        ("b_mas_dos", "((total//(a+b))*b)+2", "la parte B y dos unidades más", "dos_pasos"),
        ("diferencia_mas_dos", "((total//(a+b))*b)-((total//(a+b))*a)+2", "la diferencia entre partes y dos unidades más", "comparar_reparto"),
    ],
    (4, 3): [
        ("doble_porcentaje_a", "((a*100)//(a+b))*2", "el doble del porcentaje del componente A", "porcentaje_razon"),
        ("mitad_porcentaje_a", "((a*100)//(a+b))//2", "la mitad del porcentaje del componente A", "porcentaje_razon"),
        ("porcentaje_b_mas_dos", "((b*100)//(a+b))+2", "el porcentaje del componente B y dos puntos más", "porcentaje_razon"),
        ("diferencia_porcentual", "((b*100)//(a+b))-((a*100)//(a+b))", "la diferencia entre los porcentajes de ambos componentes", "comparar_porcentajes"),
        ("complemento_a", "100-((a*100)//(a+b))", "el porcentaje que complementa al componente A", "complemento_porcentaje"),
        ("porcentaje_a_mas_dos", "((a*100)//(a+b))+2", "el porcentaje del componente A y dos puntos más", "porcentaje_razon"),
    ],
}


def _frame(modulo: int, nivel: int, instruction: str) -> str:
    starts = {
        (1, 1): "Una figura tiene {b} partes iguales y {a} están coloreadas.",
        (1, 2): "La fracción base es {a}/{b} y se amplifica por {c}.",
        (1, 3): "En una figura de {b} partes, {a} partes están coloreadas.",
        (2, 1): "Una colección de {total} objetos se organiza en {b} grupos iguales.",
        (2, 2): "De una colección de {total} objetos se considera la fracción {a}/{b}.",
        (2, 3): "De un total de {total} objetos se usa la fracción {a}/{b}.",
        (3, 1): "Una barra representa {a}% de un total de {total} unidades.",
        (3, 2): "Un precio de {total} tiene un descuento de {a}%.",
        (3, 3): "Un gráfico muestra los datos {a}, {b} y {c}.",
        (4, 1): "Una receta mantiene la razón {a}:{b} y usa el factor {c}.",
        (4, 2): "Una mezcla respeta la razón {a}:{b} y tiene {total} unidades en total.",
        (4, 3): "Una mezcla contiene {a} partes del componente A y {b} del componente B.",
    }
    return f"{starts[(modulo, nivel)]} ¿Cuánto es {instruction}?"


def build_extended_templates() -> list[dict]:
    magnitudes = {1: "fraccion_visual", 2: "fraccion_cantidad", 3: "porcentajes_promedios", 4: "razon_mezclas"}
    templates: list[dict] = []
    for (modulo, nivel), specs in _SPECS.items():
        for suffix, formula, instruction, habilidad in specs:
            templates.append({
                "id": f"tplx_m{modulo}_n{nivel}_{suffix}",
                "modulo_id": modulo,
                "nivel_id": nivel,
                "magnitud": magnitudes[modulo],
                "operacion_correcta": habilidad,
                "habilidad": habilidad,
                "incognita": suffix,
                "campos_requeridos": [],
                "formula": formula,
                "marcos_alternativos": [_frame(modulo, nivel, instruction)],
            })
    return templates
