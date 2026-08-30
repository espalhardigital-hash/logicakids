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
        ("partes_y_dos", "a+2", "las partes que resultan al agregar dos a las coloreadas", "comparar_cantidad"),
        ("producto_partes", "a*b", "el producto entre partes coloreadas y partes totales", "relacion_partes"),
        ("libres_y_dos", "(b-a)+2", "las partes que resultan al agregar dos a las que quedan libres", "complemento"),
    ],
    (1, 2): [
        ("factor_equivalencia", "c", "el factor común que conserva la fracción", "inferir_factor"),
        ("numerador_original", "a", "el numerador de la fracción original", "simplificar_inversa"),
        ("denominador_original", "b", "el denominador de la fracción original", "simplificar_inversa"),
        ("subdivisiones_por_parte", "c", "las partes nuevas que produce cada parte original", "leer_subdivision"),
        ("cortes_nuevos_coloreados", "a*(c-1)", "los cortes interiores añadidos en la zona coloreada", "contar_cortes"),
        ("cortes_nuevos_totales", "b*(c-1)", "los cortes interiores añadidos en toda la tira", "contar_cortes"),
        ("corregir_numerador", "a*c", "el numerador que corrige la equivalencia", "detectar_error"),
        ("corregir_denominador", "b*c", "el denominador que corrige la equivalencia", "detectar_error"),
        ("numerador_simplificado", "a", "el numerador después de simplificar", "simplificar"),
        ("denominador_simplificado", "b", "el denominador después de simplificar", "simplificar"),
    ],
    (1, 3): [
        ("triple_coloreadas", "a*3", "triple de las partes coloreadas", "transferencia_multiplicativa"),
        ("doble_complemento", "(b-a)*2", "doble de las partes sin colorear", "transferencia_complemento"),
        ("triple_complemento", "(b-a)*3", "triple de las partes sin colorear", "transferencia_complemento"),
        ("suma_partes", "a+b", "la suma entre partes coloreadas y totales", "interpretacion_datos"),
        ("producto_coloreadas_libres", "a*(b-a)", "el producto entre las partes coloreadas y las libres", "dos_datos"),
        ("complemento_mas_dos", "(b-a)+2", "las partes que resultan al agregar dos a las partes libres", "comparacion"),
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
        ("parte_mas_un_grupo", "(total//b)*(a+1)", "la cantidad conjunta de la fracción indicada y un grupo adicional", "fraccion_mas_unidad"),
        ("complemento_grupos", "(total//b)*(b-a)", "la parte complementaria de la colección", "complemento_fraccion"),
        ("doble_fraccion", "((total//b)*a)*2", "el doble de la fracción indicada", "doble_fraccion"),
        ("fraccion_mas_dos", "((total//b)*a)+2", "la fracción indicada y dos objetos adicionales", "dos_pasos"),
        ("triple_fraccion", "((total//b)*a)*3", "el triple de la fracción indicada", "triple_fraccion"),
        ("fraccion_mas_grupo", "((total//b)*a)+(total//b)", "la cantidad conjunta de la fracción indicada y un grupo adicional", "fraccion_mas_unidad"),
    ],
    (2, 3): [
        ("doble_parte", "((total//b)*a)*2", "el doble de la parte indicada", "transferencia_fraccion"),
        ("triple_parte", "((total//b)*a)*3", "el triple de la parte indicada", "transferencia_fraccion"),
        ("complemento_doble", "(total-((total//b)*a))*2", "el doble de lo que no se utiliza", "complemento"),
        ("parte_mas_dos", "((total//b)*a)+2", "la parte indicada y dos objetos adicionales", "dos_pasos"),
        ("complemento_mas_dos", "(total-((total//b)*a))+2", "lo que queda y dos objetos adicionales", "dos_pasos"),
        ("parte_mas_un_grupo", "((total//b)*a)+(total//b)", "la cantidad conjunta de la parte indicada y un grupo igual", "fraccion_mas_unidad"),
    ],
    (3, 1): [
        ("doble_porcentaje_cantidad", "((total*a)//100)*2", "el doble de la cantidad que representa el porcentaje", "porcentaje_cantidad"),
        ("cantidad_mas_diez", "((total*a)//100)+10", "la cantidad del porcentaje y diez unidades más", "dos_pasos"),
        ("total_mas_porcentaje", "total+((total*a)//100)", "la suma del total y la cantidad que representa el porcentaje", "aumento"),
        ("mitad_porcentaje", "((total*a)//100)//2", "la mitad de la cantidad que representa el porcentaje", "mitad_porcentaje"),
        ("complemento_transferencia", "total-((total*a)//100)", "la cantidad que falta para completar el total", "complemento_porcentaje"),
        ("porcentaje_mas_dos", "((total*a)//100)+2", "la cantidad del porcentaje y dos unidades más", "dos_pasos"),
    ],
    (3, 2): [
        ("doble_ahorro", "((total*a)//100)*2", "el doble del ahorro", "descuento_multietapa"),
        ("ahorro_mas_diez", "((total*a)//100)+10", "el ahorro y diez unidades más", "dos_pasos"),
        ("precio_mas_ahorro", "total+((total*a)//100)", "la suma del precio original y el ahorro calculado", "interpretacion_porcentaje"),
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
        ("doble_componente_a", "(a*c)*2", "el doble de la cantidad del primer ingrediente", "razon_escalada"),
        ("triple_componente_b", "(b*c)*3", "el triple de la cantidad del segundo ingrediente", "razon_escalada"),
        ("suma_componentes", "(a*c)+(b*c)", "la suma de ambos ingredientes", "total_razon"),
        ("diferencia_componentes", "(b*c)-(a*c)", "la diferencia entre ambos ingredientes", "comparar_razon"),
        ("a_mas_dos", "(a*c)+2", "el primer ingrediente con dos unidades extra", "dos_pasos"),
        ("b_mas_dos", "(b*c)+2", "el segundo ingrediente con dos unidades extra", "dos_pasos"),
    ],
    (4, 2): [
        ("unidad_razon", "total//(a+b)", "el tamaño de una porción base de la razón", "unidad_proporcional"),
        ("doble_a", "((total//(a+b))*a)*2", "el doble de la cantidad del ingrediente A", "reparto_proporcional"),
        ("triple_b", "((total//(a+b))*b)*3", "el triple de la cantidad del ingrediente B", "reparto_proporcional"),
        ("a_mas_dos", "((total//(a+b))*a)+2", "la cantidad del ingrediente A con dos unidades extra", "dos_pasos"),
        ("b_mas_dos", "((total//(a+b))*b)+2", "la cantidad del ingrediente B con dos unidades extra", "dos_pasos"),
        ("diferencia_mas_dos", "((total//(a+b))*b)-((total//(a+b))*a)+2", "la diferencia entre ingredientes con dos unidades extra", "comparar_reparto"),
    ],
    (4, 3): [
        ("doble_porcentaje_a", "((a*100)//(a+b))*2", "el doble del porcentaje del ingrediente A", "porcentaje_razon"),
        ("mitad_porcentaje_a", "((a*100)//(a+b))//2", "la mitad del porcentaje del ingrediente A", "porcentaje_razon"),
        ("porcentaje_b_mas_dos", "((b*100)//(a+b))+2", "el porcentaje del ingrediente B y dos puntos más", "porcentaje_razon"),
        ("diferencia_porcentual", "((b*100)//(a+b))-((a*100)//(a+b))", "la diferencia entre los porcentajes de ambos ingredientes", "comparar_porcentajes"),
        ("complemento_a", "100-((a*100)//(a+b))", "el porcentaje que falta para completar el 100%", "complemento_porcentaje"),
        ("porcentaje_a_mas_dos", "((a*100)//(a+b))+2", "el porcentaje del ingrediente A y dos puntos más", "porcentaje_razon"),
    ],
}

