from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from services import ambienteservice
from schemas.ambiente import AmbienteCreate, AmbienteResponse, AmbienteUpdate

router = APIRouter(prefix="/api/ambientes", tags=["Ambientes"])

@router.get("/", response_model=list[AmbienteResponse])
def listar(db: Session = Depends(get_db)):
    return ambienteservice.get_all(db)

@router.get("/{id}", response_model=AmbienteResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    ambiente = ambienteservice.get_by_id(db, id)
    if not ambiente:
        raise HTTPException(status_code=404, detail="No encontrado")
    return ambiente

@router.post("/", response_model=AmbienteResponse)
def crear(ambiente: AmbienteCreate, db: Session = Depends(get_db)):
    return ambienteservice.create(db, ambiente)

@router.put("/{id}", response_model=AmbienteResponse)
def actualizar(id: int, ambiente: AmbienteUpdate, db: Session = Depends(get_db)):
    return ambienteservice.update(db, id, ambiente)

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    ambiente = ambienteservice.delete(db, id)
    if not ambiente:
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"mensaje": "Eliminado"}
