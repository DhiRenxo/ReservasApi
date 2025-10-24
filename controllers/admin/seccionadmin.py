from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import List
from app.database import get_db as get_async_db
from schemas import seccion as schemas
from services import seccionservice as service
from utils.google_auth import get_current_user

router = APIRouter(prefix="/secciones", tags=["Secciones"])


@router.post("/", response_model=schemas.Seccion)
async def crear_seccion(
    seccion: schemas.SeccionCreate,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await service.crear_seccion(db, seccion)


@router.get("/", response_model=List[schemas.Seccion])
async def listar_secciones(
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await service.obtener_secciones(db)


@router.get("/{id}", response_model=schemas.Seccion)
async def obtener_seccion(
    id: int,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    seccion = await service.obtener_seccion_por_id(db, id)
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    return seccion


@router.put("/{id}", response_model=schemas.Seccion)
async def actualizar_seccion(
    id: int,
    seccion: schemas.SeccionUpdate,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await service.actualizar_seccion(db, id, seccion)


@router.delete("/{id}", response_model=schemas.Seccion)
async def eliminar_seccion(
    id: int,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await service.eliminar_seccion(db, id)


@router.patch("/estado/{id}", response_model=schemas.Seccion)
async def cambiar_estado(
    id: int,
    estado_obj: schemas.SeccionEstado,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await service.actualizar_estado_seccion(db, id, estado_obj.estado)


@router.post("/reactivar/{id}", response_model=schemas.Seccion)
async def reactivar_seccion(
    id: int,
    nuevo_inicio: date,
    nuevo_fin: date,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await service.reactivar_seccion_creando_nueva(db, id, nuevo_inicio, nuevo_fin)