# Familias inspiradas en representaciones escolares habituales (tiras,
# colecciones, cuadrículas de cien y tablas de razón). No reproducen textos ni
# imágenes de las referencias: solo fijan una habilidad, una fórmula y un
# modelo visual original. Cada una cambia la representación que debe leer el
# alumno, por lo que añade variedad estructural y no una sustitución cosmética.
_REFERENCE_SPECS: dict[tuple[int, int], tuple[str, str, str, str, str]] = {
    (1, 1): ("tira_complemento", "b-a", "las partes que quedan sin colorear", "complemento_visual", "fraction_strip"),
    (1, 2): ("tira_equivalente", "a*c", "el número de partes coloreadas en la segunda tira", "comparar_representaciones", "equivalence_strip"),
    (1, 3): ("tira_comparacion", "(b-a)*2", "el doble de las partes sin colorear", "comparar_complemento", "fraction_strip"),
    (2, 1): ("grupos_iguales", "total//b", "la cantidad que hay en un grupo igual", "leer_grupos", "group_cards"),
    (2, 2): ("coleccion_fraccion", "(total//b)*a", "la cantidad que representa la fracción indicada", "fraccion_de_cantidad", "group_cards"),
    (2, 3): ("coleccion_complemento", "total-((total//b)*a)", "la cantidad que queda sin usar", "complemento_de_cantidad", "group_cards"),
    (3, 1): ("cuadricula_cien", "(total*a)//100", "la cantidad representada por el porcentaje", "porcentaje_cantidad", "hundred_grid"),
    (3, 2): ("descuento_cuadricula", "total-((total*a)//100)", "el precio después del descuento", "precio_con_descuento", "hundred_grid"),
    (3, 3): ("tabla_promedios", "(a+b+c)//3", "el promedio de los tres datos", "leer_tabla_y_promediar", "data_table"),
    (4, 1): ("tabla_razon_total", "(a*c)+(b*c)", "la cantidad total de la razón escalada", "escalar_razon", "ratio_table"),
    (4, 2): ("tabla_reparto", "(total//(a+b))*a", "la cantidad del componente A", "reparto_proporcional", "ratio_table"),
    (4, 3): ("tabla_porcentaje", "(a*100)//(a+b)", "el porcentaje del componente A", "razon_a_porcentaje", "ratio_table"),
}


