"""
Test de verificación para la Etapa 2: Restauración del Contrato de Schemas Pydantic.
Verifica que los schemas de app/fase5/schemas.py acepten exactamente los kwargs
del router.py y del frontend (Fase5Types.ts) sin lanzamientos de ValidationError o AttributeError.
"""

import pytest
from pydantic import ValidationError

from app.fase5.schemas import (
    Fase5NivelInfo,
    Fase5DesafioInfo,
    Fase5ModuloInfo,
    Fase5Dashboard,
    Fase5PreguntaParaAlumno,
    Fase5AlternativaOut,
    Fase5ResponderPregunta,
    Fase5ResultadoRespuesta,
    Fase5ContenidoLectura,
    Fase5CerrarRescate,
)


def test_fase5_nivel_info_schema():
    """BUG-08: router.py envía estado, aciertos, porcentaje."""
    nivel = Fase5NivelInfo(
        nivel_id=1,
        nombre="Lectura de Fracciones",
        descripcion="Desc",
        estado="en_progreso",
        porcentaje=50,
        aciertos=5,
        requeridos=10,
        usa_cronometro=False,
    )
    assert nivel.estado == "en_progreso"
    assert nivel.aciertos == 5
    assert nivel.porcentaje == 50


def test_fase5_desafio_info_schema():
    """BUG-09: router.py envía desafio_id, dificultad, tiempo_limite, max_errores..."""
    desafio = Fase5DesafioInfo(
        desafio_id=11,
        nombre="Desafío Inicial",
        dificultad="estandar",
        estado="bloqueado",
        porcentaje=0,
        aciertos=0,
        requeridos=15,
        tiempo_limite=25,
        max_errores=2,
    )
    assert desafio.desafio_id == 11
    assert desafio.dificultad == "estandar"


def test_fase5_modulo_info_schema():
    """BUG-14: router.py envía color, estado, porcentaje_global."""
    modulo = Fase5ModuloInfo(
        modulo_id=1,
        nombre="La Fracción Visual",
        descripcion="Desc",
        icono="pie-chart",
        color="#3B82F6",
        estado="en_progreso",
        porcentaje_global=25,
        niveles=[],
        desafios=[],
    )
    assert modulo.color == "#3B82F6"
    assert modulo.estado == "en_progreso"
    assert modulo.porcentaje_global == 25


def test_fase5_dashboard_schema():
    """BUG-10: router.py envía alumno_nombre, puntos_totales, desafio_mixto_*."""
    dashboard = Fase5Dashboard(
        alumno_nombre="Juanito",
        puntos_totales=150,
        desafio_mixto_disponible=True,
        desafio_mixto_estado="disponible",
        modulos=[],
    )
    assert dashboard.alumno_nombre == "Juanito"
    assert dashboard.puntos_totales == 150
    assert dashboard.desafio_mixto_disponible is True


def test_fase5_pregunta_para_alumno_schema():
    """BUG-13: router.py envía aciertos_acumulados, intentos_totales, porcentaje_actual, cantidad_requerida."""
    preg = Fase5PreguntaParaAlumno(
        id=1,
        modulo_id=1,
        nivel_id=1,
        enunciado="¿Qué fracción representa?",
        tipo_pregunta="multiple_opcion",
        respuesta_correcta=None,
        tiene_cronometro=False,
        tiempo_limite_segundos=0,
        alternativas=[Fase5AlternativaOut(id=10, texto="1/2")],
        datos_numericos={"tipo_visual": "pizza", "cortes": 4, "sombreados": [1, 2]},
        aciertos_acumulados=3,
        intentos_totales=4,
        porcentaje_actual=30,
        cantidad_requerida=10,
    )
    assert preg.aciertos_acumulados == 3
    assert preg.cantidad_requerida == 10


def test_fase5_responder_pregunta_schema():
    """BUG-07: frontend envía respuesta_dada u alternativa_id, no exige respuesta_alumno."""
    payload1 = Fase5ResponderPregunta(
        modulo_id=1,
        nivel_id=1,
        pregunta_id=42,
        respuesta_dada="1/2",
        tiempo_respuesta_segundos=3.5,
    )
    assert payload1.respuesta_dada == "1/2"

    payload2 = Fase5ResponderPregunta(
        modulo_id=1,
        nivel_id=1,
        pregunta_id=42,
        alternativa_id=101,
        tiempo_respuesta_segundos=2.1,
    )
    assert payload2.alternativa_id == 101


def test_fase5_resultado_respuesta_schema():
    """BUG-12: router.py envía early_exit, explicacion_profunda, errores_sesion, max_errores_tolerados."""
    resultado = Fase5ResultadoRespuesta(
        es_correcta=True,
        respuesta_correcta="1/2",
        feedback_tutor="¡Bien hecho!",
        feedback_error=None,
        explicacion={"pasos": [{"orden": 1, "texto": "Explicación"}]},
        aciertos_acumulados=5,
        intentos_totales=6,
        porcentaje_actual=50,
        bloque_completado=False,
        fase_completada=False,
        es_espejo=False,
        intentos_espejo_actuales=0,
        intentos_espejo_max=3,
        soporte_avanzado=False,
        early_exit=False,
        errores_sesion=0,
        max_errores_tolerados=2,
        explicacion_profunda="Explicación detallada de rescate",
    )
    assert resultado.early_exit is False
    assert resultado.explicacion_profunda == "Explicación detallada de rescate"


def test_fase5_contenido_lectura_schema():
    """BUG-11: router.py envía parrafos, tip_pedagogico, diccionario, interactivos en lugar de contenido_html."""
    lectura = Fase5ContenidoLectura(
        modulo_id=1,
        nivel_id=1,
        titulo="La Fracción Visual - Nivel 1",
        parrafos=["Una fracción representa partes de un todo."],
        ejemplos=[{"enunciado": "Una pizza en 4 partes", "respuesta": "1/4"}],
        tip_pedagogico="Simplifica siempre que sea posible",
        diccionario={"Numerador": "Partes tomadas", "Denominador": "Partes totales"},
        interactivos=[{"tipo": "simulador"}],
    )
    assert lectura.parrafos == ["Una fracción representa partes de un todo."]
    assert lectura.diccionario["Numerador"] == "Partes tomadas"


def test_fase5_cerrar_rescate_schema():
    rescate = Fase5CerrarRescate(
        modulo_id=1,
        nivel_id=1,
        pregunta_id=42,
        success=True,
    )
    assert rescate.success is True
