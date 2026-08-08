"""
Script de Enriquecimiento: 12 Marcos Narrativos Alternativos para las 72 Plantillas de la Fase 4
"""

import json
import os

def generate_12_frames(p):
    formula = p.get("formula", "")
    magnitud = p.get("magnitud", "dinero")
    op = p.get("operacion_correcta", "multiplicar")
    pid = p.get("id", "")
    
    # Marcos base por tipo de fórmula y magnitud
    if formula in ("a+b", "a+b+c"):
        if magnitud == "dinero":
            return [
                "En {lugar}, {personaje} compró {objetos_0} por {unidad} {a} y {objetos_1} por {unidad} {b}.",
                "Durante su visita a {lugar}, {personaje} gastó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "Para la clase de arte en {lugar}, {personaje} pagó {unidad} {a} por {objetos_0} y {unidad} {b} por {objetos_1}.",
                "Organizando la fiesta en {lugar}, {personaje} abonó {unidad} {a} de {objetos_0} y {unidad} {b} de {objetos_1}.",
                "En el taller escolar de {lugar}, {personaje} juntó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "Ayudando en {lugar}, {personaje} destinó {unidad} {a} a {objetos_0} y {unidad} {b} a {objetos_1}.",
                "En el club de robótica en {lugar}, {personaje} adquirió {objetos_0} a {unidad} {a} y {objetos_1} a {unidad} {b}.",
                "En las compras para el viaje en {lugar}, {personaje} abonó {unidad} {a} de {objetos_0} más {unidad} {b} de {objetos_1}.",
                "Cuidando a su mascota en {lugar}, {personaje} compró {objetos_0} por {unidad} {a} y {objetos_1} por {unidad} {b}.",
                "En el concurso de {lugar}, {personaje} sumó {unidad} {a} por {objetos_0} y {unidad} {b} por {objetos_1}.",
                "Para la feria científica en {lugar}, {personaje} reservó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "En el ensayo musical en {lugar}, {personaje} gastó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}."
            ]
        elif magnitud == "masa":
            return [
                "En {lugar}, {personaje} colocó en la balanza {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Cocinando una receta en {lugar}, {personaje} pesó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Para el proyecto de ciencias en {lugar}, {personaje} mezcló {a} {unidad} de {objetos_0} con {b} {unidad} de {objetos_1}.",
                "Ayudando en {lugar}, {personaje} empacó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En el huerto escolar de {lugar}, {personaje} cosechó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Durante la jornada en {lugar}, {personaje} transportó {a} {unidad} de {objetos_0} más {b} {unidad} de {objetos_1}.",
                "En el taller de {lugar}, {personaje} preparó una carga de {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Organizando la despensa en {lugar}, {personaje} acomodó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Cuidando los animales en {lugar}, {personaje} sirvió {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En la feria de {lugar}, {personaje} juntó {a} {unidad} de {objetos_0} junto a {b} {unidad} de {objetos_1}.",
                "En la actividad del club en {lugar}, {personaje} pesó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Para la merienda en {lugar}, {personaje} reunió {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}."
            ]
        else: # longitud
            return [
                "En {lugar}, {personaje} unió un tramo de {objeto_medible} de {a} {unidad} con otro de {b} {unidad}.",
                "Para la clase de arte en {lugar}, {personaje} cortó dos tiras de {objeto_medible}: una de {a} {unidad} y otra de {b} {unidad}.",
                "En el proyecto escolar de {lugar}, {personaje} midió {a} {unidad} de {objeto_medible} y agregó {b} {unidad} más.",
                "Durante el entrenamiento deportivo en {lugar}, {personaje} recorrió {a} {unidad} y luego {b} {unidad} adicionales.",
                "Trabajando en el taller de {lugar}, {personaje} ensambló dos partes de {objeto_medible}: {a} {unidad} y {b} {unidad}.",
                "En el huerto escolar de {lugar}, {personaje} colocó {a} {unidad} de {objeto_medible} y {b} {unidad} más.",
                "Haciendo un trabajo manual en {lugar}, {personaje} juntó {a} {unidad} de {objeto_medible} con {b} {unidad}.",
                "En el club de robótica de {lugar}, {personaje} conectó {a} {unidad} de {objeto_medible} y {b} {unidad}.",
                "Organizando el evento en {lugar}, {personaje} desplegó {a} {unidad} de {objeto_medible} más {b} {unidad}.",
                "En la excursión al aire libre por {lugar}, {personaje} caminó {a} {unidad} en la primera etapa y {b} {unidad} en la segunda.",
                "Cuidando el espacio en {lugar}, {personaje} cercó {a} {unidad} de {objeto_medible} y luego {b} {unidad}.",
                "En el ensayo en {lugar}, {personaje} extendió {a} {unidad} de {objeto_medible} junto a {b} {unidad}."
            ]

    elif formula in ("total-a", "total-a-b", "a-b", "a-b/100", "a*1000-b"):
        if magnitud == "dinero":
            return [
                "En {lugar}, {personaje} llevaba {total} {unidad}. Compró {objetos_0} por {unidad} {a}.",
                "De visita en {lugar}, {personaje} tenía {total} {unidad} y abonó {unidad} {a} por {objetos_0}.",
                "Para la salida escolar a {lugar}, {personaje} llevó {total} {unidad} y gastó {unidad} {a} en {objetos_0}.",
                "En la feria de {lugar}, {personaje} disponía de {total} {unidad} y pagó {unidad} {a} por {objetos_0}.",
                "Organizando sus ahorros en {lugar}, {personaje} separó {total} {unidad} y usó {unidad} {a} en {objetos_0}.",
                "En la cafetería de {lugar}, {personaje} pagó con un billete de {total} {unidad} una compra de {unidad} {a}.",
                "Durante el festival en {lugar}, {personaje} reservó {total} {unidad} y consumió {unidad} {a} en {objetos_0}.",
                "En el taller de {lugar}, {personaje} tenía {total} {unidad} de presupuesto y gastó {unidad} {a} en materiales.",
                "Para el regalo de cumpleaños en {lugar}, {personaje} aportó {total} {unidad} y compró un artículo de {unidad} {a}.",
                "En el quiosco de {lugar}, {personaje} entregó {total} {unidad} para pagar una merienda de {unidad} {a}.",
                "Cuidando su dinero en {lugar}, {personaje} guardó {total} {unidad} y destinó {unidad} {a} a {objetos_0}.",
                "En la librería de {lugar}, {personaje} abonó una cuenta con {total} {unidad} tras comprar útiles por {unidad} {a}."
            ]
        elif magnitud == "masa":
            return [
                "En {lugar}, {personaje} tenía un paquete de {objeto_medible} de {total} {unidad} y retiró {a} {unidad}.",
                "Cocinando en {lugar}, {personaje} tenía {total} {unidad} de {objeto_medible} y usó {a} {unidad} para la receta.",
                "En el proyecto de ciencias en {lugar}, {personaje} separó {a} {unidad} de una reserva total de {total} {unidad} de {objeto_medible}.",
                "Ayudando en la despensa de {lugar}, {personaje} tomó {a} {unidad} de un saco de {total} {unidad} de {objeto_medible}.",
                "En el huerto de {lugar}, {personaje} cosechó {total} {unidad} de {objeto_medible} y entregó {a} {unidad}.",
                "Durante la actividad en {lugar}, {personaje} pesó {total} {unidad} de {objeto_medible} y apartó {a} {unidad}.",
                "En el taller de {lugar}, {personaje} utilizó {a} {unidad} de una carga de {total} {unidad} de {objeto_medible}.",
                "Para alimentar a las mascotas en {lugar}, {personaje} usó {a} {unidad} de un lote de {total} {unidad} de {objeto_medible}.",
                "Organizando los insumos en {lugar}, {personaje} distribuyó {a} {unidad} de un recipiente de {total} {unidad} de {objeto_medible}.",
                "En la feria de {lugar}, {personaje} vendió {a} {unidad} de una caja con {total} {unidad} de {objeto_medible}.",
                "En el club de {lugar}, {personaje} restó {a} {unidad} a un contenedor de {total} {unidad} de {objeto_medible}.",
                "Para la preparación en {lugar}, {personaje} extrajo {a} {unidad} de una reserva de {total} {unidad} de {objeto_medible}."
            ]
        else: # longitud
            return [
                "En {lugar}, {personaje} tenía una tira de {objeto_medible} de {total} {unidad} y cortó un trozo de {a} {unidad}.",
                "Para la clase de arte en {lugar}, {personaje} usó {a} {unidad} de un rollo de {objeto_medible} de {total} {unidad}.",
                "En el proyecto escolar de {lugar}, {personaje} recortó {a} {unidad} a una pieza de {objeto_medible} de {total} {unidad}.",
                "Durante el entrenamiento en {lugar}, {personaje} debía recorrer {total} {unidad} y ya avanzó {a} {unidad}.",
                "Trabajando en el taller de {lugar}, {personaje} separó {a} {unidad} de una barra de {objeto_medible} de {total} {unidad}.",
                "En el huerto escolar de {lugar}, {personaje} instaló {a} {unidad} de una manguera de {total} {unidad} de {objeto_medible}.",
                "Haciendo manualidades en {lugar}, {personaje} le quitó {a} {unidad} a una cinta de {objeto_medible} de {total} {unidad}.",
                "En el club de robótica de {lugar}, {personaje} recortó {a} {unidad} de un cable de {objeto_medible} de {total} {unidad}.",
                "Organizando la cerca en {lugar}, {personaje} colocó {a} {unidad} de un tramo total de {total} {unidad} de {objeto_medible}.",
                "En la excursión por {lugar}, {personaje} caminó {a} {unidad} de una ruta fijada de {total} {unidad}.",
                "Cuidando el material en {lugar}, {personaje} tomó {a} {unidad} de un carrete de {objeto_medible} de {total} {unidad}.",
                "En el ensayo en {lugar}, {personaje} desplegó {a} {unidad} de los {total} {unidad} de {objeto_medible} disponibles."
            ]

    elif formula in ("a*n_cant", "a*b", "a*b*c"):
        if magnitud == "dinero":
            return [
                "En {lugar}, {personaje} compró {n_cant} paquetes de {objetos_0} a {unidad} {a} cada uno.",
                "De visita en {lugar}, {personaje} adquirió {n_cant} unidades de {objetos_0} por {unidad} {a} cada una.",
                "Para la clase de arte en {lugar}, {personaje} compró {n_cant} artículos de {objetos_0} a {unidad} {a} la unidad.",
                "Organizando la fiesta en {lugar}, {personaje} reservó {n_cant} recuerdos de {objetos_0} a {unidad} {a} cada uno.",
                "En la papelería de {lugar}, {personaje} abonó {n_cant} materiales de {objetos_0} por {unidad} {a} cada uno.",
                "Ayudando en {lugar}, {personaje} compró {n_cant} porciones de {objetos_0} a {unidad} {a} cada una.",
                "En el club de robótica en {lugar}, {personaje} adquirió {n_cant} componentes de {objetos_0} a {unidad} {a} cada uno.",
                "Para la excursión escolar en {lugar}, {personaje} pagó {n_cant} tickets de {objetos_0} a {unidad} {a} cada uno.",
                "Cuidando sus gastos en {lugar}, {personaje} compró {n_cant} bolsas de {objetos_0} por {unidad} {a} cada una.",
                "En el festival de {lugar}, {personaje} abonó {n_cant} fichas de {objetos_0} a {unidad} {a} cada una.",
                "Para el proyecto de ciencias en {lugar}, {personaje} encargó {n_cant} recipientes de {objetos_0} a {unidad} {a} cada uno.",
                "En el ensayo musical en {lugar}, {personaje} compró {n_cant} repuestos de {objetos_0} a {unidad} {a} cada uno."
            ]
        elif magnitud == "masa":
            return [
                "Cada caja de {objetos_0} en {lugar} pesa {a} {unidad}. {personaje} transporta {n_cant} cajas.",
                "Cocinando en {lugar}, {personaje} utilizó {n_cant} porciones de {objetos_0} de {a} {unidad} cada una.",
                "Para el experimento en {lugar}, {personaje} pesó {n_cant} envases de {objetos_0} de {a} {unidad} cada uno.",
                "Ayudando en la despensa de {lugar}, {personaje} cargó {n_cant} bolsas de {objetos_0} de {a} {unidad} cada una.",
                "En el huerto escolar de {lugar}, {personaje} cosechó {n_cant} cestas de {objetos_0} de {a} {unidad} cada una.",
                "Durante el trabajo en {lugar}, {personaje} acomodó {n_cant} paquetes de {objetos_0} de {a} {unidad} cada uno.",
                "En el taller de {lugar}, {personaje} preparó {n_cant} recipientes de {objetos_0} de {a} {unidad} cada uno.",
                "Cuidando a las mascotas en {lugar}, {personaje} repartió {n_cant} raciones de {objetos_0} de {a} {unidad} cada una.",
                "Organizando los insumos en {lugar}, {personaje} pesó {n_cant} sacos de {objetos_0} de {a} {unidad} cada uno.",
                "En la feria de {lugar}, {personaje} empaquetó {n_cant} lotes de {objetos_0} de {a} {unidad} cada uno.",
                "En el club deportivo de {lugar}, {personaje} transportó {n_cant} equipamientos de {objetos_0} de {a} {unidad} cada uno.",
                "Para la preparación en {lugar}, {personaje} juntó {n_cant} bloques de {objetos_0} de {a} {unidad} cada uno."
            ]
        else: # longitud
            return [
                "En {lugar}, {personaje} necesita {n_cant} piezas de {objeto_medible}. Cada pieza mide {a} {unidad}.",
                "Para la clase de arte en {lugar}, {personaje} cortó {n_cant} tiras de {objeto_medible} de {a} {unidad} cada una.",
                "En el proyecto escolar de {lugar}, {personaje} midió {n_cant} trozos de {objeto_medible} de {a} {unidad} cada uno.",
                "Durante el entrenamiento deportivo en {lugar}, {personaje} recorrió {n_cant} tramos de {a} {unidad} cada uno.",
                "Trabajando en el taller de {lugar}, {personaje} ensambló {n_cant} barras de {objeto_medible} de {a} {unidad} cada una.",
                "En el huerto escolar de {lugar}, {personaje} colocó {n_cant} estacas de {objeto_medible} de {a} {unidad} cada una.",
                "Haciendo manualidades en {lugar}, {personaje} recortó {n_cant} secciones de {objeto_medible} de {a} {unidad} cada una.",
                "En el club de robótica de {lugar}, {personaje} usó {n_cant} cables de {objeto_medible} de {a} {unidad} cada uno.",
                "Organizando el cerco en {lugar}, {personaje} midió {n_cant} lados de {objeto_medible} de {a} {unidad} cada uno.",
                "En la excursión al aire libre por {lugar}, {personaje} avanzó {n_cant} etapas de {a} {unidad} cada una.",
                "Cuidando el espacio en {lugar}, {personaje} extendió {n_cant} rollos de {objeto_medible} de {a} {unidad} cada uno.",
                "En el ensayo en {lugar}, {personaje} unió {n_cant} varillas de {objeto_medible} de {a} {unidad} cada una."
            ]

    elif formula in ("total/a", "a/n_cant", "a/b", "(total-c)/n_cant"):
        if magnitud == "dinero":
            return [
                "En {lugar}, {personaje} gastó {total} {unidad} en {n_cant} paquetes de {objetos_0} iguales.",
                "De visita en {lugar}, {personaje} pagó un total de {unidad} {total} por {n_cant} artículos iguales de {objetos_0}.",
                "Para la clase de arte en {lugar}, {personaje} abonó {total} {unidad} por {n_cant} suministros de {objetos_0} idénticos.",
                "Organizando la fiesta en {lugar}, {personaje} repartió un presupuesto de {unidad} {total} entre {n_cant} bolsas iguales.",
                "En la papelería de {lugar}, {personaje} pagó {total} {unidad} al comprar {n_cant} útiles de {objetos_0} idénticos.",
                "Ayudando a su grupo en {lugar}, {personaje} dividió una cuenta de {unidad} {total} entre {n_cant} personas por igual.",
                "En el club de robótica en {lugar}, {personaje} adquirió {n_cant} piezas iguales por un monto total de {unidad} {total}.",
                "Para la salida de excursión en {lugar}, {personaje} juntó {total} {unidad} vendiendo {n_cant} tickets iguales.",
                "Cuidando la caja en {lugar}, {personaje} repartió un fondo de {total} {unidad} en {n_cant} partes iguales.",
                "En el concurso de {lugar}, {personaje} distribuyó un premio de {unidad} {total} entre {n_cant} ganadores por igual.",
                "Para el proyecto escolar en {lugar}, {personaje} pagó {total} {unidad} por {n_cant} cajas idénticas de {objetos_0}.",
                "En el ensayo musical en {lugar}, {personaje} invirtió {total} {unidad} en {n_cant} accesorios idénticos de {objetos_0}."
            ]
        elif magnitud == "masa":
            return [
                "En {lugar}, {personaje} tiene un cargamento de {total} {unidad} de {objeto_medible} repartido en {n_cant} cajas iguales.",
                "Cocinando en {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} porciones iguales.",
                "Para el experimento en {lugar}, {personaje} separó {total} {unidad} de {objeto_medible} en {n_cant} frascos idénticos.",
                "Ayudando en la despensa de {lugar}, {personaje} distribuyó {total} {unidad} de {objeto_medible} en {n_cant} bolsas iguales.",
                "En el huerto de {lugar}, {personaje} repartió una cosecha de {total} {unidad} de {objeto_medible} entre {n_cant} cestas iguales.",
                "Durante el trabajo en {lugar}, {personaje} empaquetó {total} {unidad} de {objeto_medible} en {n_cant} cajas de igual peso.",
                "En el taller de {lugar}, {personaje} fraccionó una carga de {total} {unidad} de {objeto_medible} en {n_cant} envases iguales.",
                "Para alimentar las mascotas en {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} platos iguales.",
                "Organizando los insumos en {lugar}, {personaje} pesó {total} {unidad} de {objeto_medible} en {n_cant} lotes idénticos.",
                "En la feria de {lugar}, {personaje} empaquetó {total} {unidad} de {objeto_medible} en {n_cant} paquetes del mismo peso.",
                "En el club deportivo de {lugar}, {personaje} repartió {total} {unidad} de {objeto_medible} en {n_cant} maletas iguales.",
                "Para la preparación en {lugar}, {personaje} fraccionó {total} {unidad} de {objeto_medible} entre {n_cant} recipientes iguales."
            ]
        else: # longitud
            return [
                "En {lugar}, {personaje} tiene una tira de {objeto_medible} de {total} {unidad} y la cortó en {n_cant} trozos iguales.",
                "Para la clase de arte en {lugar}, {personaje} dividió un rollo de {objeto_medible} de {total} {unidad} en {n_cant} partes iguales.",
                "En el proyecto escolar de {lugar}, {personaje} recortó una pieza de {objeto_medible} de {total} {unidad} en {n_cant} tiras iguales.",
                "Durante el entrenamiento en {lugar}, {personaje} dividió un recorrido de {total} {unidad} en {n_cant} etapas idénticas.",
                "Trabajando en el taller de {lugar}, {personaje} cortó una barra de {objeto_medible} de {total} {unidad} en {n_cant} tramos iguales.",
                "En el huerto escolar de {lugar}, {personaje} repartió {total} {unidad} de {objeto_medible} en {n_cant} hileras iguales.",
                "Haciendo manualidades en {lugar}, {personaje} dividió una cinta de {objeto_medible} de {total} {unidad} en {n_cant} secciones iguales.",
                "En el club de robótica de {lugar}, {personaje} separó {total} {unidad} de {objeto_medible} en {n_cant} cables iguales.",
                "Organizando la cerca en {lugar}, {personaje} repartió {total} {unidad} de {objeto_medible} en {n_cant} lados idénticos.",
                "En la excursión al aire libre por {lugar}, {personaje} dividió la ruta de {total} {unidad} en {n_cant} tramos iguales.",
                "Cuidando el material en {lugar}, {personaje} fraccionó un carrete de {objeto_medible} de {total} {unidad} en {n_cant} partes del mismo largo.",
                "En el ensayo en {lugar}, {personaje} cortó {total} {unidad} de {objeto_medible} en {n_cant} varillas del mismo tamaño."
            ]
    else:
        # Fallback 12 marcos genéricos si no encaja en las anteriores
        return [
            "En {lugar}, {personaje} analiza los datos de {objeto_medible}.",
            "Durante la actividad en {lugar}, {personaje} registra las medidas de {objeto_medible}.",
            "En la clase de matemáticas en {lugar}, {personaje} calcula las cantidades de {objeto_medible}.",
            "Trabajando en {lugar}, {personaje} toma nota de las cifras de {objeto_medible}.",
            "En su proyecto personal en {lugar}, {personaje} revisa los números de {objeto_medible}.",
            "De visita en {lugar}, {personaje} comprueba las dimensiones de {objeto_medible}.",
            "Organizando su tarea en {lugar}, {personaje} evalúa los valores de {objeto_medible}.",
            "En el taller escolar de {lugar}, {personaje} verifica el inventario de {objeto_medible}.",
            "Para su presentación en {lugar}, {personaje} compara las medidas de {objeto_medible}.",
            "Durante su jornada en {lugar}, {personaje} anota los resultados de {objeto_medible}.",
            "En el club de ciencias de {lugar}, {personaje} mide cuidadosamente {objeto_medible}.",
            "Ayudando en {lugar}, {personaje} resume las cantidades observadas de {objeto_medible}."
        ]

def run():
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(backend_dir, "app", "fase4", "data")
    plantillas_path = os.path.join(data_dir, "plantillas_fase4.json")
    
    with open(plantillas_path, "r", encoding="utf-8") as f:
        plantillas = json.load(f)
        
    print(f"[*] Procesando {len(plantillas)} plantillas para asignar 12 marcos alternativos...")
    
    for p in plantillas:
        # Corregir fórmulas e incógnitas de división si era m3_esq4
        if p.get("id") in ("m3_n1_esq4_div_dividendo", "m3_n2_esq4_div_dividendo", "m3_n3_esq4_div_dividendo"):
            p["formula"] = "total/a"
            p["operacion_correcta"] = "dividir"
            p["incognita"] = "factor_multiplicativo"
            
        p["marcos_alternativos"] = generate_12_frames(p)
        
    with open(plantillas_path, "w", encoding="utf-8") as f:
        json.dump(plantillas, f, ensure_ascii=False, indent=2)
        
    print("✅ ¡Las 72 plantillas ahora cuentan con 12 marcos narrativos alternativos!")

if __name__ == "__main__":
    run()