def _pregunta_nominal(instruction: str) -> str:
    """Formula una pregunta concordante a partir de una incógnita nominal."""
    if instruction.startswith("las "):
        return f"¿Cuántas {instruction[4:]}?"
    if instruction.startswith("los "):
        return f"¿Cuántos {instruction[4:]}?"
    return f"¿Cuál es {instruction}?"


_STARTS = {
        (1, 1): "Una figura tiene {b} partes iguales; hay {a} partes coloreadas.",
        (1, 2): "La fracción base es {a}/{b} y se amplifica por {c}.",
        (1, 3): "En una figura de {b} partes, hay {a} partes coloreadas.",
        (2, 1): "Una colección de {total} objetos se organiza en {b} grupos iguales.",
        (2, 2): "De una colección de {total} objetos se considera la fracción {a}/{b}.",
        (2, 3): "De un total de {total} objetos se usa la fracción {a}/{b}.",
        (3, 1): "Una barra representa {a}% de un total de {total} unidades.",
        (3, 2): "Un precio de {total} tiene un descuento de {a}%.",
        (3, 3): "Un gráfico muestra los datos {a}, {b} y {c}.",
        (4, 1): "Una receta de cocina mantiene la razón {a}:{b} y se preparan {c} tandas iguales.",
        (4, 2): "Se prepara una mezcla de {total} unidades siguiendo la razón {a}:{b}.",
        (4, 3): "Un batido combina {a} vasos de frutilla y {b} vasos de leche (total: {total} vasos).",
}

