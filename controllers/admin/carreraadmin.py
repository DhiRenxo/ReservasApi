from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import services.carreraservice as service
from schemas.carrera import CarreraOut, CarreraCreate, CarreraUpdate
from typing import List
from utils.google_auth import get_current_user

router = APIRouter(prefix="/carreras", tags=["Carreras"])

@router.get("/", response_model=List[CarreraOut])
def listar_carreras(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return service.get_all(db)

@router.get("/{carrera_id}", response_model=CarreraOut)
def obtener_carrera(carrera_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    carrera = service.get_by_id(db, carrera_id)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera

@router.post("/", response_model=CarreraOut)
def crear_carrera(carrera: CarreraCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return service.create(db, carrera)

@router.put("/{carrera_id}", response_model=CarreraOut)
def actualizar_carrera(carrera_id: int, carrera_update: CarreraUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    carrera = service.update(db, carrera_id, carrera_update)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera

@router.delete("/{carrera_id}", response_model=CarreraOut)
def eliminar_carrera(carrera_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    carrera = service.delete(db, carrera_id)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera
