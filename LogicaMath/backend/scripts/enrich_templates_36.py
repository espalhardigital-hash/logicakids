"""
Script de Enriquecimiento: 36 Marcos Narrativos Alternativos para las 72 Plantillas de la Fase 4
"""

import json
import os

def generate_36_frames(p):
    """Punto de entrada: genera 36 marcos y los sanea (Bugs #4 y #5) antes de
    devolverlos. El Módulo 4 (conversión de unidades) tiene reglas propias
    porque sus fórmulas representan un salto de escala, no las mismas
    operaciones "total menos a" / "a más b" que asumen las reglas genéricas
    de abajo (pensadas para dinero/masa/longitud de los módulos 1-3)."""
    if p.get("modulo_id") == 4:
        return _sanitize_frames(_generate_36_frames_modulo4(p))
    return _sanitize_frames(_generate_36_frames_generico(p))


def _generate_36_frames_generico(p):
    formula = p.get("formula", "")
    magnitud = p.get("magnitud", "dinero")
    pid = p.get("id", "")

    if pid == "m1_n2_esq2_diferencia_pesos":
        return _frames_m1_n2_esq2_diferencia_pesos()

    if formula == "a+b-c":
        if magnitud == "temperatura":
            return [
                "En {lugar}, la temperatura de {objeto_medible} era de {a} {unidad}. Subió {b} {unidad} y luego bajó {c} {unidad}.",
                "En {lugar}, {personaje} registró que {objeto_medible} tenía {a} {unidad}. Subió {b} {unidad} al mediodía y bajó {c} {unidad} por la noche.",
                "En {lugar}, {personaje} anotó {a} {unidad} en {objeto_medible} al amanecer. Subió {b} {unidad} y luego bajó {c} {unidad}.",
                "En {lugar}, {personaje} controló {objeto_medible}: partió de {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} midió {objeto_medible} a las 8: {a} {unidad}. Subió {b} {unidad} al mediodía y bajó {c} {unidad} a la noche.",
                "En {lugar}, {personaje} vigiló {objeto_medible} durante el día: comenzó en {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} tomó nota de {objeto_medible}: {a} {unidad} al inicio, subió {b} {unidad} y bajó {c} {unidad} después.",
                "En {lugar}, {personaje} revisó {objeto_medible} tres veces: {a} {unidad}, luego subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} llevó el registro de {objeto_medible}: partió de {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} observó {objeto_medible}: {a} {unidad} por la mañana, subió {b} {unidad} y bajó {c} {unidad} por la tarde.",
                "En {lugar}, {personaje} anotó en la planilla de {objeto_medible}: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} controló dos veces {objeto_medible}: comenzó en {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} siguió de cerca {objeto_medible}: {a} {unidad} al empezar, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} chequeó {objeto_medible} cada hora: partió de {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} apuntó {a} {unidad} para {objeto_medible}. Más tarde subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} midió {objeto_medible} al llegar: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} registró el cambio de {objeto_medible}: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} anotó {objeto_medible} al comenzar el turno: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} llevó control de {objeto_medible} todo el día: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} verificó {objeto_medible} en tres momentos: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} tomó la primera lectura de {objeto_medible}: {a} {unidad}. Subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} anotó {a} {unidad} al iniciar el registro de {objeto_medible}, que luego subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} completó la ficha de {objeto_medible}: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} controló {objeto_medible} para el informe: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} anotó el valor inicial de {objeto_medible}: {a} {unidad}. Subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} siguió la variación de {objeto_medible}: {a} {unidad} al comienzo, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} tomó tres lecturas de {objeto_medible}: {a} {unidad}, luego subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} anotó {objeto_medible} en su bitácora: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} midió {objeto_medible} para el reporte diario: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} controló {objeto_medible} antes de irse: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} registró {objeto_medible} para el estudio: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} anotó cuidadosamente {objeto_medible}: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} verificó dos veces el valor de {objeto_medible}: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} completó el seguimiento de {objeto_medible}: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} tomó nota al mediodía de {objeto_medible}: partió de {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
                "En {lugar}, {personaje} anotó el registro final de {objeto_medible}: {a} {unidad}, subió {b} {unidad} y bajó {c} {unidad}.",
            ]
        else:  # dinero
            return [
                "En {lugar}, {personaje} tenía {a} {unidad} guardados. Recibió {b} {unidad} de su familia y gastó {c} {unidad} en útiles.",
                "En {lugar}, {personaje} contaba con {a} {unidad} en su alcancía. Cobró {b} {unidad} por un mandado y pagó {c} {unidad} de una deuda.",
                "En {lugar}, {personaje} llevaba {a} {unidad} en el bolsillo. Ganó {b} {unidad} vendiendo rifas y usó {c} {unidad} en la merienda.",
                "En {lugar}, {personaje} había ahorrado {a} {unidad}. Le regalaron {b} {unidad} de propina y abonó {c} {unidad} de una cuota.",
                "En {lugar}, {personaje} tenía un saldo de {a} {unidad}. Recibió {b} {unidad} por su cumpleaños y gastó {c} {unidad} en un regalo.",
                "En {lugar}, {personaje} disponía de {a} {unidad}. Cobró {b} {unidad} de la semana y pagó {c} {unidad} del transporte.",
                "En {lugar}, {personaje} guardaba {a} {unidad} en una caja. Ingresó {b} {unidad} de la venta de galletas y sacó {c} {unidad} para materiales.",
                "En {lugar}, {personaje} tenía {a} {unidad} de su mesada. Le pagaron {b} {unidad} por ayudar en casa y gastó {c} {unidad} en estampillas.",
                "En {lugar}, {personaje} contaba con {a} {unidad} de ahorro. Recibió {b} {unidad} de un premio y destinó {c} {unidad} a una donación.",
                "En {lugar}, {personaje} llevaba {a} {unidad} para el día. Cobró {b} {unidad} por lavar el auto y gastó {c} {unidad} en un juego.",
                "En {lugar}, {personaje} tenía {a} {unidad} en su cuenta. Ingresó {b} {unidad} de una venta y retiró {c} {unidad} para el bus.",
                "En {lugar}, {personaje} guardaba {a} {unidad} de aguinaldo. Recibió {b} {unidad} extra y pagó {c} {unidad} de una multa.",
                "En {lugar}, {personaje} disponía de {a} {unidad} para gastar. Ganó {b} {unidad} apostando canicas y usó {c} {unidad} en golosinas.",
                "En {lugar}, {personaje} tenía {a} {unidad} en el sobre. Le devolvieron {b} {unidad} de un préstamo y pagó {c} {unidad} de la entrada.",
                "En {lugar}, {personaje} contaba con {a} {unidad}. Cobró {b} {unidad} por cuidar mascotas y gastó {c} {unidad} en comida.",
                "En {lugar}, {personaje} llevaba {a} {unidad} de fondo. Recibió {b} {unidad} por vender manualidades y pagó {c} {unidad} de materiales.",
                "En {lugar}, {personaje} tenía {a} {unidad} reservados. Le abonaron {b} {unidad} de intereses y retiró {c} {unidad} para un libro.",
                "En {lugar}, {personaje} guardaba {a} {unidad} del mes pasado. Ingresó {b} {unidad} de su trabajo de medio tiempo y gastó {c} {unidad} en ropa.",
                "En {lugar}, {personaje} disponía de {a} {unidad} iniciales. Cobró {b} {unidad} por reciclar botellas y usó {c} {unidad} en el cine.",
                "En {lugar}, {personaje} tenía {a} {unidad} en su billetera. Recibió {b} {unidad} de vuelto y pagó {c} {unidad} de una rifa.",
                "En {lugar}, {personaje} contaba con {a} {unidad} de saldo. Ganó {b} {unidad} en un concurso y gastó {c} {unidad} en un regalo.",
                "En {lugar}, {personaje} llevaba {a} {unidad}. Le pagaron {b} {unidad} por un trabajo extra y abonó {c} {unidad} de una cuenta pendiente.",
                "En {lugar}, {personaje} tenía {a} {unidad} guardados desde el mes anterior. Recibió {b} {unidad} de un familiar y pagó {c} {unidad} de una excursión.",
                "En {lugar}, {personaje} disponía de {a} {unidad}. Cobró {b} {unidad} vendiendo limonada y gastó {c} {unidad} en vasos.",
                "En {lugar}, {personaje} tenía {a} {unidad} en su alcancía de barro. Ingresó {b} {unidad} de sus ahorros semanales y sacó {c} {unidad} para un boleto.",
                "En {lugar}, {personaje} contaba con {a} {unidad} de presupuesto. Recibió {b} {unidad} de reembolso y pagó {c} {unidad} de la merienda.",
                "En {lugar}, {personaje} llevaba {a} {unidad} para el paseo. Le dieron {b} {unidad} extra y gastó {c} {unidad} en un souvenir.",
                "En {lugar}, {personaje} tenía {a} {unidad} de la semana pasada. Cobró {b} {unidad} por su trabajo escolar y pagó {c} {unidad} de una tasa.",
                "En {lugar}, {personaje} guardaba {a} {unidad}. Recibió {b} {unidad} de un premio deportivo y usó {c} {unidad} en un uniforme.",
                "En {lugar}, {personaje} disponía de {a} {unidad} ahorrados. Ganó {b} {unidad} en una venta de garaje y pagó {c} {unidad} de flete.",
                "En {lugar}, {personaje} tenía {a} {unidad} en su cuenta de ahorros. Ingresó {b} {unidad} por intereses y retiró {c} {unidad} para gastos.",
                "En {lugar}, {personaje} llevaba {a} {unidad} de fondo común. Recibió {b} {unidad} de aportes y gastó {c} {unidad} en materiales.",
                "En {lugar}, {personaje} contaba con {a} {unidad}. Cobró {b} {unidad} por un mandado extra y pagó {c} {unidad} de una cuota atrasada.",
                "En {lugar}, {personaje} tenía {a} {unidad} guardados para el viaje. Le regalaron {b} {unidad} y gastó {c} {unidad} en el pasaje.",
                "En {lugar}, {personaje} disponía de {a} {unidad} al empezar el día. Ganó {b} {unidad} vendiendo entradas y pagó {c} {unidad} de comisión.",
                "En {lugar}, {personaje} tenía {a} {unidad} reservados para emergencias. Recibió {b} {unidad} de un bono y usó {c} {unidad} en reparaciones.",
            ]

    # Generación estructurada de 36 contextos vivenciales únicos
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
                "En el ensayo musical en {lugar}, {personaje} gastó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "Revisando la cuenta en {lugar}, {personaje} sumó {unidad} {a} por {objetos_0} junto a {unidad} {b} de {objetos_1}.",
                "En la tienda de manualidades en {lugar}, {personaje} pagó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "Durante la tarde en {lugar}, {personaje} compró {objetos_0} de {unidad} {a} y {objetos_1} de {unidad} {b}.",
                "Preparando la merienda en {lugar}, {personaje} gastó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "En la papelería de {lugar}, {personaje} seleccionó {objetos_0} por {unidad} {a} y {objetos_1} por {unidad} {b}.",
                "De paseo por {lugar}, {personaje} invirtió {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "Para el campamento scout en {lugar}, {personaje} pagó {unidad} {a} por {objetos_0} y {unidad} {b} por {objetos_1}.",
                "En la salida al cine en {lugar}, {personaje} gastó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "Ayudando en la granja de {lugar}, {personaje} abonó {unidad} {a} por {objetos_0} y {unidad} {b} por {objetos_1}.",
                "En la ferretería de {lugar}, {personaje} compró {objetos_0} por {unidad} {a} y {objetos_1} por {unidad} {b}.",
                "En el mercadillo de {lugar}, {personaje} gastó {unidad} {a} en {objetos_0} más {unidad} {b} en {objetos_1}.",
                "Para el mural escolar en {lugar}, {personaje} aportó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "En el taller de reciclaje de {lugar}, {personaje} pagó {unidad} {a} por {objetos_0} y {unidad} {b} por {objetos_1}.",
                "En el entrenamiento deportivo en {lugar}, {personaje} gastó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "Durante el picnic en {lugar}, {personaje} compró {objetos_0} por {unidad} {a} y {objetos_1} por {unidad} {b}.",
                "En el torneo de {lugar}, {personaje} abonó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "Para la conservación del jardín en {lugar}, {personaje} pagó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "En el ensayo de la banda en {lugar}, {personaje} gastó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "Para armar piezas en {lugar}, {personaje} pagó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "En la competencia en {lugar}, {personaje} invirtió {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}.",
                "Preparando los accesorios en {lugar}, {personaje} compró {objetos_0} a {unidad} {a} y {objetos_1} a {unidad} {b}.",
                "En el centro cultural de {lugar}, {personaje} pagó {unidad} {a} por {objetos_0} y {unidad} {b} por {objetos_1}.",
                "Para el taller de robótica en {lugar}, {personaje} abonó {unidad} {a} de {objetos_0} y {unidad} {b} de {objetos_1}.",
                "En la heladería de {lugar}, {personaje} gastó {unidad} {a} en {objetos_0} y {unidad} {b} en {objetos_1}."
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
                "Para la merienda en {lugar}, {personaje} reunió {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En el laboratorio de {lugar}, {personaje} midió {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En la verdulería de {lugar}, {personaje} seleccionó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En el taller de carpintería en {lugar}, {personaje} pesó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Durante el campamento en {lugar}, {personaje} llevó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Para la competencia escolar en {lugar}, {personaje} preparó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En la granja de {lugar}, {personaje} juntó {a} {unidad} de {objetos_0} con {b} {unidad} de {objetos_1}.",
                "En la panadería de {lugar}, {personaje} mezcló {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En la cocina del comedor en {lugar}, {personaje} pesó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Para la feria ambiental en {lugar}, {personaje} juntó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En el almacén de {lugar}, {personaje} empaquetó {a} {unidad} de {objetos_0} más {b} {unidad} de {objetos_1}.",
                "Cuidando el puesto en {lugar}, {personaje} acomodó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En el taller de artesanía en {lugar}, {personaje} midió {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Durante el evento comunitario en {lugar}, {personaje} cargó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En la actividad recreativa en {lugar}, {personaje} pesó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Para el proyecto botánico en {lugar}, {personaje} juntó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En la clase de nutrición en {lugar}, {personaje} combinó {a} {unidad} de {objetos_0} con {b} {unidad} de {objetos_1}.",
                "En el depósito central de {lugar}, {personaje} pesó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Durante el taller práctico en {lugar}, {personaje} agrupó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En el vivero escolar de {lugar}, {personaje} preparó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Para la preparación del festín en {lugar}, {personaje} pesó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En la fábrica de dulces de {lugar}, {personaje} mezcló {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En la feria gastronómica de {lugar}, {personaje} sirvió {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "En el centro de acopio de {lugar}, {personaje} descargó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}.",
                "Para el desafío matemático en {lugar}, {personaje} sumó {a} {unidad} de {objetos_0} y {b} {unidad} de {objetos_1}."
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
                "En el ensayo en {lugar}, {personaje} extendió {a} {unidad} de {objeto_medible} junto a {b} {unidad}.",
                "Para el mural en {lugar}, {personaje} midió {a} {unidad} y añadió {b} {unidad} de {objeto_medible}.",
                "En el taller de tecnología en {lugar}, {personaje} unió {a} {unidad} de {objeto_medible} con {b} {unidad}.",
                "Durante la caminata en {lugar}, {personaje} avanzó {a} {unidad} y después {b} {unidad}.",
                "En la pista de atletismo de {lugar}, {personaje} corrió {a} {unidad} y completó {b} {unidad} más.",
                "Para la cerca de la granja en {lugar}, {personaje} instaló {a} {unidad} de {objeto_medible} y {b} {unidad}.",
                "En la feria de maquetas de {lugar}, {personaje} pegó {a} {unidad} de {objeto_medible} a {b} {unidad}.",
                "Durante el campamento de {lugar}, {personaje} tendió {a} {unidad} de {objeto_medible} y {b} {unidad}.",
                "En el laboratorio de {lugar}, {personaje} ajustó {a} {unidad} de {objeto_medible} más {b} {unidad}.",
                "Para el escenario en {lugar}, {personaje} colocó {a} {unidad} de {objeto_medible} y {b} {unidad}.",
                "En el paseo en bicicleta por {lugar}, {personaje} pedaleó {a} {unidad} y sumó {b} {unidad}.",
                "Haciendo la maqueta en {lugar}, {personaje} unió {a} {unidad} de {objeto_medible} con {b} {unidad}.",
                "En la competencia de diseño en {lugar}, {personaje} midió {a} {unidad} y luego {b} {unidad} de {objeto_medible}.",
                "En la actividad scout de {lugar}, {personaje} anudó {a} {unidad} de {objeto_medible} con {b} {unidad}.",
                "Para la instalación eléctrica en {lugar}, {personaje} tendió {a} {unidad} de {objeto_medible} más {b} {unidad}.",
                "En la clase de educación física en {lugar}, {personaje} trotó {a} {unidad} y caminó {b} {unidad}.",
                "Durante la reforma en {lugar}, {personaje} cortó {a} {unidad} de {objeto_medible} y {b} {unidad}.",
                "En la feria de inventos de {lugar}, {personaje} acopló {a} {unidad} de {objeto_medible} a {b} {unidad}.",
                "Para el adorno de fiesta en {lugar}, {personaje} extendió {a} {unidad} de {objeto_medible} y {b} {unidad}.",
                "En el taller de modelismo de {lugar}, {personaje} unió {a} {unidad} de {objeto_medible} con {b} {unidad}.",
                "Durante la práctica deportiva en {lugar}, {personaje} recorrió {a} {unidad} y luego {b} {unidad}.",
                "En el vivero de {lugar}, {personaje} colocó {a} {unidad} de {objeto_medible} y agregó {b} {unidad}.",
                "Para el circuito de carreras en {lugar}, {personaje} midió {a} {unidad} y {b} {unidad} adicionales.",
                "En el centro de entrenamiento de {lugar}, {personaje} completó {a} {unidad} más {b} {unidad}.",
                "Para la exhibición de {lugar}, {personaje} presentó {a} {unidad} de {objeto_medible} y {b} {unidad}."
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
                "En la librería de {lugar}, {personaje} abonó una cuenta con {total} {unidad} tras comprar útiles por {unidad} {a}.",
                "Al pagar en la caja de {lugar}, {personaje} presentó {total} {unidad} y su compra costó {unidad} {a}.",
                "En la heladería de {lugar}, {personaje} disponía de {total} {unidad} y pagó {unidad} {a} por el postre.",
                "Para la entrada al parque en {lugar}, {personaje} tenía {total} {unidad} y usó {unidad} {a}.",
                "En el puesto de artesanías de {lugar}, {personaje} llevó {total} {unidad} y compró por {unidad} {a}.",
                "Durante la tarde de juegos en {lugar}, {personaje} gastó {unidad} {a} de su fondo de {total} {unidad}.",
                "En la papelería escolar de {lugar}, {personaje} entregó {total} {unidad} al adquirir {objetos_0} por {unidad} {a}.",
                "Para el viaje de estudios en {lugar}, {personaje} reservó {total} {unidad} y gastó {unidad} {a}.",
                "En la tienda deportiva de {lugar}, {personaje} llevó {total} {unidad} y compró por {unidad} {a}.",
                "En la panadería de {lugar}, {personaje} pagó una cuenta de {unidad} {a} entregando {total} {unidad}.",
                "Para el regalo familiar en {lugar}, {personaje} usó {unidad} {a} de un ahorro total de {total} {unidad}.",
                "En la zapatería de {lugar}, {personaje} disponía de {total} {unidad} y compró por {unidad} {a}.",
                "Durante la excursión a {lugar}, {personaje} llevaba {total} {unidad} y gastó {unidad} {a}.",
                "En la tienda de juguetes en {lugar}, {personaje} abonó {unidad} {a} teniendo {total} {unidad}.",
                "En la frutería de {lugar}, {personaje} entregó un billete de {total} {unidad} para pagar {unidad} {a}.",
                "Para la entrada al evento en {lugar}, {personaje} pagó {unidad} {a} de sus {total} {unidad}.",
                "En el quiosco escolar de {lugar}, {personaje} gastó {unidad} {a} de un saldo inicial de {total} {unidad}.",
                "En el taller de pintura en {lugar}, {personaje} tenía {total} {unidad} y usó {unidad} {a}.",
                "Para el taller de música en {lugar}, {personaje} invirtió {unidad} {a} de un total de {total} {unidad}.",
                "En la feria de libros de {lugar}, {personaje} compró por {unidad} {a} teniendo {total} {unidad}.",
                "En el centro comercial de {lugar}, {personaje} abonó {unidad} {a} con un billete de {total} {unidad}.",
                "Para la fiesta sorpresa en {lugar}, {personaje} gastó {unidad} {a} de sus {total} {unidad}.",
                "En la boutique de {lugar}, {personaje} usó {unidad} {a} de un saldo de {total} {unidad}.",
                "En la tienda de mascotas de {lugar}, {personaje} abonó {unidad} {a} teniendo {total} {unidad}.",
                "Para el concurso escolar en {lugar}, {personaje} usó {unidad} {a} del presupuesto de {total} {unidad}."
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
                "Para la preparación en {lugar}, {personaje} extrajo {a} {unidad} de una reserva de {total} {unidad} de {objeto_medible}.",
                "En el almacén de {lugar}, {personaje} sacó {a} {unidad} de una bolsa de {total} {unidad} de {objeto_medible}.",
                "En la panadería de {lugar}, {personaje} usó {a} {unidad} de una reserva de {total} {unidad} de {objeto_medible}.",
                "Durante la clase práctica en {lugar}, {personaje} separó {a} {unidad} de los {total} {unidad} de {objeto_medible}.",
                "En la cocina del restaurante en {lugar}, {personaje} retiró {a} {unidad} de los {total} {unidad} de {objeto_medible}.",
                "Para el taller ambiental en {lugar}, {personaje} usó {a} {unidad} de un cargamento de {total} {unidad} de {objeto_medible}.",
                "En la granja de {lugar}, {personaje} descontó {a} {unidad} de un total de {total} {unidad} de {objeto_medible}.",
                "En la fábrica de dulces en {lugar}, {personaje} empleó {a} {unidad} de un contenedor de {total} {unidad} de {objeto_medible}.",
                "Durante el experimento botánico en {lugar}, {personaje} separó {a} {unidad} de {total} {unidad} de {objeto_medible}.",
                "En el laboratorio científico de {lugar}, {personaje} apartó {a} {unidad} de {total} {unidad} de {objeto_medible}.",
                "Cuidando el establo en {lugar}, {personaje} usó {a} {unidad} de una provisión de {total} {unidad} de {objeto_medible}.",
                "En el vivero de {lugar}, {personaje} tomó {a} {unidad} de una mezcla de {total} {unidad} de {objeto_medible}.",
                "Para la competencia gastronómica en {lugar}, {personaje} usó {a} {unidad} de {total} {unidad} de {objeto_medible}.",
                "En la verdulería de {lugar}, {personaje} separó {a} {unidad} de una caja de {total} {unidad} de {objeto_medible}.",
                "En el centro de nutrición de {lugar}, {personaje} usó {a} {unidad} de una muestra de {total} {unidad} de {objeto_medible}.",
                "Para el festival de cocina en {lugar}, {personaje} tomó {a} {unidad} de {total} {unidad} de {objeto_medible}.",
                "En el taller de cerámica en {lugar}, {personaje} usó {a} {unidad} de una masa total de {total} {unidad} de {objeto_medible}.",
                "Durante la actividad en el campo en {lugar}, {personaje} descargó {a} {unidad} de {total} {unidad} de {objeto_medible}.",
                "En la panificadora de {lugar}, {personaje} separó {a} {unidad} de una harina total de {total} {unidad} de {objeto_medible}.",
                "Para el proyecto de compostaje en {lugar}, {personaje} retiró {a} {unidad} de {total} {unidad} de {objeto_medible}.",
                "En la tienda de alimentos en {lugar}, {personaje} descontó {a} {unidad} a un paquete de {total} {unidad} de {objeto_medible}.",
                "Cuidando el vivero escolar en {lugar}, {personaje} usó {a} {unidad} de los {total} {unidad} de {objeto_medible}.",
                "En el taller de experimentos de {lugar}, {personaje} tomó {a} {unidad} de {total} {unidad} de {objeto_medible}.",
                "Para la preparación del menú en {lugar}, {personaje} pesó {total} {unidad} y usó {a} {unidad} de {objeto_medible}.",
                "En la bodega de {lugar}, {personaje} separó {a} {unidad} de un lote de {total} {unidad} de {objeto_medible}."
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
                "En el ensayo en {lugar}, {personaje} desplegó {a} {unidad} de los {total} {unidad} de {objeto_medible} disponibles.",
                "En la construcción del mural en {lugar}, {personaje} recortó {a} {unidad} de una tira de {total} {unidad} de {objeto_medible}.",
                "Durante el taller de maquetas en {lugar}, {personaje} quitó {a} {unidad} a un listón de {total} {unidad} de {objeto_medible}.",
                "En el entrenamiento de atletismo en {lugar}, {personaje} corrió {a} {unidad} de una pista de {total} {unidad}.",
                "Para la decoración del escenario en {lugar}, {personaje} usó {a} {unidad} de {total} {unidad} de {objeto_medible}.",
                "En el circuito de ciclismo en {lugar}, {personaje} recorrió {a} {unidad} de un tramo de {total} {unidad}.",
                "Haciendo arreglos en {lugar}, {personaje} cortó {a} {unidad} de un cable de {total} {unidad} de {objeto_medible}.",
                "En la feria científica de {lugar}, {personaje} usó {a} {unidad} de una varilla de {total} {unidad} de {objeto_medible}.",
                "Durante el paseo en {lugar}, {personaje} caminó {a} {unidad} de un trayecto de {total} {unidad}.",
                "En el taller de costura en {lugar}, {personaje} recortó {a} {unidad} de una tela de {total} {unidad} de {objeto_medible}.",
                "Para el cerca perimetral en {lugar}, {personaje} colocó {a} {unidad} de un alambre de {total} {unidad} de {objeto_medible}.",
                "En la clase de educación física en {lugar}, {personaje} trotó {a} {unidad} de una meta de {total} {unidad}.",
                "Durante la remodelación en {lugar}, {personaje} usó {a} {unidad} de un perfil de {total} {unidad} de {objeto_medible}.",
                "En el club scout de {lugar}, {personaje} desenrolló {a} {unidad} de una cuerda de {total} {unidad} de {objeto_medible}.",
                "Para la carpa de campamento en {lugar}, {personaje} usó {a} {unidad} de una guía de {total} {unidad} de {objeto_medible}.",
                "En la pista de carreras de {lugar}, {personaje} completó {a} {unidad} de los {total} {unidad} fijados.",
                "En el taller de prototipos de {lugar}, {personaje} recortó {a} {unidad} de un tubo de {total} {unidad} de {objeto_medible}.",
                "Durante la excursión botánica en {lugar}, {personaje} recorrió {a} {unidad} de un sendero de {total} {unidad}.",
                "En la feria de inventores de {lugar}, {personaje} usó {a} {unidad} de una barra de {total} {unidad} de {objeto_medible}.",
                "Para el adorno del salón en {lugar}, {personaje} cortó {a} {unidad} de una guirnalda de {total} {unidad} de {objeto_medible}.",
                "En el taller mecánico de {lugar}, {personaje} usó {a} {unidad} de una manguera de {total} {unidad} de {objeto_medible}.",
                "Durante la prueba deportiva en {lugar}, {personaje} avanzó {a} {unidad} de una longitud total de {total} {unidad}.",
                "En el vivero de {lugar}, {personaje} recortó {a} {unidad} a un tutor de {total} {unidad} de {objeto_medible}.",
                "Para el proyecto de infraestructura en {lugar}, {personaje} colocó {a} {unidad} de {total} {unidad} de {objeto_medible}.",
                "En la competencia de obstáculos en {lugar}, {personaje} superó {a} {unidad} de un trazado de {total} {unidad}."
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
                "En el ensayo musical en {lugar}, {personaje} compró {n_cant} repuestos de {objetos_0} a {unidad} {a} cada uno.",
                "Revisando el catálogo en {lugar}, {personaje} eligió {n_cant} accesorios de {objetos_0} a {unidad} {a} cada uno.",
                "En el puesto de la feria en {lugar}, {personaje} compró {n_cant} cajas de {objetos_0} a {unidad} {a} cada una.",
                "En la cafetería escolar de {lugar}, {personaje} adquirió {n_cant} sándwiches de {objetos_0} a {unidad} {a} cada uno.",
                "Para el regalo grupal en {lugar}, {personaje} compró {n_cant} tarjetas de {objetos_0} a {unidad} {a} cada una.",
                "En la librería de {lugar}, {personaje} pagó {n_cant} cuadernos de {objetos_0} a {unidad} {a} cada uno.",
                "Durante la tarde en {lugar}, {personaje} compró {n_cant} golosinas de {objetos_0} a {unidad} {a} cada una.",
                "En el campamento en {lugar}, {personaje} encargó {n_cant} linternas de {objetos_0} a {unidad} {a} cada una.",
                "En el cine de {lugar}, {personaje} adquirió {n_cant} entradas de {objetos_0} a {unidad} {a} cada una.",
                "En la granja de {lugar}, {personaje} compró {n_cant} recipientes de {objetos_0} a {unidad} {a} cada uno.",
                "En la ferretería de {lugar}, {personaje} pagó {n_cant} herramientas de {objetos_0} a {unidad} {a} cada una.",
                "En el mercadillo de {lugar}, {personaje} eligió {n_cant} bolsas de {objetos_0} a {unidad} {a} cada una.",
                "Para el mural en {lugar}, {personaje} compró {n_cant} pinceles de {objetos_0} a {unidad} {a} cada uno.",
                "En la tienda ecológica de {lugar}, {personaje} encargó {n_cant} envases de {objetos_0} a {unidad} {a} cada uno.",
                "En la tienda de deportes de {lugar}, {personaje} compró {n_cant} pelotas de {objetos_0} a {unidad} {a} cada una.",
                "Durante el picnic en {lugar}, {personaje} adquirió {n_cant} jugos de {objetos_0} a {unidad} {a} cada uno.",
                "En la tienda de juegos en {lugar}, {personaje} pagó {n_cant} fichas de {objetos_0} a {unidad} {a} cada una.",
                "Para el cuidado del jardín en {lugar}, {personaje} compró {n_cant} macetas de {objetos_0} a {unidad} {a} cada una.",
                "En el taller de música en {lugar}, {personaje} abonó {n_cant} accesorios de {objetos_0} a {unidad} {a} cada uno.",
                "En la tienda de piezas en {lugar}, {personaje} compró {n_cant} bloques de {objetos_0} a {unidad} {a} cada uno.",
                "En la competencia en {lugar}, {personaje} adquirió {n_cant} medallas de {objetos_0} a {unidad} {a} cada una.",
                "En la boutique escolar de {lugar}, {personaje} compró {n_cant} distintivos de {objetos_0} a {unidad} {a} cada uno.",
                "En el centro cultural de {lugar}, {personaje} encargó {n_cant} boletos de {objetos_0} a {unidad} {a} cada uno.",
                "Para la feria de inventos en {lugar}, {personaje} pagó {n_cant} módulos de {objetos_0} a {unidad} {a} cada uno.",
                "En la heladería artesanal de {lugar}, {personaje} compró {n_cant} copas de {objetos_0} a {unidad} {a} cada una."
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
                "Para la preparación en {lugar}, {personaje} juntó {n_cant} bloques de {objetos_0} de {a} {unidad} cada uno.",
                "En la panadería de {lugar}, {personaje} preparó {n_cant} moldes de {objetos_0} de {a} {unidad} cada uno.",
                "En el laboratorio de {lugar}, {personaje} pesó {n_cant} muestras de {objetos_0} de {a} {unidad} cada una.",
                "En el depósito de {lugar}, {personaje} acomodó {n_cant} lotes de {objetos_0} de {a} {unidad} cada uno.",
                "Durante la cosecha en {lugar}, {personaje} juntó {n_cant} cajas de {objetos_0} de {a} {unidad} cada una.",
                "En la fábrica de alimentos en {lugar}, {personaje} embotelló {n_cant} frascos de {objetos_0} de {a} {unidad} cada uno.",
                "Para el comedor de {lugar}, {personaje} preparó {n_cant} platos de {objetos_0} de {a} {unidad} cada uno.",
                "En el vivero de {lugar}, {personaje} alistó {n_cant} bolsas de compost de {objetos_0} de {a} {unidad} cada una.",
                "En el mercado mayorista de {lugar}, {personaje} pesó {n_cant} cargas de {objetos_0} de {a} {unidad} cada una.",
                "Durante la prueba en {lugar}, {personaje} cargó {n_cant} recipientes de {objetos_0} de {a} {unidad} cada uno.",
                "En el taller artesanal de {lugar}, {personaje} usó {n_cant} bloques de {objetos_0} de {a} {unidad} cada uno.",
                "Para la exposición escolar en {lugar}, {personaje} presentó {n_cant} muestras de {objetos_0} de {a} {unidad} cada una.",
                "En el centro de acopio de {lugar}, {personaje} registró {n_cant} sacos de {objetos_0} de {a} {unidad} cada uno.",
                "Cuidando la bodega en {lugar}, {personaje} organizó {n_cant} paquetes de {objetos_0} de {a} {unidad} cada uno.",
                "En la feria gastronómica de {lugar}, {personaje} sirvió {n_cant} porciones de {objetos_0} de {a} {unidad} cada una.",
                "En la granja modelo de {lugar}, {personaje} alistó {n_cant} fardos de {objetos_0} de {a} {unidad} cada uno.",
                "Para el proyecto ecológico en {lugar}, {personaje} pesó {n_cant} contenedores de {objetos_0} de {a} {unidad} cada uno.",
                "En el almacén escolar de {lugar}, {personaje} apiló {n_cant} cajas de {objetos_0} de {a} {unidad} cada una.",
                "Durante el taller de ciencia en {lugar}, {personaje} mezcló {n_cant} frascos de {objetos_0} de {a} {unidad} cada uno.",
                "En la verdulería central de {lugar}, {personaje} pesó {n_cant} bolsas de {objetos_0} de {a} {unidad} cada una.",
                "Para el campamento scout en {lugar}, {personaje} repartió {n_cant} mochilas de {objetos_0} de {a} {unidad} cada una.",
                "En el laboratorio farmacéutico en {lugar}, {personaje} pesó {n_cant} frascos de {objetos_0} de {a} {unidad} cada uno.",
                "En la pastelería de {lugar}, {personaje} preparó {n_cant} tortas de {objetos_0} de {a} {unidad} cada una.",
                "En el puesto de venta en {lugar}, {personaje} empacó {n_cant} bolsitas de {objetos_0} de {a} {unidad} cada una.",
                "Para la maratón de {lugar}, {personaje} alistó {n_cant} kits de {objetos_0} de {a} {unidad} cada uno."
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
                "En el ensayo en {lugar}, {personaje} unió {n_cant} varillas de {objeto_medible} de {a} {unidad} cada una.",
                "Para la maqueta en {lugar}, {personaje} recortó {n_cant} varillas de {objeto_medible} de {a} {unidad} cada una.",
                "En la obra de teatro de {lugar}, {personaje} desplegó {n_cant} cintas de {objeto_medible} de {a} {unidad} cada una.",
                "Durante el taller de carpintería en {lugar}, {personaje} cortó {n_cant} tablas de {objeto_medible} de {a} {unidad} cada una.",
                "En el laboratorio de física en {lugar}, {personaje} midió {n_cant} hilos de {objeto_medible} de {a} {unidad} cada uno.",
                "Para la cerca del jardín en {lugar}, {personaje} colocó {n_cant} tramos de {objeto_medible} de {a} {unidad} cada uno.",
                "En la clase de educación física de {lugar}, {personaje} corrió {n_cant} vueltas de {a} {unidad} cada una.",
                "Durante la competencia de maquetas en {lugar}, {personaje} usó {n_cant} listones de {objeto_medible} de {a} {unidad} cada uno.",
                "En la granja educativa de {lugar}, {personaje} tendió {n_cant} hileras de {objeto_medible} de {a} {unidad} cada una.",
                "Para el mural del colegio en {lugar}, {personaje} pegó {n_cant} tiras de {objeto_medible} de {a} {unidad} cada una.",
                "En la fábrica textil de {lugar}, {personaje} midió {n_cant} cortes de {objeto_medible} de {a} {unidad} cada uno.",
                "Durante la excursión por la montaña en {lugar}, {personaje} caminó {n_cant} senderos de {a} {unidad} cada uno.",
                "En el taller de inventos en {lugar}, {personaje} acopló {n_cant} perfiles de {objeto_medible} de {a} {unidad} cada uno.",
                "Para la fiesta del pueblo en {lugar}, {personaje} extendió {n_cant} guirnaldas de {objeto_medible} de {a} {unidad} cada una.",
                "En el circuito de ciclismo en {lugar}, {personaje} pedaleó {n_cant} tramos de {a} {unidad} cada uno.",
                "Haciendo la escenografía en {lugar}, {personaje} unió {n_cant} paneles de {objeto_medible} de {a} {unidad} cada uno.",
                "En el club scout de {lugar}, {personaje} desenrolló {n_cant} cuerdas de {objeto_medible} de {a} {unidad} cada una.",
                "Para el vivero escolar en {lugar}, {personaje} colocó {n_cant} tutores de {objeto_medible} de {a} {unidad} cada uno.",
                "En la competencia de diseño en {lugar}, {personaje} recortó {n_cant} láminas de {objeto_medible} de {a} {unidad} cada una.",
                "Durante la práctica en la pista de {lugar}, {personaje} corrió {n_cant} series de {a} {unidad} cada una.",
                "En el taller mecánico de {lugar}, {personaje} midió {n_cant} tubos de {objeto_medible} de {a} {unidad} cada uno.",
                "Para la exhibición científica en {lugar}, {personaje} montó {n_cant} rieles de {objeto_medible} de {a} {unidad} cada uno.",
                "En la jornada ambiental de {lugar}, {personaje} instaló {n_cant} cercos de {objeto_medible} de {a} {unidad} cada uno.",
                "En el campamento de verano en {lugar}, {personaje} extendió {n_cant} lonas de {objeto_medible} de {a} {unidad} cada una.",
                "Para la feria tecnológica en {lugar}, {personaje} conectó {n_cant} buses de {objeto_medible} de {a} {unidad} cada uno."
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
                "En el ensayo musical en {lugar}, {personaje} invirtió {total} {unidad} en {n_cant} accesorios idénticos de {objetos_0}.",
                "Revisando los gastos en {lugar}, {personaje} dividió {total} {unidad} entre {n_cant} cuotas iguales de {objetos_0}.",
                "En el mercado de {lugar}, {personaje} pagó {total} {unidad} por {n_cant} bolsas de {objetos_0} idénticas.",
                "Durante la tarde en {lugar}, {personaje} repartió {total} {unidad} entre {n_cant} entradas de {objetos_0} iguales.",
                "Para la merienda grupal en {lugar}, {personaje} abonó {total} {unidad} por {n_cant} combos idénticos de {objetos_0}.",
                "En la librería del barrio en {lugar}, {personaje} gastó {total} {unidad} en {n_cant} libros de {objetos_0} iguales.",
                "En el parque de atracciones de {lugar}, {personaje} pagó {total} {unidad} por {n_cant} fichas idénticas de {objetos_0}.",
                "Para el regalo del maestro en {lugar}, {personaje} juntó {total} {unidad} entre {n_cant} alumnos por igual.",
                "En el cine del centro en {lugar}, {personaje} compró {n_cant} combos de {objetos_0} por un total de {total} {unidad}.",
                "En la ferretería de {lugar}, {personaje} invirtió {total} {unidad} en {n_cant} herramientas idénticas de {objetos_0}.",
                "En la granja interactiva de {lugar}, {personaje} pagó {total} {unidad} por {n_cant} paseos de {objetos_0} iguales.",
                "Para el mural artístico en {lugar}, {personaje} gastó {total} {unidad} en {n_cant} latas iguales de {objetos_0}.",
                "En el taller de costura de {lugar}, {personaje} pagó {total} {unidad} por {n_cant} carreteles iguales de {objetos_0}.",
                "Durante la feria artesanal en {lugar}, {personaje} invirtió {total} {unidad} en {n_cant} aderezos de {objetos_0} iguales.",
                "En el torneo de ajedrez en {lugar}, {personaje} repartió {total} {unidad} entre {n_cant} trofeos idénticos.",
                "Para el huerto orgánico en {lugar}, {personaje} abonó {total} {unidad} por {n_cant} sacos iguales de {objetos_0}.",
                "En la heladería de {lugar}, {personaje} gastó {total} {unidad} en {n_cant} barquillos idénticos de {objetos_0}.",
                "En la tienda de cómics en {lugar}, {personaje} pagó {total} {unidad} por {n_cant} revistas iguales de {objetos_0}.",
                "Para el festival de teatro en {lugar}, {personaje} invirtió {total} {unidad} en {n_cant} trajes iguales de {objetos_0}.",
                "En el centro de robótica de {lugar}, {personaje} pagó {total} {unidad} por {n_cant} motores idénticos de {objetos_0}.",
                "Durante el campamento de verano en {lugar}, {personaje} repartió {total} {unidad} entre {n_cant} equipos por igual.",
                "En la tienda deportiva en {lugar}, {personaje} gastó {total} {unidad} en {n_cant} camisetas idénticas de {objetos_0}.",
                "Para la campaña solidaria en {lugar}, {personaje} dividió {total} {unidad} en {n_cant} donaciones iguales de {objetos_0}.",
                "En el taller de carpintería en {lugar}, {personaje} pagó {total} {unidad} por {n_cant} guías idénticas de {objetos_0}.",
                "Para la competencia de inventos en {lugar}, {personaje} distribuyó {total} {unidad} entre {n_cant} proyectos idénticos."
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
                "Para la preparación en {lugar}, {personaje} fraccionó {total} {unidad} de {objeto_medible} entre {n_cant} recipientes iguales.",
                "En la panadería de {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} moldes idénticos.",
                "En el laboratorio bioquímico de {lugar}, {personaje} fraccionó {total} {unidad} de {objeto_medible} en {n_cant} frascos iguales.",
                "Durante la vendimia en {lugar}, {personaje} empaquetó {total} {unidad} de {objeto_medible} en {n_cant} cajas idénticas.",
                "En la fábrica de chocolates de {lugar}, {personaje} vertió {total} {unidad} de {objeto_medible} en {n_cant} barras iguales.",
                "Para el comedor escolar de {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} raciones iguales.",
                "En la granja avícola de {lugar}, {personaje} distribuyó {total} {unidad} de {objeto_medible} en {n_cant} comederos iguales.",
                "En el vivero forestal de {lugar}, {personaje} repartió {total} {unidad} de {objeto_medible} en {n_cant} maceteros idénticos.",
                "Para la feria gastronómica en {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} platillos iguales.",
                "En la verdulería central de {lugar}, {personaje} embolsó {total} {unidad} de {objeto_medible} en {n_cant} paquetes del mismo peso.",
                "Cuidando la reserva en {lugar}, {personaje} fraccionó {total} {unidad} de {objeto_medible} en {n_cant} tambores iguales.",
                "En la quesería artesanal de {lugar}, {personaje} repartió {total} {unidad} de {objeto_medible} entre {n_cant} moldes idénticos.",
                "Para el taller de cerámica en {lugar}, {personaje} cortó {total} {unidad} de {objeto_medible} en {n_cant} bloques iguales.",
                "En el almacén de semillas de {lugar}, {personaje} distribuyó {total} {unidad} de {objeto_medible} en {n_cant} frascos idénticos.",
                "Durante el festival de repostería en {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} tazones iguales.",
                "En la fábrica de jabones de {lugar}, {personaje} repartió {total} {unidad} de {objeto_medible} en {n_cant} moldes idénticos.",
                "Para el vivero comunitario de {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} sacos iguales.",
                "En el laboratorio de suelos en {lugar}, {personaje} separó {total} {unidad} de {objeto_medible} en {n_cant} muestras iguales.",
                "Durante la faena agrícola en {lugar}, {personaje} distribuyó {total} {unidad} de {objeto_medible} en {n_cant} remolques iguales.",
                "En el mercado de especias en {lugar}, {personaje} embolsó {total} {unidad} de {objeto_medible} en {n_cant} sobres idénticos.",
                "Para la expedición de alta montaña en {lugar}, {personaje} repartió {total} {unidad} de {objeto_medible} en {n_cant} cargas iguales.",
                "En la planta de procesado en {lugar}, {personaje} fraccionó {total} {unidad} de {objeto_medible} en {n_cant} envases iguales.",
                "Cuidando el puesto de salud en {lugar}, {personaje} distribuyó {total} {unidad} de {objeto_medible} en {n_cant} frasquitos iguales.",
                "Para el concurso de cocina en {lugar}, {personaje} repartió {total} {unidad} de {objeto_medible} en {n_cant} recipientes iguales.",
                "En el taller de cosmética natural de {lugar}, {personaje} fraccionó {total} {unidad} de {objeto_medible} en {n_cant} potes iguales."
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
                "En el ensayo en {lugar}, {personaje} cortó {total} {unidad} de {objeto_medible} en {n_cant} varillas del mismo tamaño.",
                "Para el mural del gimnasio en {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} franjas iguales.",
                "Durante el taller de diseño en {lugar}, {personaje} cortó {total} {unidad} de {objeto_medible} en {n_cant} segmentos iguales.",
                "En la pista de atletismo de {lugar}, {personaje} dividió la vuelta de {total} {unidad} en {n_cant} sectores del mismo tamaño.",
                "Para el decorado del teatro en {lugar}, {personaje} fraccionó {total} {unidad} de {objeto_medible} en {n_cant} tramos iguales.",
                "En el circuito de karts de {lugar}, {personaje} dividió la pista de {total} {unidad} en {n_cant} zonas del mismo largo.",
                "Haciendo arreglos eléctricos en {lugar}, {personaje} cortó {total} {unidad} de {objeto_medible} en {n_cant} cables del mismo largo.",
                "En la feria de robótica de {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} guías idénticas.",
                "Durante la caminata guiada en {lugar}, {personaje} fraccionó el trayecto de {total} {unidad} en {n_cant} paradas iguales.",
                "En el taller de modas de {lugar}, {personaje} cortó {total} {unidad} de {objeto_medible} en {n_cant} retazos idénticos.",
                "Para el cerco de la huerta en {lugar}, {personaje} repartió {total} {unidad} de {objeto_medible} en {n_cant} postes iguales.",
                "En la clase de educación física de {lugar}, {personaje} dividió una distancia de {total} {unidad} en {n_cant} relevos iguales.",
                "Durante la obra en {lugar}, {personaje} cortó {total} {unidad} de {objeto_medible} en {n_cant} vigas idénticas.",
                "En la actividad scout de {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} cuerdas del mismo tamaño.",
                "Para la carpa comunitaria en {lugar}, {personaje} recortó {total} {unidad} de {objeto_medible} en {n_cant} parantes iguales.",
                "En la pista de pruebas de {lugar}, {personaje} dividió un recorrido de {total} {unidad} en {n_cant} tramos idénticos.",
                "En el taller de prototipos de {lugar}, {personaje} cortó {total} {unidad} de {objeto_medible} en {n_cant} varillas del mismo largo.",
                "Durante el estudio botánico en {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} parcelas iguales.",
                "En la exhibición de maquetas en {lugar}, {personaje} fraccionó {total} {unidad} de {objeto_medible} en {n_cant} listones iguales.",
                "Para los adornos navideños en {lugar}, {personaje} cortó {total} {unidad} de {objeto_medible} en {n_cant} guirnaldas del mismo tamaño.",
                "En el taller náutico de {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} drizas iguales.",
                "Durante la prueba de fondo en {lugar}, {personaje} fraccionó {total} {unidad} en {n_cant} parciales exactamente iguales.",
                "En el vivero municipal de {lugar}, {personaje} cortó {total} {unidad} de {objeto_medible} en {n_cant} cañas idénticas.",
                "Para el proyecto de riego en {lugar}, {personaje} dividió {total} {unidad} de {objeto_medible} en {n_cant} mangueras iguales.",
                "En el circuito de entrenamiento de {lugar}, {personaje} fraccionó {total} {unidad} en {n_cant} estaciones idénticas."
            ]

    # Antes había un fallback silencioso que devolvía 36 frases placeholder
    # ("... analiza la situación de X (opción N)") sin ningún dato numérico:
    # ese fue el origen del bug de preguntas irresolubles en el Módulo 4 (16
    # de 18 plantillas). Si aparece una fórmula/magnitud sin cobertura, es
    # mejor que el script falle ruidosamente a que siembre contenido roto.
    raise ValueError(
        f"generate_36_frames: sin reglas para formula={formula!r} magnitud={magnitud!r} "
        f"(plantilla {pid!r}). Agregar una rama nueva en enrich_templates_36.py."
    )


