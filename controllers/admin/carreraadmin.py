from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
import services.carreraservice as service
from schemas.carrera import CarreraOut, CarreraCreate, CarreraUpdate
from typing import List
from utils.google_auth import get_current_user

router = APIRouter(prefix="/carreras", tags=["Carreras"])


@router.get("/", response_model=List[CarreraOut])
async def listar_carreras(db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    return await service.get_all(db)


@router.get("/{carrera_id}", response_model=CarreraOut)
async def obtener_carrera(carrera_id: int, db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    carrera = await service.get_by_id(db, carrera_id)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera


@router.post("/", response_model=CarreraOut)
async def crear_carrera(carrera: CarreraCreate, db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    return await service.create(db, carrera)


@router.put("/{carrera_id}", response_model=CarreraOut)
async def actualizar_carrera(carrera_id: int, carrera_update: CarreraUpdate, db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    carrera = await service.update(db, carrera_id, carrera_update)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera


@router.delete("/{carrera_id}", response_model=CarreraOut)
async def eliminar_carrera(carrera_id: int, db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    carrera = await service.delete(db, carrera_id)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera
