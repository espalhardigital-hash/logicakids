import os
import re

seed_path = r"/app/app/fase5/seed.py"
with open(seed_path, 'r', encoding='utf-8') as f:
    content = f.read()

# M1L1 dict
content = content.replace(
    '"diccionario": {"Perímetro": "Es la suma de las longitudes de todos los lados que forman el borde de una figura."},',
    '"diccionario": {"Perímetro": "Es la suma de las longitudes de todos los lados que forman el borde de una figura.", "Lado": "Cada una de las líneas que forman una figura plana.", "Contorno": "Línea que marca el límite exterior de una figura."},'
)

# M1L2 dict
content = content.replace(
    '"diccionario": {"Lado (Arista)": "El segmento de línea que une dos esquinas de la figura."},',
    '"diccionario": {"Lado (Arista)": "El segmento de línea que une dos esquinas de la figura.", "Polígono": "Figura geométrica plana compuesta por una secuencia finita de segmentos rectos.", "Cuadrilátero": "Polígono de cuatro lados."},'
)

# M1L2 interactivos
content = content.replace(
    '{"pregunta": "Una figura tiene cuatro lados que miden: 2 cm, 3 cm, 2 cm y 3 cm. Perímetro:",',
    '{"pregunta": "Una figura tiene cuatro lados que miden: 2 cm, 3 cm, 2 cm y 3 cm. Perímetro:<br/>" + svg_rect_all_labels(3, 2, unit="cm"),'
)
content = content.replace(
    '{"pregunta": "Una estrella de 5 lados tiene cada lado de 1 m. Perímetro:",',
    '{"pregunta": "Un pentágono irregular tiene 5 lados y cada lado mide 1 m. Perímetro:<br/>" + svg_polygon_labeled([(10, 40), (20, 10), (30, 40), (25, 70), (15, 70)], [(15, 20, "1 m"), (25, 20, "1 m"), (35, 55, "1 m"), (20, 80, "1 m"), (5, 55, "1 m")], unit="m"),'
)
content = content.replace(
    '{"pregunta": "Un rectángulo mide 10 cm de largo y 5 cm de ancho. Perímetro:",',
    '{"pregunta": "Un rectángulo mide 10 cm de largo y 5 cm de ancho. Perímetro:<br/>" + svg_rect(10, 5, unit="cm"),'
)

# M1L3 dict
content = content.replace(
    '"diccionario": {"1 metro (m)": "Equivale a 100 centímetros (cm)", "1 kilómetro (km)": "Equivale a 1000 metros (m)"},',
    '"diccionario": {"1 metro (m)": "Equivale a 100 centímetros (cm)", "1 kilómetro (km)": "Equivale a 1000 metros (m)", "Unidad de longitud": "Cantidad estandarizada de longitud.", "Escalera de conversión": "Método visual para convertir unidades."},'
)
# M1L3 interactivos
content = content.replace(
    '{"pregunta": "¿Cuántos centímetros hay en 3 metros?",',
    '{"pregunta": "¿Cuántos centímetros hay en 3 metros?<br/>" + svg_rect(3, 1, unit="m"),'
)
content = content.replace(
    '{"pregunta": "¿Cuántos metros hay en 5 kilómetros?",',
    '{"pregunta": "¿Cuántos metros hay en 5 kilómetros?<br/>" + svg_rect(5, 1, unit="km"),'
)
content = content.replace(
    '{"pregunta": "¿Cuántos milímetros hay en 2 centímetros?",',
    '{"pregunta": "¿Cuántos milímetros hay en 2 centímetros?<br/>" + svg_rect(2, 1, unit="cm"),'
)

# M2L1 dict
content = content.replace(
    '"diccionario": {"Área": "La cantidad de espacio o cuadraditos que caben dentro del contorno de una figura."},',
    '"diccionario": {"Área": "La cantidad de espacio o cuadraditos que caben dentro del contorno de una figura.", "Unidad cuadrada": "Cuadrado cuyos lados miden 1 unidad.", "Base y altura": "Lados perpendiculares de un rectángulo."},'
)
content = content.replace(
    '{"pregunta": "Si un cuadrado mide 4x4 cm, ¿cuál es su área en cm²?",',
    '{"pregunta": "Si un cuadrado mide 4x4 cm, ¿cuál es su área en cm²?<br/>" + svg_shaded_rect(4, 4, unit="cm²"),'
)
content = content.replace(
    '{"pregunta": "Un rectángulo mide 5 cm de base y 2 cm de altura. Su área en cm² es:",',
    '{"pregunta": "Un rectángulo mide 5 cm de base y 2 cm de altura. Su área en cm² es:<br/>" + svg_shaded_rect(5, 2, unit="cm²"),'
)
content = content.replace(
    '{"pregunta": "Si pinto 3 filas de 3 cuadros (de 1 cm² cada uno), ¿cuál es el área total?",',
    '{"pregunta": "Si pinto 3 filas de 3 cuadros (de 1 cm² cada uno), ¿cuál es el área total?<br/>" + svg_shaded_rect(3, 3, unit="cm²"),'
)