# ── Módulo 4: conversión de unidades ─────────────────────────────────────────
# Los tokens numéricos de estas plantillas no representan "total menos a" ni
# "a más b" en el sentido genérico de los bloques de arriba: representan un
# salto de escala (m->cm, km->m, ...). Se agrupan por la FORMA de sus tokens,
# no por fórmula exacta, para no repetir 36 líneas por cada una de las ~14
# fórmulas de conversión distintas.
import re as _re_mod4


def _generate_36_frames_modulo4(p):
    formula = p.get("formula", "")
    tokens = [t for t in _re_mod4.findall(r"[A-Za-z_]+", formula) if t in ("a", "b", "c", "total", "n_cant")]
    tokens_unicos = []
    for t in tokens:
        if t not in tokens_unicos:
            tokens_unicos.append(t)
    tokens_con_unidad = [t for t in tokens_unicos if t != "n_cant"]

    if len(tokens_con_unidad) == 1 and "n_cant" not in tokens_unicos:
        # Un solo valor a convertir (a*100, a/1000, total/100, ...): el texto
        # usa {unidad} genérico porque el compositor ya garantiza (vía
        # _unidad_origen_requerida) que el escenario elegido tiene la unidad
        # de partida correcta para esta fórmula.
        val = tokens_con_unidad[0]
        return [f.replace("{VAL}", "{" + val + "}") for f in _frames_conversion_simple()]

    if len(tokens_con_unidad) == 1 and "n_cant" in tokens_unicos:
        # Conversión de varias piezas iguales (a*n_cant*100, a*n_cant/100):
        # mismo razonamiento de unidad, más la cantidad de piezas.
        return list(_frames_conversion_n_cant())

    # Fórmulas mixtas de dos o tres valores en unidades distintas
    # (a+b/100, a*1000+b, a-b/100, a+b/10, a*1000-b, a+b/100+c/100): la unidad
    # de cada token es fija por fórmula (no depende del escenario), así que se
    # hardcodea literalmente en el texto, igual que ya hacía el marco base
    # original de estas plantillas.
    unidades_por_formula = {
        "a+b/100": {"a": "m", "b": "cm"},
        "a-b/100": {"a": "m", "b": "cm"},
        "a*1000+b": {"a": "km", "b": "m"},
        "a*1000-b": {"a": "km", "b": "m"},
        "a+b/10": {"a": "cm", "b": "mm"},
        "a+b/100+c/100": {"a": "m", "b": "cm", "c": "cm"},
    }
    unidades = unidades_por_formula.get(formula)
    if not unidades:
        raise ValueError(f"_generate_36_frames_modulo4: sin unidades definidas para formula={formula!r}")

    es_diferencia = formula in ("a-b/100", "a*1000-b")
    if len(tokens_con_unidad) == 3:
        frames = _frames_conversion_tres_valores()
    elif es_diferencia:
        frames = _frames_conversion_diferencia()
    else:
        frames = _frames_conversion_combinada()

    out = []
    for f in frames:
        txt = f
        for tok, uni in unidades.items():
            txt = txt.replace("{" + tok + "_u}", uni)
        out.append(txt)
    return out


