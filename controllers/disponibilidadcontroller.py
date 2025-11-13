from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from utils.google_auth import get_current_user
from app.database import get_async_db
from services.disponibilidadservice import DisponibilidadService
from schemas.Disponibilidad import (
    DisponibilidadDocenteCreate,
    DisponibilidadDocenteUpdate,
    DisponibilidadDocenteResponse
)

router = APIRouter(prefix="/disponibilidad", tags=["Disponibilidad Docente"])

# --- Docente: Crear o actualizar ---
@router.post("/", response_model=DisponibilidadDocenteResponse)
async def create_disponibilidad(
    data: DisponibilidadDocenteCreate,
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    service = DisponibilidadService(db)
    disponibilidad = await service.create_or_update(data, user["email"])
    if not disponibilidad:
        raise HTTPException(status_code=400, detail="Docente no encontrado")
    return disponibilidad

# --- Docente: Actualizar ---
@router.put("/{id}", response_model=DisponibilidadDocenteResponse)
async def update_disponibilidad(
    id: int,
    data: DisponibilidadDocenteUpdate,
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    service = DisponibilidadService(db)
    disponibilidad = await service.update(id, data, user["email"])
    if not disponibilidad:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada o sin permisos")
    return disponibilidad

# --- Docente: Eliminar ---
@router.delete("/")
async def delete_disponibilidad(
    dia: str = Query(...),
    modalidad: str = Query(...),
    turno: str = Query(...),
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    service = DisponibilidadService(db)
    eliminado = await service.delete(dia, modalidad, turno, user["email"])
    if not eliminado:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada o sin permisos")
    return {"message": "Disponibilidad eliminada correctamente"}

# --- Administrador: Listar disponibilidades de cualquier docente ---
@router.get("/docente/{docente_id}", response_model=List[DisponibilidadDocenteResponse])
async def get_disponibilidad_docente(
    docente_id: int,
    modalidad: str | None = Query(None),
    turno: str | None = Query(None),
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    service = DisponibilidadService(db)
    disponibilidades = await service.get_by_docente(docente_id, modalidad, turno)
    return disponibilidades or []

# --- Administrador: Obtener disponibilidad por ID ---
@router.get("/{id}", response_model=DisponibilidadDocenteResponse)
async def get_disponibilidad(
    id: int,
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    service = DisponibilidadService(db)
    disponibilidad = await service.get_by_id(id)
    if not disponibilidad:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")
    return disponibilidad
