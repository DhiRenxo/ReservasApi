from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import services.docenteservice as docente_service
from schemas.docente import DocenteCreate, DocenteUpdate, DocenteOut
from typing import List
from utils.google_auth import get_current_user

router = APIRouter(
    prefix="/api/docentes",
    tags=["Docentes"]
)

@router.get("/", response_model=List[DocenteOut])
def listar(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return docente_service.listar_docentes(db)

@router.get("/{docente_id}", response_model=DocenteOut)
def obtener(docente_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    docente = docente_service.obtener_docente(db, docente_id)
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return docente

@router.post("/", response_model=DocenteOut)
def crear(docente: DocenteCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return docente_service.crear_docente(db, docente)

@router.put("/{docente_id}", response_model=DocenteOut)
def actualizar(docente_id: int, docente: DocenteUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    actualizado = docente_service.actualizar_docente(db, docente_id, docente)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return actualizado

@router.delete("/{docente_id}", response_model=DocenteOut)
def eliminar(docente_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    eliminado = docente_service.eliminar_docente(db, docente_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return eliminado