def _frames_conversion_simple():
    """36 marcos para conversión de un solo valor. {VAL} se reemplaza por el
    token real (a o total) al llamar. Verbos neutros que no implican ninguna
    escala física particular (nada de 'corrió N vueltas' ni similares), para
    que sirvan igual con un valor en mm que en km."""
    return [
        "En {lugar}, {personaje} midió {objeto_medible} y anotó {VAL} {unidad} en su libreta.",
        "Para el proyecto escolar en {lugar}, {personaje} registró {VAL} {unidad} como medida de {objeto_medible}.",
        "En {lugar}, {personaje} usó una cinta métrica y obtuvo {VAL} {unidad} para {objeto_medible}.",
        "Trabajando en {lugar}, {personaje} marcó {VAL} {unidad} al medir {objeto_medible}.",
        "En {lugar}, {personaje} anotó en su cuaderno {VAL} {unidad} de {objeto_medible}.",
        "Para el informe de {lugar}, {personaje} tomó nota de {VAL} {unidad} al medir {objeto_medible}.",
        "En {lugar}, {personaje} comprobó con la regla {VAL} {unidad} de {objeto_medible}.",
        "Durante la clase en {lugar}, {personaje} midió {objeto_medible} y registró {VAL} {unidad}.",
        "En {lugar}, {personaje} verificó la medida de {objeto_medible}: {VAL} {unidad}.",
        "Para el taller en {lugar}, {personaje} tomó la medida exacta de {objeto_medible}: {VAL} {unidad}.",
        "En {lugar}, {personaje} anotó {VAL} {unidad} después de medir {objeto_medible} con cuidado.",
        "Revisando {objeto_medible} en {lugar}, {personaje} obtuvo una lectura de {VAL} {unidad}.",
        "En {lugar}, {personaje} registró en la ficha técnica {VAL} {unidad} para {objeto_medible}.",
        "Para el control de calidad en {lugar}, {personaje} midió {objeto_medible} y anotó {VAL} {unidad}.",
        "En {lugar}, {personaje} comparó medidas y encontró {VAL} {unidad} en {objeto_medible}.",
        "Durante la inspección en {lugar}, {personaje} anotó {VAL} {unidad} al revisar {objeto_medible}.",
        "En {lugar}, {personaje} tomó nota de {VAL} {unidad} mientras examinaba {objeto_medible}.",
        "Para el catálogo de {lugar}, {personaje} registró {VAL} {unidad} como medida de {objeto_medible}.",
        "En {lugar}, {personaje} confirmó con el metro {VAL} {unidad} de {objeto_medible}.",
        "Antes de continuar en {lugar}, {personaje} anotó {VAL} {unidad} al medir {objeto_medible}.",
        "En {lugar}, {personaje} llevó un registro de {objeto_medible}: {VAL} {unidad}.",
        "Para el diseño en {lugar}, {personaje} midió {objeto_medible} y anotó {VAL} {unidad} en el plano.",
        "En {lugar}, {personaje} chequeó {objeto_medible} y obtuvo {VAL} {unidad} de medida.",
        "Durante la práctica en {lugar}, {personaje} registró {VAL} {unidad} al medir {objeto_medible}.",
        "En {lugar}, {personaje} anotó {VAL} {unidad} tras revisar {objeto_medible} con la cinta.",
        "Para el reporte de {lugar}, {personaje} tomó {VAL} {unidad} como medida de {objeto_medible}.",
        "En {lugar}, {personaje} verificó dos veces y confirmó {VAL} {unidad} para {objeto_medible}.",
        "Trabajando con cuidado en {lugar}, {personaje} midió {objeto_medible} y anotó {VAL} {unidad}.",
        "En {lugar}, {personaje} registró {VAL} {unidad} en la planilla de medidas de {objeto_medible}.",
        "Para completar la tarea en {lugar}, {personaje} anotó {VAL} {unidad} al medir {objeto_medible}.",
        "En {lugar}, {personaje} comprobó la medida de {objeto_medible} y anotó {VAL} {unidad}.",
        "Durante el experimento en {lugar}, {personaje} registró {VAL} {unidad} al medir {objeto_medible}.",
        "En {lugar}, {personaje} anotó cuidadosamente {VAL} {unidad} de {objeto_medible}.",
        "Para el archivo de {lugar}, {personaje} guardó el dato de {VAL} {unidad} de {objeto_medible}.",
        "En {lugar}, {personaje} tomó la lectura del instrumento: {VAL} {unidad} para {objeto_medible}.",
        "Revisando el trabajo en {lugar}, {personaje} confirmó {VAL} {unidad} como medida de {objeto_medible}.",
    ]


