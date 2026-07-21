from typing import List, Optional
import os
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from botocore.exceptions import ClientError

from ..db.session import get_db
from ..auth import get_current_user, get_admin_user
from ..models.ux_feedback import UXFeedback
from ..models.enums import FeedbackStatusEnum
from ..schemas import UXFeedbackCreate, UXFeedbackUpdate, UXFeedbackResponse
from ..core.storage import storage_service

router = APIRouter(prefix="/evaluador", tags=["evaluador"])

@router.post("/feedback", response_model=UXFeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_ux_feedback(
    payload: UXFeedbackCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Crea una nueva anotación de feedback UX y persistencia contextual en el modo evaluador.
    """
    db_feedback = UXFeedback(**payload.model_dump())
    db.add(db_feedback)
    try:
        await db.commit()
        await db.refresh(db_feedback)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar la anotación de UX en la base de datos: {str(e)}"
        )
    return db_feedback

@router.get("/feedback", response_model=List[UXFeedbackResponse])
async def list_ux_feedbacks(
    fase: Optional[int] = None,
    estado: Optional[FeedbackStatusEnum] = None,
    prioridad: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    admin_user: dict = Depends(get_admin_user)
):
    """
    Lista y filtra todas las anotaciones de UX reportadas. Requiere permisos de administrador.
    """
    query = select(UXFeedback)
    
    if fase is not None:
        query = query.where(UXFeedback.fase == fase)
    if estado is not None:
        query = query.where(UXFeedback.estado == estado)
    if prioridad is not None:
        query = query.where(UXFeedback.prioridad == prioridad)
        
    query = query.order_by(UXFeedback.fecha_creacion.desc())
    
    result = await db.execute(query)
    feedbacks = result.scalars().all()
    return feedbacks

@router.patch("/feedback/{feedback_id}", response_model=UXFeedbackResponse)
async def update_ux_feedback(
    feedback_id: int,
    payload: UXFeedbackUpdate,
    db: AsyncSession = Depends(get_db),
    admin_user: dict = Depends(get_admin_user)
):
    """
    Actualiza el estado de resolución y las notas del desarrollador para una anotación.
    Requiere permisos de administrador.
    """
    result = await db.execute(select(UXFeedback).where(UXFeedback.id == feedback_id))
    db_feedback = result.scalar_one_or_none()
    
    if not db_feedback:
        raise HTTPException(
            status_code=404,
            detail="Anotación de UX no encontrada"
        )
        
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_feedback, key, value)
        
    try:
        await db.commit()
        await db.refresh(db_feedback)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar la anotación en base de datos: {str(e)}"
        )
        
    return db_feedback

@router.get("/feedback/screenshots/{filename}")
async def get_feedback_screenshot(filename: str):
    safe_filename = os.path.basename(filename)
    local_path = os.path.join("app", "static", "screenshots", safe_filename)
    if os.path.exists(local_path):
        return FileResponse(local_path)

    if not storage_service.s3_client:
        raise HTTPException(status_code=404, detail="Screenshot no encontrada localmente y S3 no configurado.")

    def _fetch_from_s3():
        try:
            key = f"screenshots/{safe_filename}"
            response = storage_service.s3_client.get_object(Bucket=storage_service.bucket_name, Key=key)
            content = response['Body'].read()
            content_type = response.get('ContentType', 'image/png')
            return content, content_type
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code in ('NoSuchKey', '404'):
                return None, None
            raise

    try:
        loop = asyncio.get_event_loop()
        content, content_type = await loop.run_in_executor(None, _fetch_from_s3)
        if content is None:
            raise HTTPException(status_code=404, detail="Screenshot no encontrada")
        return Response(content=content, media_type=content_type)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching screenshot {filename}: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo la captura de pantalla")

@router.post("/feedback/upload-screenshot")
async def upload_feedback_screenshot_endpoint(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Sube una captura de pantalla para un reporte UX Feedback.
    """
    contents = await file.read()
    try:
        url = await storage_service.upload_feedback_screenshot(contents, file.filename)
        return {"url": url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo al subir la captura de pantalla: {str(e)}"
        )
