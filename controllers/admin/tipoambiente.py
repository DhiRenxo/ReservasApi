from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db as get_async_db
from services import tipoambiente
from schemas.tiposambiente import TipoAmbienteCreate, TipoAmbienteResponse
from utils.google_auth import get_current_user

router = APIRouter(prefix="/api/tiposambiente", tags=["TipoAmbiente"])


@router.get("/", response_model=List[TipoAmbienteResponse])
async def listar_tipos(
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await tipoambiente.get_all(db)


@router.get("/{id}", response_model=TipoAmbienteResponse)
async def obtener(
    id: int,
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    rol = await tipoambiente.get_by_id(db, id)
    if not rol:
        raise HTTPException(status_code=404, detail="Tipo de ambiente no encontrado")
    return rol


@router.post("/", response_model=TipoAmbienteResponse)
async def crear_tipo(
    tipo: TipoAmbienteCreate,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await tipoambiente.create(db, tipo)