def _frames_conversion_n_cant():
    """36 marcos para varias piezas iguales (a*n_cant*100, a*n_cant/100)."""
    return [
        "En {lugar}, {personaje} tiene {n_cant} piezas de {objeto_medible}, cada una de {a} {unidad}.",
        "Para el proyecto en {lugar}, {personaje} cortó {n_cant} trozos de {objeto_medible} de {a} {unidad} cada uno.",
        "En {lugar}, {personaje} juntó {n_cant} tiras de {objeto_medible} de {a} {unidad} cada una.",
        "Trabajando en {lugar}, {personaje} preparó {n_cant} secciones de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} midió {n_cant} trozos de {objeto_medible}, cada uno de {a} {unidad}.",
        "Para el taller en {lugar}, {personaje} organizó {n_cant} partes de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} contó {n_cant} piezas de {objeto_medible} de {a} {unidad} cada una.",
        "Durante la clase en {lugar}, {personaje} separó {n_cant} trozos de {objeto_medible} de {a} {unidad} cada uno.",
        "En {lugar}, {personaje} alistó {n_cant} tramos de {objeto_medible} de {a} {unidad} cada uno.",
        "Para el mural en {lugar}, {personaje} recortó {n_cant} tiras de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} colocó {n_cant} piezas de {objeto_medible} de {a} {unidad} cada una en fila.",
        "Revisando el inventario en {lugar}, {personaje} contó {n_cant} unidades de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} preparó {n_cant} muestras de {objeto_medible} de {a} {unidad} cada una.",
        "Para el experimento en {lugar}, {personaje} midió {n_cant} secciones de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} apiló {n_cant} piezas de {objeto_medible} de {a} {unidad} cada una.",
        "Durante la práctica en {lugar}, {personaje} cortó {n_cant} trozos de {objeto_medible} de {a} {unidad} cada uno.",
        "En {lugar}, {personaje} ordenó {n_cant} tramos de {objeto_medible} de {a} {unidad} cada uno.",
        "Para el catálogo en {lugar}, {personaje} midió {n_cant} piezas de {objeto_medible}, cada una de {a} {unidad}.",
        "En {lugar}, {personaje} armó {n_cant} secciones de {objeto_medible} de {a} {unidad} cada una.",
        "Trabajando con cuidado en {lugar}, {personaje} cortó {n_cant} piezas de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} distribuyó {n_cant} trozos de {objeto_medible} de {a} {unidad} cada uno.",
        "Para el proyecto de diseño en {lugar}, {personaje} preparó {n_cant} tiras de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} revisó {n_cant} piezas de {objeto_medible}, todas de {a} {unidad}.",
        "Durante el inventario en {lugar}, {personaje} midió {n_cant} secciones de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} cortó {n_cant} tramos idénticos de {objeto_medible} de {a} {unidad} cada uno.",
        "Para el armado en {lugar}, {personaje} contó {n_cant} piezas de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} separó {n_cant} porciones de {objeto_medible} de {a} {unidad} cada una.",
        "Organizando el trabajo en {lugar}, {personaje} midió {n_cant} piezas de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} etiquetó {n_cant} secciones de {objeto_medible} de {a} {unidad} cada una.",
        "Para completar el pedido en {lugar}, {personaje} cortó {n_cant} tiras de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} verificó {n_cant} piezas de {objeto_medible} de {a} {unidad} cada una.",
        "Durante la producción en {lugar}, {personaje} midió {n_cant} trozos de {objeto_medible} de {a} {unidad} cada uno.",
        "En {lugar}, {personaje} clasificó {n_cant} piezas de {objeto_medible} de {a} {unidad} cada una.",
        "Para el control final en {lugar}, {personaje} contó {n_cant} secciones de {objeto_medible} de {a} {unidad} cada una.",
        "En {lugar}, {personaje} agrupó {n_cant} tramos de {objeto_medible} de {a} {unidad} cada uno.",
        "Terminando la tarea en {lugar}, {personaje} midió {n_cant} piezas de {objeto_medible} de {a} {unidad} cada una.",
    ]


