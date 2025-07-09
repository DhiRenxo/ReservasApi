from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from services import usuarioservice
from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.get("/", response_model=list[UsuarioResponse])
def listar(db: Session = Depends(get_db)):
    return usuarioservice.get_all(db)

@router.get("/{id}", response_model=UsuarioResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    usuario = usuarioservice.get_by_id(db, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="No encontrado")
    return usuario

@router.post("/", response_model=UsuarioResponse)
def crear(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return usuarioservice.create(db, usuario)

@router.put("/{id}", response_model=UsuarioResponse)
def actualizar(id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    return usuarioservice.update(db, id, usuario)

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    usuario = usuarioservice.delete(db, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"mensaje": "Eliminado"}