_ALT_STARTS = {
    (1, 1): [
        "Un mosaico tiene {b} piezas iguales; hay {a} piezas marcadas.",
        "Una tira se divide en {b} secciones iguales; hay {a} secciones pintadas.",
        "Una ventana tiene {b} paneles iguales; hay {a} paneles decorados.",
        "Un jardín se divide en {b} parcelas iguales; hay {a} parcelas sembradas.",
    ],
    (1, 3): [
        "En un panel de {b} secciones, hay {a} secciones resaltadas.",
        "Una cinta tiene {b} tramos iguales; hay {a} tramos señalados.",
        "Una bandera tiene {b} franjas iguales; hay {a} franjas coloreadas.",
        "Un tablero se divide en {b} zonas iguales; hay {a} zonas ocupadas.",
    ],
    (2, 1): [
        "Una biblioteca organiza {total} libros en {b} estantes iguales.",
        "Un vivero distribuye {total} plantas en {b} bandejas iguales.",
        "Un club reparte {total} fichas en {b} equipos iguales.",
        "Una tienda acomoda {total} cajas en {b} filas iguales.",
    ],
    (2, 2): [
        "Una caja contiene {total} fichas y se estudia la fracción {a}/{b}.",
        "De {total} libros se selecciona la fracción {a}/{b}.",
        "De {total} semillas se planta la fracción {a}/{b}.",
        "Una colección tiene {total} tarjetas y se separa la fracción {a}/{b}.",
    ],
    (2, 3): [
        "Una actividad dispone de {total} fichas y utiliza la fracción {a}/{b}.",
        "De {total} materiales se reserva la fracción {a}/{b}.",
        "Un almacén tiene {total} cajas y despacha la fracción {a}/{b}.",
        "Una biblioteca reúne {total} libros y presta la fracción {a}/{b}.",
    ],
    (3, 1): [
        "En una colección de {total} unidades se identifica el {a}%.",
        "Un registro de {total} elementos destaca el {a}%.",
        "De {total} participantes se selecciona el {a}%.",
        "Un inventario de {total} piezas clasifica el {a}%.",
    ],
    (3, 2): [
        "Una mochila cuesta {total} soles y tiene un descuento de {a}%.",
        "Un juego educativo cuesta {total} soles y recibe una rebaja de {a}%.",
        "Una entrada al museo cuesta {total} soles y tiene una promoción de {a}%.",
        "Un libro cuesta {total} soles y se ofrece con un descuento de {a}%.",
    ],
    (3, 3): [
        "Una tabla contiene los registros {a}, {b} y {c}.",
        "Tres equipos obtienen {a}, {b} y {c} puntos.",
        "Tres lecturas duran {a}, {b} y {c} minutos.",
        "Tres grupos reúnen {a}, {b} y {c} fichas.",
    ],
    (4, 1): [
        "Para pintar un mural se mezclan témperas en razón {a}:{b} y se preparan {c} botes iguales.",
        "Un mosaico decorativo combina baldosas en razón {a}:{b} en {c} filas iguales.",
        "Un batido de frutas combina jugo y leche en razón {a}:{b} en {c} jarras iguales.",
        "Una masa de galletas mezcla ingredientes en razón {a}:{b} para {c} bandejas iguales.",
    ],
    (4, 2): [
        "Se reparten {total} fichas de juego entre dos amigos en razón {a}:{b}.",
        "Dos equipos reciben {total} puntos de premio en razón {a}:{b}.",
        "Para moldear plastilina se usan {total} gramos combinando dos colores en razón {a}:{b}.",
        "Dos salones se reparten {total} lápices de colores en razón {a}:{b}.",
    ],
    (4, 3): [
        "Un dibujo artístico combina {a} témperas azules y {b} témperas amarillas (total {total}).",
        "Una receta de galletas reúne {a} tazas de azúcar y {b} de harina (total {total} tazas).",
        "Una figura de plastilina mezcla {a} gramos verdes y {b} gramos blancos (total {total} g).",
        "Un jarabe frutal combina {a} ml de concentrado y {b} ml de agua (total {total} ml).",
    ],
}


def _frame_from_start(inicio: str, suffix: str, instruction: str) -> str:

    # Las operaciones de transferencia solo se publican si existe un propósito
    # narrativo explícito y amigable para un niño de 10 años.
    if "doble" in suffix:
        base = instruction.replace("el doble de ", "").replace("doble de ", "")
        return (
            f"{inicio} Al calcular {base}, se decide preparar el doble. "
            "¿Cuántas unidades se obtienen en total?"
        )
    if "triple" in suffix or "tres_" in suffix:
        base = instruction.replace("el triple de ", "").replace("triple de ", "")
        return (
            f"{inicio} Si necesitamos el triple de {base}, "
            "¿cuántas unidades se reúnen en total?"
        )
    if "cuatro" in suffix or "cuadruple" in suffix:
        return (
            f"{inicio} Si esa misma cantidad se necesita en cuatro grupos iguales, "
            "¿cuántas unidades abarcan esos cuatro grupos?"
        )
    if "mitad" in suffix:
        base = instruction
        if base.startswith("la mitad del "):
            base = "el " + base.removeprefix("la mitad del ")
        elif base.startswith("la mitad de la "):
            base = "la " + base.removeprefix("la mitad de la ")
        else:
            base = base.removeprefix("la mitad de ")
        return (
            f"{inicio} Si {base} se reparte en partes iguales entre dos amigos, "
            "¿cuántas unidades recibe cada uno?"
        )
    if "mas_diez" in suffix:
        return f"{inicio} Si a esa cantidad obtenida le sumamos 10 unidades extra, ¿cuántas unidades resultan en total?"
    if "mas_dos" in suffix or "mas_uno" in suffix:
        adicionales = 1 if "mas_uno" in suffix else 2
        return (
            f"{inicio} Si a esa cantidad obtenida le sumamos {adicionales} unidades extra, "
            "¿cuántas unidades resultan en total?"
        )
    return f"{inicio} {_pregunta_nominal(instruction)}"