# M2L2 dict
content = content.replace(
    '"diccionario": {"Fusión de áreas": "Juntar dos mitades de cuadrado para formar una unidad cuadrada entera."},',
    '"diccionario": {"Fusión de áreas": "Juntar dos mitades de cuadrado para formar una unidad cuadrada entera.", "Diagonal de un cuadrado": "Línea que une dos esquinas opuestas de un cuadrado.", "Triángulo rectángulo": "Triángulo con un ángulo de 90 grados."},'
)
content = content.replace(
    '{"pregunta": "Si tengo 4 cuadrados enteros de 1 cm² y 2 mitades. Área total en cm²:",',
    '{"pregunta": "Si tengo 4 cuadrados enteros de 1 cm² y 2 mitades. Área total en cm²:<br/>" + svg_grid_halves(4, 2, unit="cm²"),'
)
content = content.replace(
    '{"pregunta": "Figura con 0 enteros y 4 mitades de cm². Área en cm²:",',
    '{"pregunta": "Figura con 0 enteros y 4 mitades de cm². Área en cm²:<br/>" + svg_grid_halves(0, 4, unit="cm²"),'
)
content = content.replace(
    '{"pregunta": "Si tengo 10 enteros y 6 mitades, área total en cm²:",',
    '{"pregunta": "Si tengo 10 enteros y 6 mitades, área total en cm²:<br/>" + svg_grid_halves(10, 6, unit="cm²"),'
)

# M2L3 dict
content = content.replace(
    '"diccionario": {"Área irregular": "Figura que no tiene lados rectos ni formas clásicas predefinidas."},',
    '"diccionario": {"Área irregular": "Figura que no tiene lados rectos ni formas clásicas predefinidas.", "Aproximación": "Cálculo que no es exacto pero se acerca al valor real.", "Estimación": "Valor aproximado de una cantidad."},'
)
content = content.replace(
    '{"pregunta": "¿Cuánto es 8 enteros más 8 mitades en cm²?",',
    '{"pregunta": "¿Cuánto es 8 enteros más 8 mitades en cm²?<br/>" + svg_grid_halves(8, 8, unit="cm²"),'
)
content = content.replace(
    '{"pregunta": "¿Cuánto es 12 enteros más 2 mitades en cm²?",',
    '{"pregunta": "¿Cuánto es 12 enteros más 2 mitades en cm²?<br/>" + svg_grid_halves(12, 2, unit="cm²"),'
)
content = content.replace(
    '{"pregunta": "Si un polígono ocupa 5 enteros y 4 mitades, su área en cm² es:",',
    '{"pregunta": "Si un polígono ocupa 5 enteros y 4 mitades, su área en cm² es:<br/>" + svg_grid_halves(5, 4, unit="cm²"),'
)

# M3L1 dict
content = content.replace(
    '"diccionario": {"Descomponer": "Dividir una figura compleja en partes geométricas simples conocidas."},',
    '"diccionario": {"Descomponer": "Dividir una figura compleja en partes geométricas simples conocidas.", "Figura compuesta": "Figura formada por varias figuras simples.", "Superposición": "Poner una figura sobre otra."},'
)
content = content.replace(
    '{"pregunta": "Un rectángulo de 10 cm² y otro de 8 cm² pegados suman (en cm²):",',
    '{"pregunta": "Un rectángulo de 10 cm² y otro de 8 cm² pegados suman (en cm²):<br/>" + svg_l_shape(5, 2, 4, 2, unit="cm"),'
)
content = content.replace(
    '{"pregunta": "Figura T compuesta por un techo de 12 m² y una base de 4 m². Área total:",',
    '{"pregunta": "Figura T compuesta por un techo de 12 m² y una base de 4 m². Área total:<br/>" + svg_l_shape(6, 2, 2, 2, unit="m"),'
)
content = content.replace(
    '{"pregunta": "Una \'L\' de 15 cm² en el alto y 5 cm² en el piso. Total:",',
    '{"pregunta": "Una \'L\' de 15 cm² en el alto y 5 cm² en el piso. Total:<br/>" + svg_l_shape(5, 3, 5, 1, unit="cm"),'
)

