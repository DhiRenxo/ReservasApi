from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from services.asignacionservice import (
    crear_asignacion,
    obtener_asignaciones,
    obtener_asignacion_por_id,
    actualizar_asignacion,
    actualizar_estado_asignacion,
    eliminar_asignacion
)
from schemas.asignacion import (
    AsignacionCreate,
    AsignacionUpdate,
    AsignacionEstadoUpdate,
    AsignacionDelete
)

from utils.google_auth import get_current_user

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear(asignacion: AsignacionCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    print("📩 Datos recibidos del frontend:", asignacion.dict())
    return crear_asignacion(db, asignacion)

@router.get("/")
def listar(db: Session = Depends(get_db),  user: dict = Depends(get_current_user)):
    return obtener_asignaciones(db)

@router.get("/{asignacion_id}")
def obtener(asignacion_id: int, db: Session = Depends(get_db),  user: dict = Depends(get_current_user)):
    asignacion = obtener_asignacion_por_id(db, asignacion_id)
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return asignacion

@router.put("/{asignacion_id}")
def actualizar(asignacion_id: int, datos: AsignacionUpdate, db: Session = Depends(get_db),  user: dict = Depends(get_current_user)):
    asignacion_actualizada = actualizar_asignacion(db, asignacion_id, datos)
    if not asignacion_actualizada:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return asignacion_actualizada

@router.patch("/{asignacion_id}/estado")
def cambiar_estado(asignacion_id: int, estado_data: AsignacionEstadoUpdate, db: Session = Depends(get_db),  user: dict = Depends(get_current_user)):
    asignacion = actualizar_estado_asignacion(db, asignacion_id, estado_data)
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return asignacion

@router.delete("/")
def eliminar(delete_data: AsignacionDelete, db: Session = Depends(get_db),  user: dict = Depends(get_current_user)):
    asignacion = eliminar_asignacion(db, delete_data)
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return {"mensaje": "Asignación desactivada correctamente"}
