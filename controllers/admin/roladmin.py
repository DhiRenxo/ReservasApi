from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from schemas.rol import RolCreate, RolResponse, RolUpdate
from services import rolservice
from utils.google_auth import get_current_user

router = APIRouter(prefix="/api/roles", tags=["Roles"])

@router.get("/", response_model=list[RolResponse])
async def listar(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    return await rolservice.get_all(db)

@router.get("/{id}", response_model=RolResponse)
async def obtener(id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    rol = await rolservice.get_by_id(db, id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.post("/", response_model=RolResponse)
async def crear(data: RolCreate, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    return await rolservice.create(db, data)

@router.put("/{id}", response_model=RolResponse)
async def actualizar(id: int, data: RolUpdate, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    rol = await rolservice.update(db, id, data)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol
