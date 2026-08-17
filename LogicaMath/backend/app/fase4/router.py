"""
Router FastAPI — Fase 4: Operatoria Decimal y Conversiones
=============================================================================
Prefijo: /fase4
Tags:    fase4

Responsabilidades:
  - Dashboard con los 4 módulos (niveles de práctica y de desafíos).
  - Contenido de teoría dinámico desde la tabla NivelTeoria.
  - Obtener preguntas (desde BD para práctica libre y desafíos).
  - Validar respuestas:
    - Bucle Espejo (Mirror Loop) en modo Práctica Libre.
    - Salida Temprana (Early Exit) en modo Desafío con reinicio de progreso.
  - Graduación idempotente a Fase 5 tras aprobar el desafío mixto.
"""

import random
import re
from datetime import datetime
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, delete
from sqlalchemy.orm import selectinload

from ..db.session import get_db
from ..auth import get_current_user, get_current_student
from ..models.sql_models import (
    Alumno, Fase, Pregunta, ConfiguracionProgreso,
    ProgresoMaestria, Intento, PoolAsignadoAlumno,
    StatusEnum, EstadoProgresoEnum, Alternativa,
    OperacionEnum, TipoPreguntaEnum, TipoErrorEnum,
    PlatformSettings, User,
)
from ..utils.math_utils import normalize_response
from ..fase2.models import NivelTeoria, IntentoPregunta, IntentoPaso
from .compositor_fase4 import CompositorFase4
from .theory_examples import obtener_ejemplos_expandidos_fase4
from .schemas import (
    Fase4Dashboard, Fase4ModuloInfo, Fase4NivelInfo,
    Fase4PreguntaParaAlumno, Fase4Token,
    Fase4ResponderPregunta, Fase4ResultadoRespuesta,
    Fase4ContenidoLectura, Fase4DesafioInfo,
    Fase4AlternativaOut, Fase4CerrarRescate,
    Fase4ReiniciarBloque, Fase4ReinicioResultado,
)
from .topology import (
    FASE4_ID,
    MIXED_SECTION,
    PLAYABLE_SECTIONS,
    all_prerequisites_approved,
    configured_error_tolerance,
    get_block,
    has_reached_error_limit,
    is_block_unlocked,
    phase_is_complete,
)

router = APIRouter(prefix="/fase4", tags=["fase4"])

FASE_DECIMALES_ID = FASE4_ID
MAX_ESPEJO = 3  # Intentos máximos en Bucle Espejo
_COMPOSITOR_VISUAL = CompositorFase4()


def _enunciado_con_visual_actual(pregunta: Pregunta) -> str:
    """Renueva solo el SVG de M4 sin alterar la pregunta almacenada ni su respuesta."""
    datos = pregunta.datos_numericos or {}
    plantilla_id = datos.get("plantilla_id")
    valores = datos.get("valores")
    if not isinstance(valores, dict):
        valores = {
            key: datos[key]
            for key in ("a", "b", "c", "total", "n_cant")
            if key in datos
        }
    if not plantilla_id or not valores:
        return pregunta.enunciado

    plantilla = next(
        (item for item in _COMPOSITOR_VISUAL.plantillas if item.get("id") == plantilla_id),
        None,
    )
    if not plantilla or plantilla.get("modulo_id") != 4:
        return pregunta.enunciado

    figura = _COMPOSITOR_VISUAL._figura_svg(
        plantilla,
        valores,
        datos.get("unidad", ""),
    )
    if not figura:
        return pregunta.enunciado

    enunciado_base = re.sub(
        r"\s*<br\s*/?>\s*<svg\b.*?</svg>",
        "",
        pregunta.enunciado,
        count=1,
        flags=re.DOTALL | re.IGNORECASE,
    ).strip()
    figura = re.sub(r"height='\d+'", "height='200'", figura, count=1)
    return f"{enunciado_base}<br/>{figura}"

# ─────────────────────────────────────────────────────────────────────────────
# HELPER DE SINCRONIZACIÓN CON CONFIGURACIONES HEREDADAS (unlockedLevels)
# ─────────────────────────────────────────────────────────────────────────────
async def _sync_unlocked_levels(db: AsyncSession, alumno_id: int, operacion: str):
    from sqlalchemy.orm.attributes import flag_modified
    result_alumno = await db.execute(select(Alumno).where(Alumno.id == alumno_id))
    alumno = result_alumno.scalar_one_or_none()
    if alumno:
        result_user = await db.execute(select(User).where(User.id == alumno.user_id))
        user = result_user.scalar_one_or_none()
        if user:
            settings = user.settings or {}
            if "unlockedLevels" not in settings:
                settings["unlockedLevels"] = {}
            cat_map = {
                "suma": "addition",
                "resta": "subtraction",
                "multiplicacion": "multiplication",
                "division": "division",
                "mixta": "challenge"
            }
            cat = cat_map.get(operacion)
            if cat:
                settings["unlockedLevels"][cat] = 6
                user.settings = settings
                flag_modified(user, "settings")
                await db.flush()

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES DE MÓDULOS Y NIVELES
# ─────────────────────────────────────────────────────────────────────────────

MODULOS_META = {
    1: {"nombre": "Suma y Resta de Decimales", "descripcion": "Alineación de comas, enteros, décimas y centésimas.", "icono": "activity", "color": "#10B981"},
    2: {"nombre": "Multiplicación de Decimales", "descripcion": "Conteo de cifras decimales y factores.", "icono": "hash", "color": "#8B5CF6"},
    3: {"nombre": "División con Decimales", "descripcion": "Cocientes decimales y desplazamiento de comas.", "icono": "shopping-bag", "color": "#F59E0B"},
    4: {"nombre": "Conversión de Unidades", "descripcion": "Escalera métrica: km, m, cm, mm.", "icono": "tool", "color": "#EC4899"},
}

# Nombre canónico de la fase. Debe coincidir con app/seed.py FASES_DATA id=4.
FASE_NOMBRE = "Operatoria Decimal y Conversiones"

# FUENTE ÚNICA de la cantidad de niveles por módulo (docs/reestructuraciondefases.md C6.6):
# 4 módulos × 3 niveles = 12 niveles. NO duplicar este mapa en otro sitio.
NIVELES_POR_MODULO = {1: 3, 2: 3, 3: 3, 4: 3}

