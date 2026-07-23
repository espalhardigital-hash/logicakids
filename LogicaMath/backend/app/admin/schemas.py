from pydantic import BaseModel, Field
from typing import Optional, List

class NivelTeoriaSave(BaseModel):
    fase_id: int
    modulo_id: int
    nivel_id: int
    titulo: str
    texto_descubrimiento: str
    diccionario: Optional[dict] = None
    advertencia: Optional[str] = None
    ejemplos: Optional[list] = None
    interactivos: Optional[list] = None

class ProgressOverridePayload(BaseModel):
    fase_id: int
    seccion: int
    operacion: str
    action: str # "approve", "unlock", "lock"
    motivo: str = Field(..., min_length=10, description="Motivo pedagógico obligatorio de la intervención (mín. 10 caracteres).")

class ProgressOverrideItem(BaseModel):
    fase_id: int
    seccion: int
    operacion: str

class ProgressOverrideBulkPayload(BaseModel):
    items: List[ProgressOverrideItem]
    action: str # "approve", "unlock", "lock"
    motivo: str = Field(..., min_length=10, description="Motivo pedagógico obligatorio de la intervención (mín. 10 caracteres).")
    # Cuando True, el backend expande la acción a TODAS las secciones activas de las fases
    # involucradas (usado por el botón "Aprobar Fase completa"). Cuando False (default),
    # aplica exactamente a los items enviados — el frontend ya computó el conjunto retrógado.
    expand_phase: bool = False

class SystemConfigUpdate(BaseModel):
    vps_host: str
    ssh_user: str
    database_url: str
