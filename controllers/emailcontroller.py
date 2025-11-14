from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db as get_db

# Importamos ambos servicios
from services.email_asignacion_service import (
    enviar_notificacion_asignacion,
    enviar_confirmacion_horario
)

router = APIRouter(
    prefix="/notificaciones",
    tags=["Notificaciones"]
)

# 📢 Notificación para registrar disponibilidad
@router.post("/asignacion/{asignacion_id}")
async def notificar_docentes(asignacion_id: int, db: AsyncSession = Depends(get_db)):
    return await enviar_notificacion_asignacion(db, asignacion_id)

# 📘 Confirmación de horario publicado
@router.post("/confirmacion/{asignacion_id}")
async def confirmar_horario(asignacion_id: int, db: AsyncSession = Depends(get_db)):
    return await enviar_confirmacion_horario(db, asignacion_id)
