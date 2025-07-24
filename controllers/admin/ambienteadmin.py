from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from services import ambienteservice
from schemas.ambiente import AmbienteCreate, AmbienteResponse, AmbienteUpdate, AmbienteEstado
from utils.google_auth import get_current_user  

router = APIRouter(prefix="/api/ambientes", tags=["Ambientes"])

@router.get("/", response_model=list[AmbienteResponse])
def listar_ambientes(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return ambienteservice.get_all(db)

@router.get("/{id}", response_model=AmbienteResponse)
def obtener_ambiente(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    ambiente = ambienteservice.get_by_id(db, id)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")
    return ambiente

@router.post("/", response_model=AmbienteResponse)
def crear_ambiente(
    ambiente: AmbienteCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return ambienteservice.create(db, ambiente)

@router.put("/{id}", response_model=AmbienteResponse)
def actualizar_ambiente(
    id: int,
    ambiente: AmbienteUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return ambienteservice.update(db, id, ambiente)

@router.delete("/{id}")
def eliminar_ambiente(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    eliminado = ambienteservice.delete(db, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")
    return {"mensaje": "Ambiente eliminado correctamente"}


@router.patch("/estado/{id}", response_model=AmbienteEstado)
def cambiar_estado(id: int, estado_obj: AmbienteEstado, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return ambienteservice.actualizar_estado_seccion(db, id, estado_obj.estado)