def _frames_conversion_combinada():
    """36 marcos para dos/tres medidas en unidades distintas que se combinan
    en un total (a+b/100, a*1000+b, a+b/10). Las unidades se hardcodean
    literalmente vía {a_u}/{b_u} porque son fijas por fórmula, no por
    escenario (igual que ya hacía el marco base original de estas
    plantillas)."""
    return [
        "En {lugar}, {personaje} midió {objeto_medible}: {a} {a_u} y {b} {b_u} más.",
        "Para la clase de arte en {lugar}, {personaje} usó {a} {a_u} y {b} {b_u} de {objeto_medible}.",
        "En {lugar}, {personaje} unió dos partes de {objeto_medible}: una de {a} {a_u} y otra de {b} {b_u}.",
        "Trabajando en {lugar}, {personaje} juntó {a} {a_u} de {objeto_medible} con {b} {b_u} más.",
        "En {lugar}, {personaje} registró dos medidas de {objeto_medible}: {a} {a_u} y {b} {b_u}.",
        "Para el proyecto escolar en {lugar}, {personaje} sumó {a} {a_u} de {objeto_medible} a {b} {b_u} adicionales.",
        "En {lugar}, {personaje} anotó {a} {a_u} de {objeto_medible} en una parte, y {b} {b_u} en otra.",
        "Durante el taller en {lugar}, {personaje} combinó {a} {a_u} de {objeto_medible} con {b} {b_u}.",
        "En {lugar}, {personaje} tomó dos tramos de {objeto_medible}: {a} {a_u} y {b} {b_u}.",
        "Para el mural en {lugar}, {personaje} usó {a} {a_u} de {objeto_medible} y agregó {b} {b_u} más.",
        "En {lugar}, {personaje} midió {objeto_medible} en dos partes: {a} {a_u} y {b} {b_u}.",
        "Revisando {objeto_medible} en {lugar}, {personaje} anotó {a} {a_u} y luego {b} {b_u} más.",
        "En {lugar}, {personaje} registró {a} {a_u} de {objeto_medible} y sumó {b} {b_u}.",
        "Para el informe en {lugar}, {personaje} midió {a} {a_u} de {objeto_medible} y {b} {b_u} extra.",
        "En {lugar}, {personaje} tomó nota de {objeto_medible}: {a} {a_u} más {b} {b_u}.",
        "Durante la práctica en {lugar}, {personaje} sumó {a} {a_u} de {objeto_medible} a {b} {b_u}.",
        "En {lugar}, {personaje} anotó dos tramos de {objeto_medible}: {a} {a_u} y {b} {b_u}.",
        "Para el catálogo en {lugar}, {personaje} registró {a} {a_u} de {objeto_medible} y {b} {b_u} más.",
        "En {lugar}, {personaje} verificó {objeto_medible} en dos etapas: {a} {a_u} y {b} {b_u}.",
        "Trabajando con cuidado en {lugar}, {personaje} midió {a} {a_u} de {objeto_medible} y agregó {b} {b_u}.",
        "En {lugar}, {personaje} completó la medida de {objeto_medible}: {a} {a_u} y {b} {b_u} adicionales.",
        "Para el diseño en {lugar}, {personaje} anotó {a} {a_u} de {objeto_medible} más {b} {b_u}.",
        "En {lugar}, {personaje} sumó dos partes de {objeto_medible}: {a} {a_u} y {b} {b_u}.",
        "Durante el experimento en {lugar}, {personaje} registró {a} {a_u} de {objeto_medible} y {b} {b_u} más.",
        "En {lugar}, {personaje} tomó dos lecturas de {objeto_medible}: {a} {a_u} y {b} {b_u}.",
        "Para el reporte de {lugar}, {personaje} anotó {a} {a_u} de {objeto_medible} sumados a {b} {b_u}.",
        "En {lugar}, {personaje} midió {objeto_medible} completo: {a} {a_u} más {b} {b_u}.",
        "Organizando el trabajo en {lugar}, {personaje} sumó {a} {a_u} de {objeto_medible} y {b} {b_u}.",
        "En {lugar}, {personaje} registró {objeto_medible} en dos tramos: {a} {a_u} y {b} {b_u}.",
        "Para completar la tarea en {lugar}, {personaje} anotó {a} {a_u} de {objeto_medible} y {b} {b_u} más.",
        "En {lugar}, {personaje} comprobó dos medidas de {objeto_medible}: {a} {a_u} y {b} {b_u}.",
        "Durante la producción en {lugar}, {personaje} sumó {a} {a_u} de {objeto_medible} a {b} {b_u} extra.",
        "En {lugar}, {personaje} anotó el total de {objeto_medible} en dos partes: {a} {a_u} y {b} {b_u}.",
        "Para el control final en {lugar}, {personaje} registró {a} {a_u} de {objeto_medible} y {b} {b_u} más.",
        "En {lugar}, {personaje} juntó las dos medidas de {objeto_medible}: {a} {a_u} y {b} {b_u}.",
        "Terminando la tarea en {lugar}, {personaje} sumó {a} {a_u} de {objeto_medible} y {b} {b_u} adicionales.",
    ]