# Títulos alineados con app/fase4/theory_data.py (estructura aprobada C6.6).
# Si cambian ahí, deben cambiar aquí: son la misma verdad servida por dos rutas.
NIVELES_META = {
    (1, 1): {"nombre": "Suma alineando la coma", "descripcion": "Alineación vertical de comas y ceros de relleno."},
    (1, 2): {"nombre": "Resta con completado de ceros", "descripcion": "Distinto número de cifras decimales; completar con ceros."},
    (1, 3): {"nombre": "Combinadas en contexto", "descripcion": "Suma y resta encadenadas en situaciones reales."},
    (2, 1): {"nombre": "Un factor decimal (1 cifra)", "descripcion": "Factor decimal de una cifra por entero."},
    (2, 2): {"nombre": "Un factor decimal (2 cifras)", "descripcion": "Factor decimal de dos cifras por entero."},
    (2, 3): {"nombre": "Ambos factores decimales", "descripcion": "Conteo de cifras decimales de ambos factores."},
    (3, 1): {"nombre": "Dividendo decimal (1 cifra)", "descripcion": "Dividendo decimal de una cifra entre entero."},
    (3, 2): {"nombre": "Dividendo decimal (2 cifras)", "descripcion": "Dividendo decimal de dos cifras entre entero."},
    (3, 3): {"nombre": "Divisor decimal y redondeo por contexto", "descripcion": "Desplazamiento de la coma en ambos y ajuste por contexto real."},
    (4, 1): {"nombre": "Bajar la escalera métrica", "descripcion": "De unidad mayor a menor: multiplicar."},
    (4, 2): {"nombre": "Subir la escalera métrica", "descripcion": "De unidad menor a mayor: dividir."},
    (4, 3): {"nombre": "Unidades mixtas y contexto", "descripcion": "Convertir antes de operar; ambas direcciones."},
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS DE NAVEGACIÓN Y ACCESO
# ─────────────────────────────────────────────────────────────────────────────

def _seccion_operacion(modulo_id: int, nivel_id: int) -> tuple:
    """Map a validated Phase 4 block to its canonical section and operation."""
    block = get_block(modulo_id, nivel_id)
    return block.section, block.operation


async def _get_global_config(db: AsyncSession) -> dict:
    """Obtiene la configuración pedagógica global de la plataforma desde PlatformSettings."""
    result = await db.execute(
        select(PlatformSettings).where(PlatformSettings.key == "pedagogy_config")
    )
    settings = result.scalar_one_or_none()
    if not settings:
        return {
            "practica_libre": {
                "cantidad_requerida": 15,
                "porcentaje_aprobacion": 80,
                "usa_cronometro": False,
                "tiempo_default_segundos": 15,
                "tipo_feedback": "simple"
            },
            "desafios": {
                "cantidad_requerida": 20,
                "porcentaje_aprobacion": 90,
                "usa_cronometro": True,
                "tiempo_default_segundos_11": 25,
                "tiempo_default_segundos_12": 40,
                "tiempo_default_segundos_13": 50,
                "tipo_feedback": "simple"
            }
        }
    return settings.value


async def _get_config(db: AsyncSession, seccion: int, operacion: str) -> Optional[ConfiguracionProgreso]:
    # 1. Intentar obtener configuración específica y activa del bloque/nivel
    result = await db.execute(
        select(ConfiguracionProgreso).where(and_(
            ConfiguracionProgreso.fase_id == FASE_DECIMALES_ID,
            ConfiguracionProgreso.seccion == seccion,
            ConfiguracionProgreso.activo == True
        ))
    )
    config = result.scalar_one_or_none()
    if config:
        return config

    # 2. Fallback: configuración global heredada de Fase 4 (sección 0).
    result_phase = await db.execute(
        select(ConfiguracionProgreso).where(and_(
            ConfiguracionProgreso.fase_id == FASE_DECIMALES_ID,
            ConfiguracionProgreso.seccion == 0,
            ConfiguracionProgreso.operacion == "mixta",
            ConfiguracionProgreso.activo == True
        ))
    )
    return result_phase.scalar_one_or_none()


async def _get_or_create_progreso(
    db: AsyncSession, alumno_id: int, seccion: int, operacion: str
) -> ProgresoMaestria:
    result = await db.execute(
        select(ProgresoMaestria).where(and_(
            ProgresoMaestria.alumno_id == alumno_id,
            ProgresoMaestria.fase_id == FASE_DECIMALES_ID,
            ProgresoMaestria.seccion == seccion,
        )).with_for_update()
    )
    progreso = result.scalar_one_or_none()
    if not progreso:
        progreso = ProgresoMaestria(
            alumno_id=alumno_id,
            fase_id=FASE_DECIMALES_ID,
            seccion=seccion,
            operacion=operacion,
            estado=EstadoProgresoEnum.EN_PROGRESO,
            aciertos_acumulados=0,
            intentos_totales=0
        )
        db.add(progreso)
        await db.flush()
    return progreso


def _is_nivel_unlocked(progresos: dict, modulo_id: int, nivel_id: int) -> bool:
    return is_block_unlocked(progresos, modulo_id, nivel_id)


def _is_desafio_unlocked(progresos: dict, modulo_id: int, desafio_id: int, all_practice_approved: bool) -> bool:
    return all_practice_approved and is_block_unlocked(progresos, modulo_id, desafio_id)


def _is_admin_inspection(current_user: object) -> bool:
    return isinstance(current_user, dict) and current_user.get("role") == "ADMIN"


async def _load_progress_by_section(db: AsyncSession, alumno_id: int) -> dict:
    result = await db.execute(
        select(ProgresoMaestria).where(and_(
            ProgresoMaestria.alumno_id == alumno_id,
            ProgresoMaestria.fase_id == FASE_DECIMALES_ID,
        ))
    )
    return {progress.seccion: progress for progress in result.scalars().all()}


async def _authorize_block_access(
    db: AsyncSession,
    alumno: Alumno,
    modulo_id: int,
    nivel_id: int,
    current_user: object,
) -> dict:
    """Apply the same canonical unlock policy to every playable endpoint."""
    get_block(modulo_id, nivel_id)
    if _is_admin_inspection(current_user):
        return {}
    progress_by_section = await _load_progress_by_section(db, alumno.id)
    if not is_block_unlocked(progress_by_section, modulo_id, nivel_id):
        raise HTTPException(status_code=403, detail="Este bloque de Fase 4 aun esta bloqueado.")
    return progress_by_section


async def _resolve_question_for_block(
    db: AsyncSession, question_id: int, modulo_id: int, nivel_id: int
) -> Pregunta:
    """Load a Phase 4 question and bind it to its server-owned block identity."""
    block = get_block(modulo_id, nivel_id)
    result = await db.execute(
        select(Pregunta)
        .options(selectinload(Pregunta.alternativas))
        .where(and_(
            Pregunta.id == question_id,
            Pregunta.fase_id == FASE_DECIMALES_ID,
            Pregunta.estado == StatusEnum.ACTIVO,
        ))
    )
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Pregunta de Fase 4 no encontrada.")
    if question.seccion != block.section:
        raise HTTPException(
            status_code=409,
            detail="La pregunta no pertenece al bloque de Fase 4 indicado.",
        )
    return question


def _progress_value(progress: Optional[ProgresoMaestria], field: str) -> int:
    return int(getattr(progress, field, 0) or 0)


async def _lock_student_progress(db: AsyncSession, alumno_id: int) -> None:
    """Serialize progress mutations, including the first response in a block."""
    await db.execute(
        select(Alumno.id).where(Alumno.id == alumno_id).with_for_update()
    )


# ─────────────────────────────────────────────────────────────────────────────
# ENDPOINT 1 — Dashboard canónico de la Fase 4 (25 bloques)
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/dashboard", response_model=Fase4Dashboard)
async def get_fase4_dashboard(
    db: AsyncSession = Depends(get_db),
    alumno: Alumno = Depends(get_current_student),
):
    """
    Devuelve el estado completo de los 4 módulos de Fase 4 para el alumno,
    incluyendo niveles de práctica libre y desafíos.
    """

    # Cargar progresos en Fase 4
    result = await db.execute(
        select(ProgresoMaestria).where(and_(
            ProgresoMaestria.alumno_id == alumno.id,
            ProgresoMaestria.fase_id == FASE_DECIMALES_ID,
        ))
    )
    progresos = {p.seccion: p for p in result.scalars().all()}

    # Cargar configuraciones
    result = await db.execute(
        select(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE_DECIMALES_ID)
    )
    configs = {c.seccion: c for c in result.scalars().all()}

    global_cfg = await _get_global_config(db)
    pl_cfg = global_cfg.get("practica_libre", {})
    des_cfg = global_cfg.get("desafios", {})

    modulos = []
    modulo_niveles_map = NIVELES_POR_MODULO

    for mod_id in range(1, 5):
        meta = MODULOS_META[mod_id]
        niveles = []
        desafios = []
        mod_porcentaje_total = 0
        num_niveles = modulo_niveles_map[mod_id]

        # 1. Cargar niveles de práctica libre
        for niv_id in range(1, num_niveles + 1):
            seccion, operacion = _seccion_operacion(mod_id, niv_id)
            niv_meta = NIVELES_META.get((mod_id, niv_id), {"nombre": f"Nivel {niv_id}", "descripcion": ""})
            config = configs.get(seccion)
            progreso = progresos.get(seccion)

            if config is None:
                estado = "bloqueado"
                porcentaje = 0
                aciertos = 0
                requeridos = pl_cfg.get("cantidad_requerida", 15)
            elif progreso is None:
                estado = "en_progreso" if _is_nivel_unlocked(progresos, mod_id, niv_id) else "bloqueado"
                porcentaje = 0
                aciertos = 0
                requeridos = config.cantidad_requerida
            else:
                requeridos = config.cantidad_requerida
                aciertos = progreso.aciertos_acumulados
                porcentaje = min(100, progreso.porcentaje_actual)
                if progreso.estado == EstadoProgresoEnum.APROBADO:
                    estado = "dominado"
                    porcentaje = 100
                else:
                    estado = "en_progreso" if _is_nivel_unlocked(progresos, mod_id, niv_id) else "bloqueado"

            mod_porcentaje_total += porcentaje
            niveles.append(Fase4NivelInfo(
                nivel_id=niv_id,
                nombre=niv_meta["nombre"],
                descripcion=niv_meta["descripcion"],
                estado=estado,
                porcentaje=porcentaje,
                aciertos=aciertos,
                requeridos=requeridos,
                usa_cronometro=config.usa_cronometro if config else pl_cfg.get("usa_cronometro", False),
            ))

        all_practice_approved = all(n.estado == "dominado" for n in niveles)

        # 2. Cargar desafíos (11, 12, 13)
        desafio_configs = {
            11: {"nombre": "Desafío 1", "dificultad": "estandar", "tiempo_limite": 30, "max_errores": 3},
            12: {"nombre": "Desafío 2", "dificultad": "avanzada", "tiempo_limite": 45, "max_errores": 3},
            13: {"nombre": "Desafío Final", "dificultad": "maestria", "tiempo_limite": 60, "max_errores": 2},
        }

        for des_id in [11, 12, 13]:
            seccion, operacion = _seccion_operacion(mod_id, des_id)
            d_conf = desafio_configs[des_id]
            config = configs.get(seccion)
            progreso = progresos.get(seccion)

            if config is None:
                estado = "bloqueado"
                porcentaje = 0
                aciertos = 0
                requeridos = des_cfg.get("cantidad_requerida", 25 if des_id != 13 else 10)
            elif progreso is None:
                estado = "en_progreso" if _is_desafio_unlocked(progresos, mod_id, des_id, all_practice_approved) else "bloqueado"
                porcentaje = 0
                aciertos = 0
                requeridos = config.cantidad_requerida
            else:
                requeridos = config.cantidad_requerida
                aciertos = progreso.aciertos_acumulados
                porcentaje = min(100, progreso.porcentaje_actual)
                if progreso.estado == EstadoProgresoEnum.APROBADO:
                    estado = "dominado"
                    porcentaje = 100
                else:
                    estado = "en_progreso" if _is_desafio_unlocked(progresos, mod_id, des_id, all_practice_approved) else "bloqueado"
            if config:
                usa_crono = config.usa_cronometro
                tiempo_limite = config.tiempo_default_segundos if (config.tiempo_default_segundos is not None and config.tiempo_default_segundos > 0) else d_conf["tiempo_limite"]
                cantidad_req = config.cantidad_requerida
                porc_aprobacion = config.porcentaje_aprobacion
            else:
                usa_crono = des_cfg.get("usa_cronometro", True)
                tiempo_key = f"tiempo_default_segundos_{des_id}"
                tiempo_limite = des_cfg.get(tiempo_key, d_conf["tiempo_limite"])
                cantidad_req = des_cfg.get("cantidad_requerida", 25 if des_id != 13 else 10)
                porc_aprobacion = des_cfg.get("porcentaje_aprobacion", 90)

            if not usa_crono:
                tiempo_limite = 0

            max_errores_dinamico = configured_error_tolerance(
                mod_id,
                des_id,
                config.errores_tolerados if config else None,
            )

            mod_porcentaje_total += porcentaje
            desafios.append(Fase4DesafioInfo(
                desafio_id=des_id,
                nombre=d_conf["nombre"],
                dificultad=d_conf["dificultad"],
                estado=estado,
                porcentaje=porcentaje,
                aciertos=aciertos,
                requeridos=requeridos,
                tiempo_limite=tiempo_limite,
                max_errores=max_errores_dinamico,
            ))
        mod_porcentaje = mod_porcentaje_total // (num_niveles + 3)
        
        if all(n.estado == "dominado" for n in niveles) and all(d.estado == "dominado" for d in desafios):
            estado_modulo = "dominado"
        elif all(n.estado == "bloqueado" for n in niveles):
            estado_modulo = "bloqueado"
        else:
            estado_modulo = "en_progreso"

        modulos.append(Fase4ModuloInfo(
            modulo_id=mod_id,
            nombre=meta["nombre"],
            descripcion=meta["descripcion"],
            icono=meta["icono"],
            color=meta["color"],
            estado=estado_modulo,
            porcentaje_global=mod_porcentaje,
            niveles=niveles,
            desafios=desafios,
        ))

    puntos = sum(
        p.aciertos_acumulados
        for section, p in progresos.items()
        if section in PLAYABLE_SECTIONS
    )
    mixed_completed = phase_is_complete(progresos)
    desafio_mixto_disponible = all_prerequisites_approved(progresos) or mixed_completed
    if mixed_completed:
        desafio_mixto_estado = "completado"
    elif desafio_mixto_disponible:
        desafio_mixto_estado = "disponible"
    else:
        desafio_mixto_estado = "bloqueado"

    return Fase4Dashboard(
        alumno_nombre=alumno.nombre,
        puntos_totales=puntos,
        modulos=modulos,
        desafio_mixto_disponible=desafio_mixto_disponible,
        desafio_mixto_estado=desafio_mixto_estado,
    )


# ─────────────────────────────────────────────────────────────────────────────
# ENDPOINT 2 — Contenido de lectura / teoría dinámico
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/lectura/{modulo_id}/nivel/{nivel_id}", response_model=Fase4ContenidoLectura)
async def get_lectura_fase4(
    modulo_id: int,
    nivel_id: int,
    db: AsyncSession = Depends(get_db),
    alumno: Alumno = Depends(get_current_student),
    current_user: dict = Depends(get_current_user),
):
    """Devuelve el contenido de lectura/teoría de un nivel específico desde la base de datos."""
    try:
        await _authorize_block_access(
            db, alumno, modulo_id, nivel_id, current_user
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    result = await db.execute(
        select(NivelTeoria).where(and_(
            NivelTeoria.fase_id == FASE_DECIMALES_ID,
            NivelTeoria.modulo_id == modulo_id,
            NivelTeoria.nivel_id == nivel_id,
        ))
    )
    theory = result.scalar_one_or_none()
    
    if not theory:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontró contenido teórico para el módulo {modulo_id}, nivel {nivel_id}."
        )
    
    parrafos = [p.strip() for p in theory.texto_descubrimiento.split("\n") if p.strip()]
    
    return Fase4ContenidoLectura(
        modulo_id=modulo_id,
        nivel_id=nivel_id,
        modulo_nombre=MODULOS_META.get(modulo_id, {}).get("nombre", f"Módulo {modulo_id}"),
        fase_nombre=FASE_NOMBRE,
        titulo=theory.titulo,
        parrafos=parrafos,
        ejemplos=(
            obtener_ejemplos_expandidos_fase4(modulo_id, nivel_id)
            if modulo_id == 4
            else theory.ejemplos
        ),
        tip_pedagogico=theory.advertencia,
        diccionario=getattr(theory, 'diccionario', None),
        interactivos=theory.interactivos,
    )


# ─────────────────────────────────────────────────────────────────────────────
# ENDPOINT 3 — Obtener Pregunta (Práctica con Bucle Espejo y Desafíos aleatorios)
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/modulo/{modulo_id}/nivel/{nivel_id}/pregunta", response_model=Fase4PreguntaParaAlumno)
async def get_pregunta_fase4(
    modulo_id: int,
    nivel_id: int,
    reload: bool = False,
    db: AsyncSession = Depends(get_db),
    alumno: Alumno = Depends(get_current_student),
    current_user: dict = Depends(get_current_user),
):
    """
    Devuelve la siguiente pregunta para un módulo y nivel (o desafío) dados.
    Cargado dinámicamente desde el pool pre-sembrado en la base de datos.
    Soporta Bucle Espejo en práctica libre y selección aleatoria en desafíos.
    """
    try:
        progress_by_section = await _authorize_block_access(
            db, alumno, modulo_id, nivel_id, current_user
        )
        seccion, operacion = _seccion_operacion(modulo_id, nivel_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    config = await _get_config(db, seccion, operacion)
    progreso = progress_by_section.get(seccion)

    # 1. MODO DESAFÍO (modulo_id == 99 o nivel_id en 11, 12, 13)
    if modulo_id == 99 or nivel_id in (11, 12, 13):
        # Obtener preguntas del desafío que el alumno ya aprobó
        result = await db.execute(
            select(Intento.pregunta_id)
            .where(and_(
                Intento.alumno_id == alumno.id,
                Intento.fase_id == FASE_DECIMALES_ID,
                Intento.seccion == seccion,
                Intento.es_correcta == True
            ))
        )
        correct_pregunta_ids = set(result.scalars().all())

        # Si modulo_id == 99, traer preguntas de toda la fase 2 (preferiblemente de nivel 13)
        query = select(Pregunta).options(selectinload(Pregunta.alternativas)).where(and_(
            Pregunta.fase_id == FASE_DECIMALES_ID,
            Pregunta.estado == StatusEnum.ACTIVO
        ))
        
        query = query.where(Pregunta.seccion == seccion)

        result = await db.execute(query)
        preguntas = result.scalars().all()
        if not preguntas:
            raise HTTPException(status_code=404, detail="No hay preguntas en el pool para este desafío.")

        # Filtrar preguntas no aprobadas
        uncompleted = [q for q in preguntas if q.id not in correct_pregunta_ids]
        if not uncompleted:
            uncompleted = preguntas  # Si aprobó todas, permitir repetir

        pregunta_elex = random.choice(uncompleted)

        alts_out = None
        if pregunta_elex.tipo_pregunta.value == "multiple_opcion" or pregunta_elex.alternativas:
            alts_out = [
                Fase4AlternativaOut(id=alt.id, texto=alt.texto, orden=alt.orden)
                for alt in pregunta_elex.alternativas
            ]
            random.shuffle(alts_out)

        if config:
            tiene_crono = config.usa_cronometro
            if modulo_id == 99:
                tiempo_lim = config.tiempo_default_segundos if (config.tiempo_default_segundos is not None and config.tiempo_default_segundos > 0) else 90
            elif modulo_id in (3, 4):
                tiempo_lim = config.tiempo_default_segundos if (config.tiempo_default_segundos is not None and config.tiempo_default_segundos > 0) else (30 if nivel_id == 11 else (45 if nivel_id == 12 else 60))
            else:
                tiempo_lim = config.tiempo_default_segundos if (config.tiempo_default_segundos is not None and config.tiempo_default_segundos > 0) else (25 if nivel_id == 11 else (40 if nivel_id == 12 else 50))
        else:
            global_cfg = await _get_global_config(db)
            des_cfg = global_cfg.get("desafios", {})
            tiene_crono = des_cfg.get("usa_cronometro", True)
            tiempo_key = f"tiempo_default_segundos_{nivel_id}"
            if modulo_id == 99:
                tiempo_lim = des_cfg.get(tiempo_key, 90)
            elif modulo_id in (3, 4):
                tiempo_lim = des_cfg.get(tiempo_key, 30 if nivel_id == 11 else (45 if nivel_id == 12 else 60))
            else:
                tiempo_lim = des_cfg.get(tiempo_key, 25 if nivel_id == 11 else (40 if nivel_id == 12 else 50))

        if not tiene_crono:
            tiempo_lim = None

        return Fase4PreguntaParaAlumno(
            id=pregunta_elex.id,
            modulo_id=modulo_id,
            nivel_id=nivel_id,
            enunciado=_enunciado_con_visual_actual(pregunta_elex),
            tipo_pregunta=pregunta_elex.tipo_pregunta.value,
            tiene_cronometro=tiene_crono,
            tiempo_limite_segundos=tiempo_lim,
            alternativas=alts_out,
            datos_numericos=pregunta_elex.datos_numericos,
            aciertos_acumulados=_progress_value(progreso, "aciertos_acumulados"),
            intentos_totales=_progress_value(progreso, "intentos_totales"),
            porcentaje_actual=_progress_value(progreso, "porcentaje_actual"),
            cantidad_requerida=config.cantidad_requerida if config else None,
        )

    # 2. MODO PRÁCTICA LIBRE (1-10)
    else:
        # `reload` is retained as a read-only compatibility parameter.
        result = await db.execute(
            select(Intento)
            .where(and_(
                Intento.alumno_id == alumno.id,
                Intento.fase_id == FASE_DECIMALES_ID,
                Intento.seccion == seccion,
            ))
            .order_by(Intento.fecha.desc(), Intento.id.desc())
            .limit(1)
        )
        latest_attempt = result.scalar_one_or_none()

        espejo_pregunta = None
        
        # Lógica Bucle Espejo (solo si el último intento fue fallido y no fue bypass)
        if latest_attempt and not latest_attempt.es_correcta and latest_attempt.respuesta_dada != "BYPASS_EXPLICACION":
            result_q = await db.execute(
                select(Pregunta).options(selectinload(Pregunta.alternativas)).where(Pregunta.id == latest_attempt.pregunta_id)
            )
            failed_pregunta = result_q.scalar_one_or_none()
            
            if failed_pregunta and failed_pregunta.estructura_padre_id:
                # Contar cuántos intentos lleva en esta misma familia de preguntas
                res_fam = await db.execute(
                    select(Intento)
                    .join(Pregunta, Intento.pregunta_id == Pregunta.id)
                    .where(and_(
                        Intento.alumno_id == alumno.id,
                        Pregunta.estructura_padre_id == failed_pregunta.estructura_padre_id
                    ))
                    .order_by(Intento.fecha.desc(), Intento.id.desc())
                )
                family_attempts = res_fam.scalars().all()
                attempts_count = len(family_attempts)

                # Si lleva menos del máximo permitido en el bucle espejo y el último falló
                if attempts_count > 0 and not family_attempts[0].es_correcta and attempts_count < (MAX_ESPEJO + 1):
                    # Obtener las preguntas del pool para esta familia
                    result_fam_qs = await db.execute(
                        select(Pregunta).options(selectinload(Pregunta.alternativas))
                        .where(and_(
                            Pregunta.estructura_padre_id == failed_pregunta.estructura_padre_id,
                            Pregunta.estado == StatusEnum.ACTIVO
                        ))
                    )
                    family_questions = result_fam_qs.scalars().all()
                    
                    attempted_ids = {a.pregunta_id for a in family_attempts}
                    unattempted_mirrors = [
                        q for q in family_questions
                        if q.id not in attempted_ids and q.datos_numericos and q.datos_numericos.get("es_espejo") is True
                    ]

                    if unattempted_mirrors:
                        espejo_pregunta = random.choice(unattempted_mirrors)

        if espejo_pregunta:
            pregunta_elex = espejo_pregunta
        else:
            # Seleccionar una nueva familia (pregunta original: es_espejo = False)
            result_qs = await db.execute(
                select(Pregunta).options(selectinload(Pregunta.alternativas))
                .where(and_(
                    Pregunta.fase_id == FASE_DECIMALES_ID,
                    Pregunta.seccion == seccion,
                    Pregunta.estado == StatusEnum.ACTIVO
                ))
            )
            preguntas = result_qs.scalars().all()
            if not preguntas:
                raise HTTPException(status_code=404, detail="No hay preguntas en el pool para este nivel.")

            originales = [q for q in preguntas if not q.datos_numericos or q.datos_numericos.get("es_espejo") is not True]
            if not originales:
                originales = preguntas

            # Buscar familias ya tratadas (correctas o con bypass de explicación)
            res_solved = await db.execute(
                select(Pregunta.estructura_padre_id)
                .join(Intento, Intento.pregunta_id == Pregunta.id)
                .where(and_(
                    Intento.alumno_id == alumno.id,
                    Intento.fase_id == FASE_DECIMALES_ID,
                    Intento.seccion == seccion,
                    Intento.es_correcta == True  # P1: solo acierto real cuenta
                ))
            )
            solved_families = set(res_solved.scalars().all())

            unsolved_originales = [o for o in originales if o.estructura_padre_id not in solved_families]
            if not unsolved_originales:
                unsolved_originales = originales

            pregunta_elex = random.choice(unsolved_originales)

        pasos_encadenados = None
        if modulo_id == 4:
            pasos_encadenados = []
            if pregunta_elex.datos_numericos and "pasos" in pregunta_elex.datos_numericos:
                pasos_encadenados = pregunta_elex.datos_numericos["pasos"]

        alts_out = None
        if pregunta_elex.tipo_pregunta.value == "multiple_opcion" or pregunta_elex.alternativas:
            alts_out = [
                Fase4AlternativaOut(id=alt.id, texto=alt.texto, orden=alt.orden)
                for alt in pregunta_elex.alternativas
            ]
            random.shuffle(alts_out)

        if config:
            tiene_crono = config.usa_cronometro
            tiempo_lim = config.tiempo_default_segundos
            cantidad_req = config.cantidad_requerida
        else:
            global_cfg = await _get_global_config(db)
            if modulo_id == 99 or nivel_id in (11, 12, 13):
                des_cfg = global_cfg.get("desafios", {})
                tiene_crono = des_cfg.get("usa_cronometro", True)
                tiempo_key = f"tiempo_default_segundos_{nivel_id}"
                if modulo_id in (3, 4):
                    tiempo_lim = des_cfg.get(tiempo_key, 30 if nivel_id == 11 else (45 if nivel_id == 12 else (90 if modulo_id == 99 else 60)))
                else:
                    tiempo_lim = des_cfg.get(tiempo_key, 25 if nivel_id == 11 else (40 if nivel_id == 12 else 50))
                cantidad_req = des_cfg.get("cantidad_requerida", 20 if nivel_id != 13 else 10)
            else:
                pl_cfg = global_cfg.get("practica_libre", {})
                tiene_crono = pl_cfg.get("usa_cronometro", False)
                tiempo_lim = pl_cfg.get("tiempo_default_segundos", 15)
                cantidad_req = pl_cfg.get("cantidad_requerida", 15)

        if not tiene_crono:
            tiempo_lim = None

        # Calcular max_errores_tolerados y errores_sesion para desafíos (Bug 1 fix - Fuente Única de Verdad)
        _max_err = None
        _errores_sesion = 0
        if modulo_id == 99 or nivel_id in (11, 12, 13):
            _max_err = configured_error_tolerance(
                modulo_id,
                nivel_id,
                config.errores_tolerados if config else None,
            )
            res_err = await db.execute(
                select(Intento.es_correcta)
                .where(and_(
                    Intento.alumno_id == alumno.id,
                    Intento.fase_id == FASE_DECIMALES_ID,
                    Intento.seccion == seccion,
                ))
            )
            _errores_sesion = sum(1 for (es_corr,) in res_err.tuples() if not es_corr)

        return Fase4PreguntaParaAlumno(
            id=pregunta_elex.id,
            modulo_id=modulo_id,
            nivel_id=nivel_id,
            enunciado=_enunciado_con_visual_actual(pregunta_elex),
            tipo_pregunta=pregunta_elex.tipo_pregunta.value,
            tiene_cronometro=tiene_crono,
            tiempo_limite_segundos=tiempo_lim,
            pasos_encadenados=pasos_encadenados,
            alternativas=alts_out,
            datos_numericos=pregunta_elex.datos_numericos,
            aciertos_acumulados=_progress_value(progreso, "aciertos_acumulados"),
            intentos_totales=_progress_value(progreso, "intentos_totales"),
            porcentaje_actual=_progress_value(progreso, "porcentaje_actual"),
            cantidad_requerida=cantidad_req,
            max_errores_tolerados=_max_err,
            errores_sesion=_errores_sesion,
        )# ─────────────────────────────────────────────────────────────────────────────
# ENDPOINT 4 — Responder pregunta (Valida y actualiza progreso)
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/reiniciar", response_model=Fase4ReinicioResultado)
async def reiniciar_bloque_fase4(
    payload: Fase4ReiniciarBloque,
    db: AsyncSession = Depends(get_db),
    alumno: Alumno = Depends(get_current_student),
    current_user: dict = Depends(get_current_user),
):
    """Explicitly reset one unlocked block; GET endpoints never mutate state."""
    admin_inspection = _is_admin_inspection(current_user)
    try:
        seccion, operacion = _seccion_operacion(payload.modulo_id, payload.nivel_id)
        if not admin_inspection:
            await _lock_student_progress(db, alumno.id)
        progress_by_section = await _authorize_block_access(
            db, alumno, payload.modulo_id, payload.nivel_id, current_user
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if admin_inspection:
        return Fase4ReinicioResultado(
            message="Inspeccion de administrador: no se modifico progreso.",
            modulo_id=payload.modulo_id,
            nivel_id=payload.nivel_id,
            progreso_reiniciado=False,
        )

    question_ids_result = await db.execute(
        select(Pregunta.id).where(and_(
            Pregunta.fase_id == FASE_DECIMALES_ID,
            Pregunta.seccion == seccion,
        ))
    )
    question_ids = list(question_ids_result.scalars().all())
    if question_ids:
        attempt_question_ids_result = await db.execute(
            select(IntentoPregunta.id).where(and_(
                IntentoPregunta.alumno_id == alumno.id,
                IntentoPregunta.pregunta_id.in_(question_ids),
            ))
        )
        attempt_question_ids = list(attempt_question_ids_result.scalars().all())
        if attempt_question_ids:
            await db.execute(
                delete(IntentoPaso).where(
                    IntentoPaso.intento_pregunta_id.in_(attempt_question_ids)
                )
            )
        await db.execute(
            delete(IntentoPregunta).where(and_(
                IntentoPregunta.alumno_id == alumno.id,
                IntentoPregunta.pregunta_id.in_(question_ids),
            ))
        )

    await db.execute(
        delete(Intento).where(and_(
            Intento.alumno_id == alumno.id,
            Intento.fase_id == FASE_DECIMALES_ID,
            Intento.seccion == seccion,
        ))
    )

    progreso = progress_by_section.get(seccion)
    if progreso is not None:
        progreso.aciertos_acumulados = 0
        progreso.intentos_totales = 0
        progreso.porcentaje_actual = 0
        progreso.estado = EstadoProgresoEnum.EN_PROGRESO
        progreso.fecha_aprobacion = None

    await db.commit()
    return Fase4ReinicioResultado(
        message="Bloque de Fase 4 reiniciado.",
        modulo_id=payload.modulo_id,
        nivel_id=payload.nivel_id,
        progreso_reiniciado=progreso is not None,
    )


@router.post("/responder", response_model=Fase4ResultadoRespuesta)
async def responder_fase4(
    payload: Fase4ResponderPregunta,
    db: AsyncSession = Depends(get_db),
    alumno: Alumno = Depends(get_current_student),
    current_user: dict = Depends(get_current_user),
):
    """
    Valida la respuesta del alumno, calcula aciertos, e implementa:
    - Bucle Espejo (Mirror Loop) en modo Práctica Libre (1-10).
    - Lógica de Salida Temprana (Early Exit) en modo Desafío (11-13) con reinicio de progreso.
    """
    modulo_id = payload.modulo_id
    nivel_id = payload.nivel_id
    admin_inspection = _is_admin_inspection(current_user)
    try:
        seccion, operacion = _seccion_operacion(modulo_id, nivel_id)
        pregunta = await _resolve_question_for_block(
            db, payload.pregunta_id, modulo_id, nivel_id
        )
        if not admin_inspection:
            await _lock_student_progress(db, alumno.id)
        progress_by_section = await _authorize_block_access(
            db, alumno, modulo_id, nivel_id, current_user
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    config = await _get_config(db, seccion, operacion)
    progreso = progress_by_section.get(seccion)
    if not admin_inspection:
        progreso = await _get_or_create_progreso(db, alumno.id, seccion, operacion)

    es_correcta = False
    respuesta_correcta_str = pregunta.respuesta_correcta
    paso_aprobado = None
    valor_paso1_congelado = None

    # 1. VALIDAR LA RESPUESTA
    tipo_pregunta = pregunta.tipo_pregunta.value
    # La normalización decimal de Fase 4 no necesita retirar símbolos monetarios.
    is_money = False

    tipo_error = None
    feedback_mostrado = None

    if tipo_pregunta == "multiple_opcion":
        if not payload.alternativa_id:
            # Caso de timeout o no selección: tratamos como error
            es_correcta = False
            alternativa_elegida = None
            correct_alt = next((a for a in pregunta.alternativas if a.es_correcta), None)
            respuesta_correcta_str = correct_alt.texto if correct_alt else pregunta.respuesta_correcta
            tipo_error = TipoErrorEnum.CALCULO
            feedback_mostrado = "¡Se acabó el tiempo! Intenta responder más rápido la próxima vez."
        else:
            alternativa_elegida = next((a for a in pregunta.alternativas if a.id == payload.alternativa_id), None)
            if not alternativa_elegida:
                raise HTTPException(status_code=404, detail="Alternativa elegida no encontrada.")
            
            es_correcta = alternativa_elegida.es_correcta
            correct_alt = next((a for a in pregunta.alternativas if a.es_correcta), None)
            respuesta_correcta_str = correct_alt.texto if correct_alt else pregunta.respuesta_correcta
            if not es_correcta:
                tipo_error = alternativa_elegida.tipo_error
                feedback_mostrado = alternativa_elegida.feedback_error

    else:
        # Fase 4 solo genera 'multiple_opcion' y 'respuesta_numerica' (verificado
        # contra la BD real: 0 preguntas 'constructor_soluciones_chained' o
        # 'subrayado_tokens'). No se maneja esa rama aquí.
        resp_dada = normalize_response(payload.respuesta_dada, is_money)
        resp_corr = normalize_response(respuesta_correcta_str, is_money)
        es_correcta = resp_dada == resp_corr

    es_correcta_intento = es_correcta

    if admin_inspection:
        return Fase4ResultadoRespuesta(
            es_correcta=es_correcta,
            respuesta_correcta=respuesta_correcta_str,
            feedback_error=feedback_mostrado,
            aciertos_acumulados=_progress_value(progreso, "aciertos_acumulados"),
            intentos_totales=_progress_value(progreso, "intentos_totales"),
            porcentaje_actual=_progress_value(progreso, "porcentaje_actual"),
            paso_aprobado=paso_aprobado,
            valor_paso1_congelado=valor_paso1_congelado,
        )

    # 2. DETECTAR ERRORES COGNITIVOS EN PREGUNTAS ABIERTAS
    if not es_correcta and tipo_pregunta != "multiple_opcion":
        if pregunta.errores_previstos and isinstance(pregunta.errores_previstos, dict):
            normalized_dada = normalize_response(payload.respuesta_dada, is_money)
            err_list = pregunta.errores_previstos.get("respuestas_erroneas", [])
            for err in err_list:
                err_val_normalized = normalize_response(err.get("valor", ""), is_money)
                if normalized_dada == err_val_normalized:
                    tipo_error_str = err.get("tipo_error", "calculo")
                    # TipoErrorEnum.CALCULO.value == "calculo": hasattr() comprueba
                    # nombres de atributo ("CALCULO"), no valores de enum ("calculo"),
                    # así que siempre fallaba y clasificaba todo como CALCULO.
                    try:
                        tipo_error = TipoErrorEnum(tipo_error_str)
                    except ValueError:
                        tipo_error = TipoErrorEnum.CALCULO
                    feedback_mostrado = err.get("feedback")
                    break
            
            # Fallback a calculo si no coincide con ningun error cognitivo previsto
            if not tipo_error:
                tipo_error = TipoErrorEnum.CALCULO
                feedback_mostrado = pregunta.errores_previstos.get("calculo", "Revisa tus cálculos e inténtalo de nuevo.")

    es_variante_espejo = (pregunta.datos_numericos and pregunta.datos_numericos.get("es_espejo"))

    # 3. REGISTRAR EL INTENTO
    intento = Intento(
        alumno_id=alumno.id,
        pregunta_id=payload.pregunta_id,
        respuesta_dada=payload.respuesta_dada or (str(payload.alternativa_id) if payload.alternativa_id else ""),
        es_correcta=es_correcta_intento,
        fase_id=FASE_DECIMALES_ID,
        seccion=seccion,
        operacion=operacion,
        tipo_error=tipo_error,
        feedback_mostrado=feedback_mostrado,
        explicacion_mostrada=pregunta.explicacion_paso_a_paso if not es_correcta else None,
        tiempo_respuesta_segundos=payload.tiempo_respuesta_segundos,
    )
    db.add(intento)
    await db.flush()

    # 3. ACTUALIZAR PROGRESO Y LÓGICAS ESPECIALES
    
    # 3.1 MODO DESAFÍO (11, 12, 13 o Mod 99) -> Salida Temprana (Early Exit)
    if modulo_id == 99 or nivel_id in (11, 12, 13):
        if config:
            cantidad_req = config.cantidad_requerida
            porc_aprobacion = config.porcentaje_aprobacion
        else:
            if modulo_id == 99:
                cantidad_req = 20
                porc_aprobacion = 90
            else:
                cantidad_req = 10 if nivel_id == 13 else 25
                porc_aprobacion = 90

        max_errores = configured_error_tolerance(
            modulo_id,
            nivel_id,
            config.errores_tolerados if config else None,
        )

        result_att = await db.execute(
            select(Intento)
            .where(and_(
                Intento.alumno_id == alumno.id,
                Intento.fase_id == FASE_DECIMALES_ID,
                Intento.seccion == seccion,
            ))
            .order_by(Intento.fecha.desc(), Intento.id.desc())
        )
        attempts = result_att.scalars().all()
        
        errores_sesion = sum(1 for attempt in attempts if not attempt.es_correcta)
        
        if has_reached_error_limit(errores_sesion, max_errores):
            # RESET DE CONTADORES POR SALIDA TEMPRANA
            # Bug 2 fix: si el bloque ya fue APROBADO (superado alguna vez), preservar
            # ese estado para que los desafíos siguientes no se re-bloqueen.
            # Solo se resetean los contadores para el nuevo intento.
            # E8/DA7-B1: SALIDA HONROSA (reemplaza el reset destructivo). Conserva
            # el progreso, no bloquea; borra solo intentos INCORRECTOS de la
            # sección (reinicia el contador de errores, preservando los aciertos)
            # y limpia el pool para reintentar con ejercicios distintos. Mensaje
            # positivo; early_exit -> el frontend envía al repaso dirigido.
            if progreso.estado != EstadoProgresoEnum.APROBADO:
                progreso.estado = EstadoProgresoEnum.EN_PROGRESO

            await db.execute(
                delete(Intento).where(and_(
                    Intento.alumno_id == alumno.id,
                    Intento.fase_id == FASE_DECIMALES_ID,
                    Intento.seccion == seccion,
                    Intento.es_correcta == False
                ))
            )
            await db.execute(
                delete(PoolAsignadoAlumno).where(and_(
                    PoolAsignadoAlumno.alumno_id == alumno.id,
                    PoolAsignadoAlumno.seccion == seccion
                ))
            )

            await db.commit()

            return Fase4ResultadoRespuesta(
                es_correcta=es_correcta,
                respuesta_correcta=respuesta_correcta_str,
                aciertos_acumulados=progreso.aciertos_acumulados,
                intentos_totales=progreso.intentos_totales,
                porcentaje_actual=progreso.porcentaje_actual,
                bloque_completado=False,
                early_exit=True,
                errores_sesion=errores_sesion,
                max_errores_tolerados=max_errores,
                feedback_error=(
                    "¡Aún no, y está bien! Reforcemos este tema con calma y vuelve "
                    "a intentarlo: el próximo intento traerá ejercicios distintos. "
                    "Tu progreso se conserva."
                ),
            )
        else:
            progreso.intentos_totales += 1
            ya_resuelta = False
            if es_correcta:
                result_previo = await db.execute(
                    select(Intento.id).where(and_(
                        Intento.alumno_id == alumno.id,
                        Intento.pregunta_id == pregunta.id,
                        Intento.es_correcta == True,
                        Intento.id != intento.id
                    ))
                )
                if result_previo.scalar_one_or_none():
                    ya_resuelta = True

            if es_correcta and not ya_resuelta:
                progreso.aciertos_acumulados += 1

            if config:
                cantidad_req    = config.cantidad_requerida
                porc_aprobacion = config.porcentaje_aprobacion
            else:
                global_cfg = await _get_global_config(db)
                des_cfg = global_cfg.get("desafios", {})
                if modulo_id == 99:
                    cantidad_req = 20
                else:
                    cantidad_req = des_cfg.get("cantidad_requerida", 10 if nivel_id == 13 else 25)
                porc_aprobacion = des_cfg.get("porcentaje_aprobacion", 90)

            # Progreso en desafío: ratio aciertos / cantidad_req (no familias)
            progreso.porcentaje_actual = (
                min(100, int((progreso.aciertos_acumulados / cantidad_req) * 100))
                if cantidad_req > 0 else 0
            )

            bloque_completado = False
            fase_completada   = False

            if progreso.porcentaje_actual >= porc_aprobacion:
                if progreso.estado != EstadoProgresoEnum.APROBADO:
                    progreso.estado = EstadoProgresoEnum.APROBADO
                    progreso.fecha_aprobacion = datetime.utcnow()
                bloque_completado = True

                await db.flush()
                fase_completada = (
                    seccion == MIXED_SECTION
                    and progreso.estado == EstadoProgresoEnum.APROBADO
                )

            await db.commit()

            return Fase4ResultadoRespuesta(
                es_correcta=es_correcta,
                respuesta_correcta=respuesta_correcta_str,
                aciertos_acumulados=progreso.aciertos_acumulados,
                intentos_totales=progreso.intentos_totales,
                porcentaje_actual=progreso.porcentaje_actual,
                bloque_completado=bloque_completado,
                fase_completada=fase_completada,
                errores_sesion=errores_sesion,
                max_errores_tolerados=max_errores,
                feedback_error=feedback_mostrado,
            )


    else:
        # Práctica Libre (1-10): No contamos intentos ni aciertos si es una variante espejo 
        # para no penalizar el "Score" visual del alumno en modo entrenamiento.
        es_variante_espejo = (pregunta.datos_numericos and pregunta.datos_numericos.get("es_espejo"))
        
        if not es_variante_espejo:
            progreso.intentos_totales += 1
        
        ya_resuelta = False
        if es_correcta:
            result_previo = await db.execute(
                select(Intento.id).where(and_(
                    Intento.alumno_id == alumno.id,
                    Intento.pregunta_id == pregunta.id,
                    Intento.es_correcta == True,
                    Intento.id != intento.id
                )).limit(1)
            )
            if result_previo.scalar_one_or_none() is not None:
                ya_resuelta = True

        if es_correcta and not ya_resuelta:
            progreso.aciertos_acumulados += 1

        if config:
            cantidad_req = config.cantidad_requerida
            porc_aprobacion = config.porcentaje_aprobacion
        else:
            global_cfg = await _get_global_config(db)
            pl_cfg = global_cfg.get("practica_libre", {})
            cantidad_req = pl_cfg.get("cantidad_requerida", 15)
            porc_aprobacion = pl_cfg.get("porcentaje_aprobacion", 80)

        # NUEVO CÁLCULO DE PROGRESO POR COMPLETITUD (Familias únicas resueltas con éxito o bypass)
        res_fam_resueltas = await db.execute(
            select(func.count(func.distinct(Pregunta.estructura_padre_id)))
            .join(Intento, Intento.pregunta_id == Pregunta.id)
            .where(and_(
                Intento.alumno_id == alumno.id,
                Intento.fase_id == FASE_DECIMALES_ID,
                Intento.seccion == seccion,
                Intento.es_correcta == True  # P1: solo acierto real cuenta
            ))
        )
        familias_resueltas = res_fam_resueltas.scalar() or 0
        
        progreso.porcentaje_actual = min(100, int((familias_resueltas / cantidad_req) * 100)) if cantidad_req > 0 else 0

        bloque_completado = False
        fase_completada = False

        if progreso.porcentaje_actual >= 100:
            if progreso.estado != EstadoProgresoEnum.APROBADO:
                progreso.estado = EstadoProgresoEnum.APROBADO
                progreso.fecha_aprobacion = datetime.utcnow()
            bloque_completado = True
            
            await db.flush()

            # Sincronizar espejo visual heredado
            await _sync_unlocked_levels(db, alumno.id, operacion)

        espejo = False
        intentos_espejo = 0
        soporte_avanzado = False

        if not es_correcta and modulo_id in (1, 2, 3) and pregunta.estructura_padre_id:
            res_fam = await db.execute(
                select(Intento)
                .join(Pregunta, Intento.pregunta_id == Pregunta.id)
                .where(and_(
                    Intento.alumno_id == alumno.id,
                    Pregunta.estructura_padre_id == pregunta.estructura_padre_id
                ))
                .order_by(Intento.fecha.desc(), Intento.id.desc())
            )
            family_attempts = res_fam.scalars().all()
            intentos_espejo = len(family_attempts)
            
            espejo = intentos_espejo > 0
            soporte_avanzado = (config and config.tipo_feedback == "detallado") or intentos_espejo >= (MAX_ESPEJO + 1)

        await db.commit()

        return Fase4ResultadoRespuesta(
            es_correcta=es_correcta,
            respuesta_correcta=respuesta_correcta_str,
            explicacion=pregunta.explicacion_paso_a_paso if (not es_correcta and soporte_avanzado) else None,
            feedback_error=feedback_mostrado,
            aciertos_acumulados=progreso.aciertos_acumulados,
            intentos_totales=progreso.intentos_totales,
            porcentaje_actual=progreso.porcentaje_actual,
            bloque_completado=bloque_completado,
            fase_completada=fase_completada,
            es_espejo=espejo,
            intentos_espejo_actuales=intentos_espejo,
            intentos_espejo_max=MAX_ESPEJO,
            soporte_avanzado=soporte_avanzado,
            paso_aprobado=paso_aprobado,
            valor_paso1_congelado=valor_paso1_congelado,
        )


# ─────────────────────────────────────────────────────────────────────────────
# ENDPOINT 4.5 — Cerrar Rescate (Bypass sin anti-spam)
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/cerrar-rescate", response_model=Fase4ResultadoRespuesta)
async def cerrar_rescate_fase4(
    payload: Fase4CerrarRescate,
    db: AsyncSession = Depends(get_db),
    alumno: Alumno = Depends(get_current_student),
    current_user: dict = Depends(get_current_user),
):
    """
    Cierra la explicación del bloque de rescate y registra un intento virtual 'BYPASS_EXPLICACION'.
    Esto incrementa la completitud del alumno y resetea el bucle espejo de forma fluida.
    """
    modulo_id = payload.modulo_id
    nivel_id = payload.nivel_id
    admin_inspection = _is_admin_inspection(current_user)
    try:
        seccion, operacion = _seccion_operacion(modulo_id, nivel_id)
        pregunta = await _resolve_question_for_block(
            db, payload.pregunta_id, modulo_id, nivel_id
        )
        if not admin_inspection:
            await _lock_student_progress(db, alumno.id)
        progress_by_section = await _authorize_block_access(
            db, alumno, modulo_id, nivel_id, current_user
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if admin_inspection:
        return Fase4ResultadoRespuesta(
            es_correcta=False,
            respuesta_correcta=pregunta.respuesta_correcta,
            aciertos_acumulados=0,
            intentos_totales=0,
            porcentaje_actual=0,
        )

    config = await _get_config(db, seccion, operacion)
    progreso = await _get_or_create_progreso(db, alumno.id, seccion, operacion)

    # Registrar el bypass como un intento fallido especial
    intento = Intento(
        alumno_id=alumno.id,
        pregunta_id=payload.pregunta_id,
        respuesta_dada="BYPASS_EXPLICACION",
        es_correcta=False,
        fase_id=FASE_DECIMALES_ID,
        seccion=seccion,
        operacion=operacion,
        tipo_error=TipoErrorEnum.CALCULO,
        feedback_mostrado="Bypass de Explicación",
        explicacion_mostrada=None,
        tiempo_respuesta_segundos=0.0,
    )
    db.add(intento)
    await db.flush()

    progreso.intentos_totales += 1

    if config:
        cantidad_req = config.cantidad_requerida
    else:
        global_cfg = await _get_global_config(db)
        pl_cfg = global_cfg.get("practica_libre", {})
        cantidad_req = pl_cfg.get("cantidad_requerida", 15)

    # Calcular progreso por completitud (familias resueltas con éxito o bypass)
    res_fam_resueltas = await db.execute(
        select(func.count(func.distinct(Pregunta.estructura_padre_id)))
        .join(Intento, Intento.pregunta_id == Pregunta.id)
        .where(and_(
            Intento.alumno_id == alumno.id,
            Intento.fase_id == FASE_DECIMALES_ID,
            Intento.seccion == seccion,
            Intento.es_correcta == True  # P1: solo acierto real cuenta
        ))
    )
    familias_resueltas = res_fam_resueltas.scalar() or 0
    
    progreso.porcentaje_actual = min(100, int((familias_resueltas / cantidad_req) * 100)) if cantidad_req > 0 else 0

    bloque_completado = False
    fase_completada = False

    if progreso.porcentaje_actual >= 100:
        if progreso.estado != EstadoProgresoEnum.APROBADO:
            progreso.estado = EstadoProgresoEnum.APROBADO
            progreso.fecha_aprobacion = datetime.utcnow()
        bloque_completado = True
        
        await db.flush()

        # Sincronizar espejo visual heredado
        await _sync_unlocked_levels(db, alumno.id, operacion)

    await db.commit()

    return Fase4ResultadoRespuesta(
        es_correcta=False,
        respuesta_correcta=pregunta.respuesta_correcta,
        aciertos_acumulados=progreso.aciertos_acumulados,
        intentos_totales=progreso.intentos_totales,
        porcentaje_actual=progreso.porcentaje_actual,
        bloque_completado=bloque_completado,
        fase_completada=fase_completada,
        es_espejo=False,
        intentos_espejo_actuales=0,
        intentos_espejo_max=MAX_ESPEJO,
        soporte_avanzado=False,
    )



# ─────────────────────────────────────────────────────────────────────────────
# ENDPOINT 5 — Graduación a Fase 5 (requiere el desafío mixto aprobado)
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/graduate")
async def graduate_fase4(
    db: AsyncSession = Depends(get_db),
    alumno: Alumno = Depends(get_current_student),
):
    """Advance from Phase 4 to Phase 5 exactly once after mixed mastery."""
    locked_student_result = await db.execute(
        select(Alumno).where(Alumno.id == alumno.id).with_for_update()
    )
    locked_student = locked_student_result.scalar_one()

    target_result = await db.execute(select(Fase).where(Fase.orden == 5))
    target_phase = target_result.scalar_one_or_none()
    if not target_phase:
        raise HTTPException(status_code=500, detail="La Fase 5 aun no ha sido configurada.")

    if locked_student.fase_actual_id == target_phase.id:
        return {
            "message": "El alumno ya se encuentra en la Fase 5.",
            "nueva_fase_id": target_phase.id,
            "nueva_fase_nombre": target_phase.nombre,
        }

    current_result = await db.execute(
        select(Fase).where(Fase.id == locked_student.fase_actual_id)
    )
    current_phase = current_result.scalar_one_or_none()
    if not current_phase or current_phase.orden != 4:
        raise HTTPException(
            status_code=409,
            detail="La graduacion solo puede ejecutarse desde la Fase 4.",
        )

    mixed_result = await db.execute(
        select(ProgresoMaestria).where(and_(
            ProgresoMaestria.alumno_id == locked_student.id,
            ProgresoMaestria.fase_id == FASE_DECIMALES_ID,
            ProgresoMaestria.seccion == MIXED_SECTION,
            ProgresoMaestria.estado == EstadoProgresoEnum.APROBADO,
        ))
    )
    if mixed_result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=400,
            detail="Debes aprobar el desafio mixto de la Fase 4 antes de graduarte.",
        )

    locked_student.fase_actual_id = target_phase.id
    await db.commit()

    return {
        "message": "Has dominado la Fase 4 y avanzas a la Fase 5.",
        "nueva_fase_id": target_phase.id,
        "nueva_fase_nombre": target_phase.nombre,
    }