# M3L2 dict
content = content.replace(
    '"diccionario": {"Conservación del área": "El área de un objeto no cambia cuando este cambia de forma o de posición."},',
    '"diccionario": {"Conservación del área": "El área de un objeto no cambia cuando este cambia de forma o de posición.", "Tangram": "Juego de 7 piezas que forman un cuadrado.", "Congruencia": "Dos figuras son iguales en forma y tamaño."},'
)
content = content.replace(
    '{"pregunta": "Si un triángulo de 3 cm² se rota, su nueva área es:",',
    '{"pregunta": "Si un triángulo de 3 cm² se rota, su nueva área es:<br/>" + svg_triangle_equilateral(3, unit="cm"),'
)
content = content.replace(
    '{"pregunta": "Corto un papel de 10 cm² en dos piezas. ¿Cuánto suman las dos piezas juntas?",',
    '{"pregunta": "Corto un papel de 10 cm² en dos piezas. ¿Cuánto suman las dos piezas juntas?<br/>" + svg_rect(5, 2, unit="cm"),'
)
content = content.replace(
    '{"pregunta": "Armo una casa con un Tangram de 16 cm². El área de la casa es:",',
    '{"pregunta": "Armo una casa con un Tangram de 16 cm². El área de la casa es:<br/>" + svg_square(4, unit="cm"),'
)

# M3L3 dict
content = content.replace(
    '"diccionario": {"Resta geométrica": "Resta del área total menos el área del hueco blanco."},',
    '"diccionario": {"Resta geométrica": "Resta del área total menos el área del hueco blanco.", "Área sombreada": "Parte coloreada de una figura.", "Figura hueca": "Figura con una parte interior vacía."},'
)
content = content.replace(
    '{"pregunta": "Área exterior 50 m², área interior en blanco 10 m². ¿Área pintada en m²?",',
    '{"pregunta": "Área exterior 50 m², área interior en blanco 10 m². ¿Área pintada en m²?<br/>" + svg_rect(10, 5, unit="m"),'
)
content = content.replace(
    '{"pregunta": "Caja de 100 cm² con agujero de 25 cm². Área restante:",',
    '{"pregunta": "Caja de 100 cm² con agujero de 25 cm². Área restante:<br/>" + svg_square(10, unit="cm"),'
)
content = content.replace(
    '{"pregunta": "Pared de 20 m² con ventana de 4 m². ¿Área a pintar?",',
    '{"pregunta": "Pared de 20 m² con ventana de 4 m². ¿Área a pintar?<br/>" + svg_rect(5, 4, unit="m"),'
)

# M3L4 dict
content = content.replace(
    '"diccionario": {"Eje de simetría": "Línea imaginaria que divide una figura en dos partes iguales que son reflejos una de otra."},',
    '"diccionario": {"Eje de simetría": "Línea imaginaria que divide una figura en dos partes iguales que son reflejos una de otra.", "Simetría axial": "Simetría respecto a un eje.", "Reflejo/Espejo": "Imagen que se forma al reflejarse en una superficie."},'
)
content = content.replace(
    '{"pregunta": "¿Cuántos ejes de simetría tiene un círculo (escribe: infinitos)?",',
    '{"pregunta": "¿Cuántos ejes de simetría tiene un círculo (escribe: infinitos)?<br/>" + svg_square(4, unit="cm"),'
)
content = content.replace(
    '{"pregunta": "¿Cuántos ejes de simetría tiene un cuadrado perfecto?",',
    '{"pregunta": "¿Cuántos ejes de simetría tiene un cuadrado perfecto?<br/>" + svg_square(4, unit="cm"),'
)
content = content.replace(
    '{"pregunta": "¿Cuántos ejes tiene un triángulo equilátero?",',
    '{"pregunta": "¿Cuántos ejes tiene un triángulo equilátero?<br/>" + svg_triangle_equilateral(3, unit="cm"),'
)

# M4L1 dict
content = content.replace(
    '"diccionario": {"Escala gráfica": "Barra dividida en segmentos que muestra la relación entre las distancias del plano y las reales."},',
    '"diccionario": {"Escala gráfica": "Barra dividida en segmentos que muestra la relación entre las distancias del plano y las reales.", "Distancia real": "Medida verdadera de un objeto en el mundo real.", "Proporción": "Relación de igualdad entre dos razones."},'
)
content = content.replace(
    '{"pregunta": "Escala 1 cm = 10m. Si un borde en el mapa mide 4 cm, ¿cuántos metros son?",',
    '{"pregunta": "Escala 1 cm = 10m. Si un borde en el mapa mide 4 cm, ¿cuántos metros son?<br/>" + svg_scale_bar(4, 10, unit="cm"),'
)
content = content.replace(
    '{"pregunta": "Escala 1 cm = 5km. Viajo 6 cm en el plano. ¿Distancia real en km?",',
    '{"pregunta": "Escala 1 cm = 5km. Viajo 6 cm en el plano. ¿Distancia real en km?<br/>" + svg_scale_bar(6, 5, unit="cm"),'
)
content = content.replace(
    '{"pregunta": "Escala 1 cm = 2m. Altura de 15 cm en el plano. ¿Altura real en metros?",',
    '{"pregunta": "Escala 1 cm = 2m. Altura de 15 cm en el plano. ¿Altura real en metros?<br/>" + svg_scale_bar(15, 2, unit="cm"),'
)