def _frames_conversion_diferencia():
    """36 marcos para comparar/recortar dos medidas en unidades distintas
    (a-b/100, a*1000-b)."""
    return [
        "En {lugar}, la pieza de {objeto_medible} medía {a} {a_u} y {personaje} le recortó un pedazo de {b} {b_u}.",
        "En {lugar}, el trayecto de {objeto_medible} mide {a} {a_u}, y otro tramo mide {b} {b_u}.",
        "Para la clase de arte en {lugar}, {personaje} tenía {objeto_medible} de {a} {a_u} y quitó {b} {b_u}.",
        "En {lugar}, {objeto_medible} medía {a} {a_u} al comenzar, y {personaje} le sacó {b} {b_u}.",
        "Trabajando en {lugar}, {personaje} tenía una pieza de {objeto_medible} de {a} {a_u} y cortó {b} {b_u}.",
        "En {lugar}, un tramo de {objeto_medible} mide {a} {a_u} y otro mide {b} {b_u}.",
        "En {lugar}, {personaje} midió {objeto_medible}: {a} {a_u} al inicio, y luego le recortó {b} {b_u}.",
        "Para el proyecto en {lugar}, {objeto_medible} tenía {a} {a_u} y {personaje} redujo {b} {b_u}.",
        "En {lugar}, dos secciones de {objeto_medible} miden {a} {a_u} y {b} {b_u} respectivamente.",
        "Durante el taller en {lugar}, {personaje} recortó {b} {b_u} de una pieza de {objeto_medible} de {a} {a_u}.",
        "En {lugar}, {objeto_medible} medía {a} {a_u}, y {personaje} le quitó {b} {b_u} con la tijera.",
        "Para el mural en {lugar}, {personaje} tenía {a} {a_u} de {objeto_medible} y usó {b} {b_u} menos de lo esperado.",
        "En {lugar}, un recorrido de {objeto_medible} mide {a} {a_u} y otro recorrido mide {b} {b_u}.",
        "En {lugar}, {personaje} comparó dos piezas de {objeto_medible}: una de {a} {a_u} y otra {b} {b_u} más corta.",
        "Trabajando con cuidado en {lugar}, {personaje} recortó {b} {b_u} de {objeto_medible}, que medía {a} {a_u}.",
        "En {lugar}, el primer tramo de {objeto_medible} mide {a} {a_u} y el segundo mide {b} {b_u}.",
        "Para el informe en {lugar}, {objeto_medible} medía {a} {a_u} antes del ajuste de {b} {b_u}.",
        "En {lugar}, {personaje} anotó que {objeto_medible} pasó de {a} {a_u} a tener {b} {b_u} menos.",
        "Durante la práctica en {lugar}, {personaje} redujo en {b} {b_u} una pieza de {objeto_medible} de {a} {a_u}.",
        "En {lugar}, dos trayectos distintos de {objeto_medible} miden {a} {a_u} y {b} {b_u}.",
        "Revisando {objeto_medible} en {lugar}, {personaje} notó que medía {a} {a_u} y le faltaban {b} {b_u}.",
        "En {lugar}, {personaje} cortó {b} {b_u} a una barra de {objeto_medible} de {a} {a_u}.",
        "Para el catálogo en {lugar}, {objeto_medible} medía {a} {a_u} y luego se le quitó {b} {b_u}.",
        "En {lugar}, {personaje} comparó {objeto_medible}: un tramo de {a} {a_u} contra otro de {b} {b_u}.",
        "Durante el experimento en {lugar}, {personaje} recortó {b} {b_u} de {objeto_medible}, que medía {a} {a_u}.",
        "En {lugar}, la ruta A de {objeto_medible} mide {a} {a_u} y la ruta B mide {b} {b_u}.",
        "Para el diseño en {lugar}, {personaje} tenía {a} {a_u} de {objeto_medible} y descartó {b} {b_u}.",
        "En {lugar}, {personaje} verificó dos piezas de {objeto_medible}: {a} {a_u} y {b} {b_u}.",
        "Organizando el trabajo en {lugar}, {personaje} recortó {b} {b_u} a {objeto_medible}, que medía {a} {a_u}.",
        "En {lugar}, {objeto_medible} tenía {a} {a_u} y quedó con {b} {b_u} menos tras el ajuste.",
        "Para completar la tarea en {lugar}, {personaje} comparó {a} {a_u} de {objeto_medible} con {b} {b_u} de otra pieza.",
        "En {lugar}, {personaje} anotó la diferencia entre dos tramos de {objeto_medible}: {a} {a_u} y {b} {b_u}.",
        "Durante la producción en {lugar}, {personaje} descartó {b} {b_u} de {objeto_medible}, que medía {a} {a_u}.",
        "En {lugar}, el primer trayecto de {objeto_medible} mide {a} {a_u}, y el segundo, {b} {b_u}.",
        "Para el control final en {lugar}, {personaje} comparó {objeto_medible}: {a} {a_u} contra {b} {b_u}.",
        "Terminando la tarea en {lugar}, {personaje} recortó {b} {b_u} de una pieza de {objeto_medible} de {a} {a_u}.",
    ]


