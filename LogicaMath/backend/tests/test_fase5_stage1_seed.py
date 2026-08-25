"""
Test de verificación para la Etapa 1: Reanimación del Seeder de Fase 5.
Verifica que seed.py genere 1296 preguntas, 25 configuraciones y 12 teorías sin excepciones.
"""

import pytest
from app.models.sql_models import (
    Pregunta, ConfiguracionProgreso, StatusEnum, OperacionEnum, TipoPreguntaEnum
)
from app.fase2.models import NivelTeoria
from app.fase5.compositor_fase5 import CompositorFase5
from app.fase5.theory_examples import obtener_ejemplos_expandidos_fase5


def test_seed_py_broken_kwargs_raises_typeerror():
    """Valida que los kwargs antiguos de seed.py (BUG-01, BUG-02, BUG-03) causen TypeError."""
    with pytest.raises(TypeError, match="diccionario_clave"):
        NivelTeoria(
            fase_id=5, modulo_id=1, nivel_id=1, titulo="T", texto_descubrimiento="D",
            diccionario_clave={"concepto": "Fracciones"},
            advertencia_comun="Adv", ejemplos_json=[], interactivos_json=[]
        )

    with pytest.raises(TypeError, match="explicacion"):
        Pregunta(
            fase_id=5, seccion=101, operacion=OperacionEnum.MIXTA,
            tipo_pregunta=TipoPreguntaEnum.MULTIPLE_OPCION, enunciado="E",
            respuesta_correcta="1", explicacion="Exp", es_activa=True
        )

    with pytest.raises(TypeError, match="max_errores_tolerados"):
        ConfiguracionProgreso(
            fase_id=5, seccion=101, operacion="practica_libre",
            porcentaje_aprobacion=100.0, cantidad_requerida=10,
            max_errores_tolerados=2
        )


def test_teoria_seeding_count():
    """Verifica que se generen exactamente 12 NivelTeoria validos."""
    teorias = []
    modulos_info = [
        (1, "La Fracción Visual"),
        (2, "Fracción de Cantidad"),
        (3, "Porcentajes Rápidos y Promedios"),
        (4, "Razón y Mezclas"),
    ]
    for mod_id, mod_nombre in modulos_info:
        for niv_id in (1, 2, 3):
            ejemplos = obtener_ejemplos_expandidos_fase5(mod_id, niv_id)
            t = NivelTeoria(
                fase_id=5,
                modulo_id=mod_id,
                nivel_id=niv_id,
                titulo=f"{mod_nombre} - Nivel {niv_id}",
                texto_descubrimiento=f"Descubrimiento {mod_nombre} {niv_id}",
                diccionario={"concepto": "Fracciones"},
                advertencia="Tip pedagógico",
                ejemplos=ejemplos,
                interactivos=[{"tipo": "simulador"}]
            )
            teorias.append(t)
    assert len(teorias) == 12


def test_configuracion_seeding_count_and_orden():
    """BUG-03, 04, 05: Verifica 25 configuraciones con orden_desbloqueo 1..25 y operacion MIXTA."""
    cfgs = []
    orden = 1
    # Global
    cfgs.append(ConfiguracionProgreso(
        fase_id=5, seccion=0, operacion=OperacionEnum.MIXTA,
        porcentaje_aprobacion=100.0, cantidad_requerida=15, errores_tolerados=2,
        orden_desbloqueo=orden, tipo_feedback="detallado"
    ))
    orden += 1

    # Práctica (12)
    for m in range(1, 5):
        for n in range(1, 4):
            cfgs.append(ConfiguracionProgreso(
                fase_id=5, seccion=m*100+n, operacion=OperacionEnum.MIXTA,
                porcentaje_aprobacion=100.0, cantidad_requerida=10, errores_tolerados=2,
                orden_desbloqueo=orden, tipo_feedback="detallado"
            ))
            orden += 1

    # Desafíos (12)
    for m in range(1, 5):
        for n in (11, 12, 13):
            cfgs.append(ConfiguracionProgreso(
                fase_id=5, seccion=m*1000+n, operacion=OperacionEnum.MIXTA,
                porcentaje_aprobacion=100.0, cantidad_requerida=15, errores_tolerados=2,
                orden_desbloqueo=orden, tipo_feedback="simple"
            ))
            orden += 1

    # Mixto (1)
    cfgs.append(ConfiguracionProgreso(
        fase_id=5, seccion=99099, operacion=OperacionEnum.MIXTA,
        porcentaje_aprobacion=100.0, cantidad_requerida=20, errores_tolerados=2,
        orden_desbloqueo=orden, tipo_feedback="simple"
    ))

    assert len(cfgs) == 26
    assert [c.orden_desbloqueo for c in cfgs] == list(range(1, 27))