def _frame(modulo: int, nivel: int, suffix: str, instruction: str) -> str:
    return _frame_from_start(_STARTS[(modulo, nivel)], suffix, instruction)


def _frames_transferencia(modulo: int, nivel: int, suffix: str, instruction: str) -> list[str]:
    """Tres situaciones distinguibles por familia, sin cambiar solo nombres o cifras."""
    inicios = [_STARTS[(modulo, nivel)], *_ALT_STARTS.get((modulo, nivel), [])]
    return [_frame_from_start(inicio, suffix, instruction) for inicio in inicios]


def _frames_equivalencia(suffix: str, instruction: str) -> list[str]:
    """Situaciones cognitivamente distintas para equivalencia de fracciones.

    El factor nunca se entrega junto con la operación pedida. El estudiante
    debe deducirlo comparando términos o leyendo la subdivisión visual.
    """
    frames = {
        "factor_equivalencia": [
            "Las fracciones {a}/{b} y {a_times_c}/{b_times_c} son equivalentes. ¿Por qué número se multiplicó cada término de la primera fracción?",
            "Una tira cambia de {a}/{b} a {a_times_c}/{b_times_c} sin cambiar la parte coloreada. ¿Cuántas partes nuevas se obtuvieron de cada parte original?",
            "En la tabla aparece {a}/{b} = {a_times_c}/{b_times_c}. ¿Cuál es el factor común que relaciona ambas fracciones?",
        ],
        "numerador_original": [
            "Completa la equivalencia ?/{b} = {a_times_c}/{b_times_c}. ¿Qué numerador tenía la fracción original?",
            "Una fracción se amplificó y produjo {a_times_c}/{b_times_c}. Si su denominador original era {b}, ¿cuál era su numerador?",
            "La segunda tira muestra {a_times_c}/{b_times_c}. La primera tenía {b} partes iguales. ¿Cuántas estaban coloreadas?",
        ],
        "denominador_original": [
            "Completa la equivalencia {a}/? = {a_times_c}/{b_times_c}. ¿Qué denominador tenía la fracción original?",
            "Una fracción se amplificó y produjo {a_times_c}/{b_times_c}. Si su numerador original era {a}, ¿cuál era su denominador?",
            "La segunda tira muestra {a_times_c}/{b_times_c}. La primera tenía {a} partes coloreadas. ¿En cuántas partes iguales estaba dividida?",
        ],
        "subdivisiones_por_parte": [
            "Una tira pasa de {b} partes iguales a {b_times_c} partes iguales sin cambiar su tamaño. ¿En cuántas partes nuevas se dividió cada parte original?",
            "La misma región se representa primero con {a}/{b} y luego con {a_times_c}/{b_times_c}. ¿Cuántas subdivisiones tiene ahora cada parte original?",
            "Observa las dos tiras equivalentes: una tiene {b} secciones y la otra {b_times_c}. ¿Cuántas secciones pequeñas corresponden a una sección original?",
        ],
        "cortes_nuevos_coloreados": [
            "La zona coloreada contiene {a} partes originales. Cada una se subdivide de modo que en total aparecen {a_times_c} partes coloreadas pequeñas. Sin contar los bordes que ya existían, ¿cuántos cortes interiores nuevos se añadieron en la zona coloreada?",
            "La zona coloreada pasa de {a} bloques a {a_times_c} bloques iguales. ¿Cuántas líneas divisorias nuevas se trazaron dentro de esos bloques?",
            "Compara las dos tiras. Para convertir {a} partes coloreadas en {a_times_c} partes pequeñas, ¿cuántos cortes adicionales se hicieron dentro de la región coloreada?",
        ],
        "cortes_nuevos_totales": [
            "Una tira tenía {b} partes iguales y ahora muestra {b_times_c}. Sin contar las divisiones originales, ¿cuántos cortes interiores nuevos se añadieron dentro de sus partes?",
            "Al subdividir una tira, sus {b} secciones se convierten en {b_times_c}. ¿Cuántas líneas divisorias nuevas se trazaron dentro de las secciones originales?",
            "Compara una tira de {b} partes con otra de {b_times_c} partes equivalentes. ¿Cuántos cortes adicionales aparecen dentro de las partes originales?",
        ],
        "corregir_numerador": [
            "Se escribió {a}/{b} = {a_times_c_plus_1}/{b_times_c}, pero la equivalencia es falsa. ¿Qué numerador debe reemplazar a {a_times_c_plus_1}?",
            "Un estudiante propuso {a_times_c_plus_1}/{b_times_c} como equivalente de {a}/{b}. El denominador es correcto, pero el numerador no. ¿Cuál es el numerador correcto?",
            "Revisa la segunda tira: para que represente la misma parte que {a}/{b} con denominador {b_times_c}, ¿qué numerador corrige el dato {a_times_c_plus_1}?",
        ],
        "corregir_denominador": [
            "Se escribió {a}/{b} = {a_times_c}/{b_times_c_minus_1}, pero la equivalencia es falsa. ¿Qué denominador debe reemplazar a {b_times_c_minus_1}?",
            "Un estudiante propuso {a_times_c}/{b_times_c_minus_1} como equivalente de {a}/{b}. El numerador es correcto, pero el denominador no. ¿Cuál es el denominador correcto?",
            "Revisa la segunda tira: para que represente la misma parte que {a}/{b} con numerador {a_times_c}, ¿qué denominador corrige el dato {b_times_c_minus_1}?",
        ],
        "numerador_simplificado": [
            "La fracción {a_times_c}/{b_times_c} se simplifica hasta tener denominador {b}. ¿Cuál es el numerador simplificado?",
            "Agrupa las partes pequeñas de {a_times_c}/{b_times_c} para volver a una tira con {b} partes. ¿Cuántas partes quedan coloreadas?",
            "Completa {a_times_c}/{b_times_c} = ?/{b}. ¿Qué número falta en el numerador?",
        ],
        "denominador_simplificado": [
            "La fracción {a_times_c}/{b_times_c} se simplifica hasta tener numerador {a}. ¿Cuál es el denominador simplificado?",
            "Agrupa las partes pequeñas de {a_times_c}/{b_times_c} para volver a una tira con {a} partes coloreadas. ¿Cuántas partes forman ahora el entero?",
            "Completa {a_times_c}/{b_times_c} = {a}/?. ¿Qué número falta en el denominador?",
        ],
    }
    return frames[suffix]


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
                "marcos_alternativos": (
                    _frames_equivalencia(suffix, instruction)
                    if (modulo, nivel) == (1, 2)
                    else _frames_transferencia(modulo, nivel, suffix, instruction)
                ),
            })

    for (modulo, nivel), (suffix, formula, instruction, habilidad, visual_model) in _REFERENCE_SPECS.items():
        templates.append({
            "id": f"tplr_m{modulo}_n{nivel}_{suffix}",
            "modulo_id": modulo,
            "nivel_id": nivel,
            "magnitud": magnitudes[modulo],
            "operacion_correcta": habilidad,
            "habilidad": habilidad,
            "incognita": suffix,
            "campos_requeridos": [],
            "formula": formula,
            "visual_model": visual_model,
            "marcos_alternativos": (
                [
                    "Dos tiras representan la misma parte. La primera muestra {a}/{b} y la segunda está dividida en {b_times_c} partes iguales. ¿Cuántas partes deben colorearse en la segunda tira?",
                    "Observa la tira de {a}/{b}. En otra tira equivalente hay {b_times_c} secciones del mismo tamaño. ¿Cuántas secciones deben quedar coloreadas?",
                ]
                if (modulo, nivel) == (1, 2)
                else [_frame(modulo, nivel, suffix, instruction)]
            ),
        })
    return templates