def _frames_conversion_tres_valores():
    """36 marcos para tres medidas en unidades distintas que se combinan en un
    total (a+b/100+c/100)."""
    return [
        "En {lugar}, {personaje} midió {objeto_medible} en tres partes: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Para el proyecto en {lugar}, {personaje} usó {a} {a_u}, {b} {b_u} y {c} {c_u} de {objeto_medible}.",
        "En {lugar}, {personaje} unió tres tramos de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Trabajando en {lugar}, {personaje} registró tres medidas de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} sumó {a} {a_u} de {objeto_medible} a {b} {b_u} y {c} {c_u} más.",
        "Para la clase de arte en {lugar}, {personaje} cortó tres piezas de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} anotó {objeto_medible} en tres tramos: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Durante el taller en {lugar}, {personaje} combinó {a} {a_u}, {b} {b_u} y {c} {c_u} de {objeto_medible}.",
        "En {lugar}, {personaje} tomó tres secciones de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Para el mural en {lugar}, {personaje} usó {objeto_medible} en tres partes: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} midió {objeto_medible} tres veces: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Revisando {objeto_medible} en {lugar}, {personaje} anotó {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} registró {objeto_medible} completo: {a} {a_u} más {b} {b_u} más {c} {c_u}.",
        "Para el informe en {lugar}, {personaje} sumó tres tramos de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} tomó nota de {objeto_medible} en tres etapas: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Durante la práctica en {lugar}, {personaje} unió {a} {a_u}, {b} {b_u} y {c} {c_u} de {objeto_medible}.",
        "En {lugar}, {personaje} anotó tres partes de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Para el catálogo en {lugar}, {personaje} registró {objeto_medible} en tres tramos: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} verificó {objeto_medible} en tres partes: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Trabajando con cuidado en {lugar}, {personaje} sumó {a} {a_u}, {b} {b_u} y {c} {c_u} de {objeto_medible}.",
        "En {lugar}, {personaje} completó la medida de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Para el diseño en {lugar}, {personaje} anotó {objeto_medible} en tres tramos: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} sumó tres piezas de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Durante el experimento en {lugar}, {personaje} registró {a} {a_u}, {b} {b_u} y {c} {c_u} de {objeto_medible}.",
        "En {lugar}, {personaje} tomó tres lecturas de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Para el reporte de {lugar}, {personaje} anotó {objeto_medible} en tres partes: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} midió {objeto_medible} completo en tres tramos: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Organizando el trabajo en {lugar}, {personaje} sumó {a} {a_u}, {b} {b_u} y {c} {c_u} de {objeto_medible}.",
        "En {lugar}, {personaje} registró {objeto_medible} en tres secciones: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Para completar la tarea en {lugar}, {personaje} anotó tres medidas de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} comprobó {objeto_medible} en tres tramos: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Durante la producción en {lugar}, {personaje} sumó {objeto_medible} en tres partes: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} anotó el total de {objeto_medible} en tres tramos: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Para el control final en {lugar}, {personaje} registró {objeto_medible} en tres partes: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "En {lugar}, {personaje} juntó tres medidas de {objeto_medible}: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
        "Terminando la tarea en {lugar}, {personaje} sumó {objeto_medible} en tres tramos: {a} {a_u}, {b} {b_u} y {c} {c_u}.",
    ]