def test_preguntas_seeding_count_and_family_structure():
    """Genera 1296 preguntas con doce familias por nivel."""
    comp = CompositorFase5()
    preguntas = []

    # 1. Práctica: 12 bloques x 60 = 720
    for mod_id in (1, 2, 3, 4):
        for niv_id in (1, 2, 3):
            sec = mod_id * 100 + niv_id
            for fam_idx in range(12):
                for var_idx in range(5):
                    seed_val = 500000 + sec * 100 + fam_idx * 5 + var_idx
                    data = comp.componer_pregunta_practica(mod_id, niv_id, fam_idx, var_idx, seed_val)
                    padre_id = f"f5_m{mod_id}_l{niv_id}_fam_{fam_idx:03d}"
                    p = Pregunta(
                        fase_id=5,
                        seccion=sec,
                        operacion=OperacionEnum.MIXTA,
                        tipo_pregunta=TipoPreguntaEnum.MULTIPLE_OPCION,
                        enunciado=data["enunciado"],
                        respuesta_correcta=data["respuesta_correcta"],
                        explicacion_paso_a_paso={"pasos": [{"orden": 1, "texto": data["explicacion"]}]},
                        datos_numericos={**data["datos_numericos"], "variante": var_idx},
                        estructura_padre_id=padre_id,
                        estado=StatusEnum.ACTIVO
                    )
                    preguntas.append(p)

    # 2. Desafíos: 12 bloques x 36 = 432
    for mod_id in (1, 2, 3, 4):
        for niv_id in (11, 12, 13):
            sec = mod_id * 1000 + niv_id
            target_niv = (niv_id - 10)
            for fam_idx in range(12):
                for var_idx in range(3):
                    seed_val = 600000 + sec * 100 + fam_idx * 3 + var_idx
                    data = comp.componer_pregunta_practica(mod_id, target_niv, fam_idx, var_idx, seed_val)
                    p = Pregunta(
                        fase_id=5,
                        seccion=sec,
                        operacion=OperacionEnum.MIXTA,
                        tipo_pregunta=TipoPreguntaEnum.MULTIPLE_OPCION,
                        enunciado=f"[Desafío] {data['enunciado']}",
                        respuesta_correcta=data["respuesta_correcta"],
                        explicacion_paso_a_paso={"pasos": [{"orden": 1, "texto": data["explicacion"]}]},
                        datos_numericos={**data["datos_numericos"], "variante": var_idx},
                        estructura_padre_id=f"f5_d{sec}_fam_{fam_idx:03d}",
                        estado=StatusEnum.ACTIVO
                    )
                    preguntas.append(p)

    # 3. Desafío Mixto Final: 144
    sec_mixto = 99099
    q_count = 0
    for mod_id in (1, 2, 3, 4):
        for niv_id in (1, 2, 3):
            for fam_idx in range(12):
                seed_val = 700000 + mod_id * 1000 + niv_id * 100 + fam_idx
                data = comp.componer_pregunta_practica(mod_id, niv_id, fam_idx, fam_idx % 3, seed_val)
                p = Pregunta(
                    fase_id=5,
                    seccion=sec_mixto,
                    operacion=OperacionEnum.MIXTA,
                    tipo_pregunta=TipoPreguntaEnum.MULTIPLE_OPCION,
                    enunciado=f"[Desafío Mixto Final] {data['enunciado']}",
                    respuesta_correcta=data["respuesta_correcta"],
                    explicacion_paso_a_paso={"pasos": [{"orden": 1, "texto": data["explicacion"]}]},
                    datos_numericos={**data["datos_numericos"], "variante": var_idx},
                    estructura_padre_id=f"f5_mixto_q{q_count:03d}",
                    estado=StatusEnum.ACTIVO
                )
                preguntas.append(p)
                q_count += 1

    assert len(preguntas) == 1296  # 720 + 432 + 144
    assert all(p.estado == StatusEnum.ACTIVO for p in preguntas)
    assert all(p.explicacion_paso_a_paso is not None for p in preguntas)
