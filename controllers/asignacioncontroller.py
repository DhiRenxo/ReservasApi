from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from schemas.asignacion import AsignacionCreate, AsignacionResponse, AsignacionUpdate
from services import asignacionservice
from app.database import get_db

router = APIRouter(
    prefix="/asignaciones",
    tags=["Asignaciones Docente Temporales"]
)


@router.post("/", response_model=AsignacionResponse, status_code=status.HTTP_201_CREATED)
def crear_asignacion(asignacion: AsignacionCreate, db: Session = Depends(get_db)):
    return asignacionservice.crear_asignacion(db, asignacion)


@router.get("/", response_model=list[AsignacionResponse])
def listar_asignaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return asignacionservice.obtener_asignaciones(db, skip, limit)


@router.get("/{asignacion_id}", response_model=AsignacionResponse)
def obtener_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    asignacion = asignacionservice.obtener_asignacion_por_id(db, asignacion_id)
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return asignacion


@router.put("/{asignacion_id}", response_model=AsignacionResponse)
def actualizar_asignacion(asignacion_id: int, datos: AsignacionUpdate, db: Session = Depends(get_db)):
    asignacion_actualizada = asignacionservice.actualizar_asignacion(db, asignacion_id, datos)
    if not asignacion_actualizada:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return asignacion_actualizada


@router.delete("/{asignacion_id}", response_model=AsignacionResponse)
def eliminar_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    asignacion = asignacionservice.eliminar_asignacion(db, asignacion_id)
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return asignacion

@router.get("/asignaciones/por-fecha", response_model=list[AsignacionResponse])
def listar_asignaciones_por_fecha(
    fecha: date = Query(..., description="Fecha de asignación en formato YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    asignaciones = asignacionservice.obtener_asignaciones_por_fecha(db, fecha)
    if not asignaciones:
        raise HTTPException(status_code=404, detail="No se encontraron asignaciones en esa fecha")
    return asignaciones