# ── Saneamiento (Bugs #4 y #5) ───────────────────────────────────────────────
# Bug #4: marcos que anteponen un lugar-escena propio a {lugar} ("En el huerto
# escolar de {lugar}") anidan dos lugares cuando {lugar} ya es un sitio
# completo ("el laboratorio de computación"): "en el huerto escolar del
# laboratorio de computación". Se detectaron por auditoría real (generando
# preguntas y leyendo el texto) las frases concretas que rompen así; se
# simplifican a "En {lugar}" conservando el verbo/actividad.
#
# Bug #5: en longitud de los módulos 1-3, algunos marcos usan verbos que
# implican una escala física grande o específica del deporte ("corrió N
# vueltas", "pedaleó N tramos") pero se combinan con cualquier escenario de
# esa magnitud sin filtro de escala (a diferencia del Módulo 4), produciendo
# "pedaleó 3 tramos de 2,35 mm". Se reemplazan por verbos neutros a cualquier
# escala, en línea con el resto de frases del mismo bloque.
_FIXES_LUGAR_ANIDADO = [
    ("En el huerto escolar de {lugar}", "En {lugar}"),
    ("en el huerto escolar de {lugar}", "en {lugar}"),
    ("En la clase de educación física de {lugar}", "En {lugar}"),
    ("en la clase de educación física de {lugar}", "en {lugar}"),
    ("En la clase de educación física en {lugar}", "En {lugar}"),
    ("En la granja educativa de {lugar}", "En {lugar}"),
    ("En el club de robótica de {lugar}", "En {lugar}"),
    ("En el club de robótica en {lugar}", "En {lugar}"),
    ("en el club de robótica de {lugar}", "en {lugar}"),
    ("Cuidando el vivero escolar en {lugar}", "En {lugar}"),
    ("En el vivero escolar de {lugar}", "En {lugar}"),
    ("En el taller escolar de {lugar}", "En {lugar}"),
]

_FIXES_ESCALA_VERBO = [
    (
        "En la clase de educación física de {lugar}, {personaje} corrió {n_cant} vueltas de {a} {unidad} cada una.",
        "En {lugar}, {personaje} midió {n_cant} tramos de {objeto_medible} de {a} {unidad} cada uno.",
    ),
    (
        "En el circuito de ciclismo en {lugar}, {personaje} pedaleó {n_cant} tramos de {a} {unidad} cada uno.",
        "En {lugar}, {personaje} cortó {n_cant} tramos de {objeto_medible} de {a} {unidad} cada uno.",
    ),
    (
        "Durante la práctica en la pista de {lugar}, {personaje} corrió {n_cant} series de {a} {unidad} cada una.",
        "Durante la práctica en {lugar}, {personaje} midió {n_cant} secciones de {objeto_medible} de {a} {unidad} cada una.",
    ),
    (
        "En la pista de atletismo de {lugar}, {personaje} dividió la vuelta de {total} {unidad} en {n_cant} sectores del mismo tamaño.",
        "En {lugar}, {personaje} dividió una pieza de {objeto_medible} de {total} {unidad} en {n_cant} sectores del mismo tamaño.",
    ),
    (
        "En el circuito de karts de {lugar}, {personaje} dividió la pista de {total} {unidad} en {n_cant} zonas del mismo largo.",
        "En {lugar}, {personaje} dividió una barra de {objeto_medible} de {total} {unidad} en {n_cant} zonas del mismo largo.",
    ),
    (
        "En el paseo en bicicleta por {lugar}, {personaje} pedaleó {a} {unidad} y sumó {b} {unidad}.",
        "En {lugar}, {personaje} midió {a} {unidad} de {objeto_medible} y sumó {b} {unidad} más.",
    ),
    (
        "En la clase de educación física en {lugar}, {personaje} trotó {a} {unidad} y caminó {b} {unidad}.",
        "En {lugar}, {personaje} midió {a} {unidad} de {objeto_medible} y agregó {b} {unidad} más.",
    ),
]


def _sanitize_frames(frames):
    out = []
    for f in frames:
        for old, new in _FIXES_ESCALA_VERBO:
            if f == old:
                f = new
        for old, new in _FIXES_LUGAR_ANIDADO:
            f = f.replace(old, new)
        out.append(f)
    return out


def run():
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(backend_dir, "app", "fase4", "data")
    plantillas_path = os.path.join(data_dir, "plantillas_fase4.json")

    with open(plantillas_path, "r", encoding="utf-8") as f:
        plantillas = json.load(f)

    print(f"[*] Procesando {len(plantillas)} plantillas para asignar 36 MARCOS ALTERNATIVOS a cada una...")

    for p in plantillas:
        # Asegurar corrección de fórmula e incógnita en Módulo 3 Esquema 4
        if p.get("id") in ("m3_n1_esq4_div_dividendo", "m3_n2_esq4_div_dividendo", "m3_n3_esq4_div_dividendo"):
            p["formula"] = "total/a"
            p["operacion_correcta"] = "dividir"
            p["incognita"] = "factor_multiplicativo"

        p["marcos_alternativos"] = generate_36_frames(p)

    with open(plantillas_path, "w", encoding="utf-8") as f:
        json.dump(plantillas, f, ensure_ascii=False, indent=2)

    print("Listo: las 72 plantillas ahora cuentan con 36 marcos narrativos alternativos cada una.")

if __name__ == "__main__":
    run()
