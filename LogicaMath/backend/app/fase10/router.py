from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal

router = APIRouter(prefix="/fase10", tags=["Fase 10: Razonamiento Abstracto y Visual"])

@router.get("/status")
async def get_fase10_status():
    return {
        "status": "reserved",
        "fase_id": 10,
        "nombre": "Razonamiento Abstracto y Visual",
        "mensaje": "Fase reservada; alcance definido, sin diseño interno."
    }