# M4L2 dict
content = content.replace(
    '"diccionario": {"Diagonal": "Segmento de recta que une dos vértices (esquinas) no consecutivos de un polígono."},',
    '"diccionario": {"Diagonal": "Segmento de recta que une dos vértices (esquinas) no consecutivos de un polígono.", "Teorema de Pitágoras": "En un triángulo rectángulo, el cuadrado de la hipotenusa es la suma de los cuadrados de los catetos.", "Hipotenusa": "El lado más largo de un triángulo rectángulo."},'
)
content = content.replace(
    '{"pregunta": "Si un monitor se anuncia como \'24 pulgadas\', ¿qué mide 24 pulgadas? (escribe: la diagonal)",',
    '{"pregunta": "Si un monitor se anuncia como \'24 pulgadas\', ¿qué mide 24 pulgadas? (escribe: la diagonal)<br/>" + svg_rect_diagonal(20, 12, diag_label="24 pulg", unit="pulg"),'
)
content = content.replace(
    '{"pregunta": "En un rectángulo de 3x4, ¿la diagonal mide 5? (Escribe 1 para SÍ, 2 para NO)",',
    '{"pregunta": "En un rectángulo de 3x4, ¿la diagonal mide 5? (Escribe 1 para SÍ, 2 para NO)<br/>" + svg_rect_diagonal(4, 3, diag_label="5", unit="cm"),'
)
content = content.replace(
    '{"pregunta": "¿Qué es más largo en un TV, la base o la diagonal? (escribe: diagonal)",',
    '{"pregunta": "¿Qué es más largo en un TV, la base o la diagonal? (escribe: diagonal)<br/>" + svg_rect_diagonal(16, 9, diag_label="?", unit="cm"),'
)

# M4L3 dict
content = content.replace(
    '"diccionario": {"Metro cuadrado (m²)": "Área de un cuadrado que mide 1 metro de lado (equivalente a 10,000 cm²)."},',
    '"diccionario": {"Metro cuadrado (m²)": "Área de un cuadrado que mide 1 metro de lado (equivalente a 10,000 cm²).", "Centímetro cuadrado (cm²)": "Unidad de área de 1 cm x 1 cm.", "Decímetro cuadrado (dm²)": "Unidad de área de 10 cm x 10 cm."},'
)
content = content.replace(
    '{"pregunta": "¿Cuántos cm² hay en 2 m²?",',
    '{"pregunta": "¿Cuántos cm² hay en 2 m²?<br/>" + svg_rect(2, 1, unit="m²"),'
)
content = content.replace(
    '{"pregunta": "Si una caja tiene 3 m², ¿cuántos cm² tiene?",',
    '{"pregunta": "Si una caja tiene 3 m², ¿cuántos cm² tiene?<br/>" + svg_rect(3, 1, unit="m²"),'
)
content = content.replace(
    '{"pregunta": "Un terreno de 5 m² equivale en cm² a:",',
    '{"pregunta": "Un terreno de 5 m² equivale en cm² a:<br/>" + svg_rect(5, 1, unit="m²"),'
)

# M4L2 theory text addition
content = content.replace(
    '"texto_descubrimiento": "Cuando compramos una pantalla de televisión, de celular o tablet, nos dicen su tamaño en pulgadas (por ejemplo, 32 pulgadas o 50 pulgadas).\\n¡Pero esa medida no es el ancho ni el alto! El tamaño de las pantallas siempre se mide en línea recta cruzando desde una esquina hasta la esquina contraria. ¡Eso es la diagonal!",',
    '"texto_descubrimiento": "Cuando compramos una pantalla de televisión, de celular o tablet, nos dicen su tamaño en pulgadas (por ejemplo, 32 pulgadas o 50 pulgadas).\\n¡Pero esa medida no es el ancho ni el alto! El tamaño de las pantallas siempre se mide en línea recta cruzando desde una esquina hasta la esquina contraria. ¡Eso es la diagonal!\\n¿Sabías que existe una fórmula mágica para calcular la diagonal sin medirla directamente? Se llama el Teorema de Pitágoras: si conocemos la base y la altura de un rectángulo, la diagonal al cuadrado es igual a la suma de la base al cuadrado más la altura al cuadrado (diagonal² = base² + altura²). Por ejemplo, si la base mide 3 y la altura mide 4: 3² + 4² = 9 + 16 = 25, y la raíz cuadrada de 25 es 5. ¡La diagonal mide 5!",'
)

with open(seed_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Update applied successfully")
