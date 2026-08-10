"""
Schemas Pydantic — Fase 5: Fracciones, Porcentajes y Proporciones
=================================================================
Espeja exactamente los schemas de Fase 2 y los tipos del frontend (Fase5Types.ts).
"""

from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, List, Dict, Any

from .topology import get_block


def _validate_block_pair(module_id: int, level_id: int) -> None:
    try:
        get_block(module_id, level_id)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc


class Fase5AlternativaOut(BaseModel):
    """Opción de respuesta para preguntas de opción múltiple."""
    id: int
    texto: str
    orden: Optional[int] = None


class Fase5PreguntaParaAlumno(BaseModel):
    """Estructura recibida por el frontend para mostrar una pregunta de la Fase 5."""
    id: Optional[int] = None
    modulo_id: int
    nivel_id: int
    enunciado: str
    enunciado_seed: Optional[str] = None
    tipo_pregunta: str
    respuesta_correcta: Optional[str] = None
    tiene_cronometro: bool = False
    tiempo_limite_segundos: Optional[int] = None

    alternativas: Optional[List[Fase5AlternativaOut]] = None
    pasos_encadenados: Optional[List[Dict[str, Any]]] = None
    datos_numericos: Optional[Dict[str, Any]] = None
    explicacion_referencia: Optional[Dict[str, Any]] = None

    # Estado de progreso actual
    aciertos_acumulados: int = 0
    intentos_totales: int = 0
    porcentaje_actual: int = 0
    cantidad_requerida: Optional[int] = None


class Fase5DesafioInfo(BaseModel):
    desafio_id: int
    nombre: str
    dificultad: str = "estandar"
    estado: str = "bloqueado"  # bloqueado | en_progreso | dominado
    porcentaje: int = 0
    aciertos: int = 0
    requeridos: int = 0
    tiempo_limite: int = 0
    max_errores: int = 0

    model_config = ConfigDict(extra="forbid")


class Fase5NivelInfo(BaseModel):
    nivel_id: int
    nombre: str
    descripcion: str
    estado: str = "bloqueado"  # bloqueado | en_progreso | dominado
    porcentaje: int = 0
    aciertos: int = 0
    requeridos: int = 0
    usa_cronometro: bool = False

    model_config = ConfigDict(extra="forbid")


class Fase5ModuloInfo(BaseModel):
    modulo_id: int
    nombre: str
    descripcion: str
    icono: str
    color: str
    estado: str = "bloqueado"  # bloqueado | en_progreso | dominado
    porcentaje_global: int = 0
    niveles: List[Fase5NivelInfo] = Field(default_factory=list)
    desafios: List[Fase5DesafioInfo] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class Fase5Dashboard(BaseModel):
    alumno_nombre: str
    puntos_totales: int = 0
    modulos: List[Fase5ModuloInfo] = Field(default_factory=list)
    desafio_mixto_disponible: bool = False
    desafio_mixto_estado: str = "bloqueado"  # bloqueado | disponible | completado

    model_config = ConfigDict(extra="forbid")


class Fase5ResponderPregunta(BaseModel):
    modulo_id: int
    nivel_id: int
    pregunta_id: Optional[int] = None
    enunciado_seed: Optional[str] = None

    respuesta_dada: Optional[str] = None
    alternativa_id: Optional[int] = None
    tiempo_respuesta_segundos: Optional[float] = 0.0

    @model_validator(mode="after")
    def validate_topology(self) -> "Fase5ResponderPregunta":
        _validate_block_pair(self.modulo_id, self.nivel_id)
        return self


class Fase5ResultadoRespuesta(BaseModel):
    es_correcta: bool
    respuesta_correcta: Optional[str] = None
    feedback_tutor: Optional[str] = None
    feedback_error: Optional[str] = None
    explicacion: Optional[Dict[str, Any]] = None

    # Estado de progreso
    aciertos_acumulados: int = 0
    intentos_totales: int = 0
    porcentaje_actual: int = 0
    bloque_completado: bool = False
    fase_completada: bool = False

    # Bucle Espejo (Mirror Loop)
    es_espejo: bool = False
    intentos_espejo_actuales: int = 0
    intentos_espejo_max: int = 3
    soporte_avanzado: bool = False

    # Early Exit (Desafíos)
    early_exit: bool = False
    errores_sesion: int = 0
    max_errores_tolerados: int = 0
    explicacion_profunda: Optional[str] = None

    success: bool = True

    model_config = ConfigDict(extra="forbid")


class Fase5ContenidoLectura(BaseModel):
    modulo_id: int
    nivel_id: int
    titulo: str
    parrafos: List[str] = Field(default_factory=list)
    ejemplos: Optional[List[Dict[str, Any]]] = None
    tip_pedagogico: Optional[str] = None
    diccionario: Optional[Dict[str, str]] = None
    interactivos: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(extra="forbid")


class Fase5CerrarRescate(BaseModel):
    modulo_id: int
    nivel_id: int
    pregunta_id: int
    success: Optional[bool] = True
    mensaje: str = "Bucle espejo superado con éxito"
