from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db as get_db
from services import usuarioservice
from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioDocenteCodigoUpdate
from utils.google_auth import get_current_user

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.get("/", response_model=list[UsuarioResponse])
async def listar(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    return await usuarioservice.get_all(db)

@router.get("/{id}", response_model=UsuarioResponse)
async def obtener(id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    usuario = await usuarioservice.get_by_id(db, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioResponse, status_code=201)
async def crear(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    return await usuarioservice.create(db, usuario)

@router.put("/{id}", response_model=UsuarioResponse)
async def actualizar(id: int, usuario: UsuarioUpdate, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    actualizado = await usuarioservice.update(db, id, usuario)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return actualizado

@router.delete("/{id}")
async def eliminar(id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    eliminado = await usuarioservice.delete(db, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}

@router.put("/{usuario_id}/cod-docente", response_model=UsuarioResponse)
async def actualizar_cod_docente(
    usuario_id: int,
    datos: UsuarioDocenteCodigoUpdate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return await usuarioservice.actualizar_cod_docente_service(db, usuario_id, datos)
