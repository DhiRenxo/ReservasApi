from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from services import ambienteservice
from schemas.ambiente import AmbienteCreate, AmbienteResponse, AmbienteUpdate, AmbienteEstado
from utils.google_auth import get_current_user  

router = APIRouter(prefix="/api/ambientes", tags=["Ambientes"])


@router.get("/", response_model=list[AmbienteResponse])
async def listar_ambientes(
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    return await ambienteservice.get_all(db)


@router.get("/{id}", response_model=AmbienteResponse)
async def obtener_ambiente(
    id: int,
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    ambiente = await ambienteservice.get_by_id(db, id)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")
    return ambiente


@router.post("/", response_model=AmbienteResponse)
async def crear_ambiente(
    ambiente: AmbienteCreate,
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    return await ambienteservice.create(db, ambiente)


@router.put("/{id}", response_model=AmbienteResponse)
async def actualizar_ambiente(
    id: int,
    ambiente: AmbienteUpdate,
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    return await ambienteservice.update(db, id, ambiente)


@router.delete("/{id}")
async def eliminar_ambiente(
    id: int,
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    eliminado = await ambienteservice.delete(db, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")
    return {"mensaje": "Ambiente eliminado correctamente"}


@router.patch("/estado/{id}", response_model=AmbienteEstado)
async def cambiar_estado(
    id: int,
    estado_obj: AmbienteEstado,
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    return await ambienteservice.actualizar_estado_ambiente(db, id, estado_obj.estado)
