import os
import json
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..auth import get_admin_user

router = APIRouter()

# Schema for the teacher's comment
class FeedbackRequest(BaseModel):
  fase_id: int
  seccion_id: int
  pregunta_id: Optional[int] = None
  tipo: str  # "pregunta", "teoria", "interactivo"
  comentario: str

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def create_feedback(
  payload: FeedbackRequest,
  current_user: dict = Depends(get_admin_user)
):
  """
  Guarda la retroalimentación del docente para una pregunta, teoría o interactivo.
  Escribe los comentarios estructurados en 'data/feedback_docente.json'.
  """
  if not payload.comentario.strip():
    raise HTTPException(
      status_code=400,
      detail="El comentario no puede estar vacío"
    )

  # Data path setup to persist comments inside docker volume mount
  # Path matches backend/data/feedback_docente.json in host workspace
  data_dir = "data"
  os.makedirs(data_dir, exist_ok=True)
  filepath = os.path.join(data_dir, "feedback_docente.json")

  # Prepare the new feedback item
  feedback_item = {
    "id": str(datetime.utcnow().timestamp()),
    "fase_id": payload.fase_id,
    "seccion_id": payload.seccion_id,
    "pregunta_id": payload.pregunta_id,
    "tipo": payload.tipo,
    "comentario": payload.comentario,
    "docente_username": current_user.get("username"),
    "docente_email": current_user.get("email"),
    "timestamp": datetime.utcnow().isoformat()
  }

  feedbacks = []
  if os.path.exists(filepath):
    try:
      with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:
          feedbacks = json.loads(content)
    except Exception as e:
      # If file is corrupted or not a valid list, initialize empty list
      feedbacks = []

  feedbacks.append(feedback_item)

  try:
    with open(filepath, "w", encoding="utf-8") as f:
      json.dump(feedbacks, f, ensure_ascii=False, indent=2)
  except Exception as e:
    raise HTTPException(
      status_code=500,
      detail=f"Error al escribir en la base de datos de comentarios: {str(e)}"
    )

  return {"message": "Retroalimentación guardada con éxito", "id": feedback_item["id"]}
