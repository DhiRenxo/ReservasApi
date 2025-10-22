from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from services import usuarioservice
from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioDocenteCodigoUpdate
from utils.google_auth import get_current_user 

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.get("/", response_model=list[UsuarioResponse])
def listar(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return usuarioservice.get_all(db)

@router.get("/{id}", response_model=UsuarioResponse)
def obtener(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    usuario = usuarioservice.get_by_id(db, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear(usuario: UsuarioCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return usuarioservice.create(db, usuario)

@router.put("/{id}", response_model=UsuarioResponse)
def actualizar(id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    actualizado = usuarioservice.update(db, id, usuario)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return actualizado

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    eliminado = usuarioservice.delete(db, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}

@router.put("/{usuario_id}/cod-docente", response_model=UsuarioResponse)
def actualizar_cod_docente(
    usuario_id: int,
    datos: UsuarioDocenteCodigoUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    usuario_actualizado = usuarioservice.actualizar_cod_docente_service(db, usuario_id, datos)
    return usuario_actualizado