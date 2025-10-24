from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from services.email_asignacion_service import enviar_notificacion_asignacion

router = APIRouter(
    prefix="/notificaciones",
    tags=["Notificaciones"]
)

@router.post("/asignacion/{asignacion_id}")
async def notificar_docentes(asignacion_id: int, db: AsyncSession = Depends(get_db)):
    return await enviar_notificacion_asignacion(db, asignacion_id)
