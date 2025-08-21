# routes/asignacion.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import services.asignacionservice as asignacion_service
import schemas.asignacion as asignacion_schema
from typing import List
from utils.google_auth import get_current_user

router = APIRouter(
    prefix="/asignaciones",
    tags=["Asignaciones"]
)

# -----------------------------
# CRUD Asignacion
# -----------------------------

@router.post("/", response_model=asignacion_schema.AsignacionResponse)
def create_asignacion(asignacion: asignacion_schema.AsignacionCreate, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return asignacion_service.create_asignacion(db, asignacion)


@router.get("/", response_model=List[asignacion_schema.AsignacionResponse])
def get_asignaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return asignacion_service.get_asignaciones(db, skip, limit)


@router.get("/{asignacion_id}", response_model=asignacion_schema.AsignacionResponse)
def get_asignacion(asignacion_id: int, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    db_asignacion = asignacion_service.get_asignacion(db, asignacion_id)
    if not db_asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return db_asignacion


@router.put("/{asignacion_id}", response_model=asignacion_schema.AsignacionResponse)
def update_asignacion(asignacion_id: int, asignacion: asignacion_schema.AsignacionUpdate, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    db_asignacion = asignacion_service.update_asignacion(db, asignacion_id, asignacion)
    if not db_asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return db_asignacion


@router.patch("/{asignacion_id}/secciones", response_model=asignacion_schema.AsignacionResponse)
def update_asignacion_secciones(asignacion_id: int, update: asignacion_schema.AsignacionUpdateSecciones, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    db_asignacion = asignacion_service.update_asignacion_secciones(db, asignacion_id, update)
    if not db_asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return db_asignacion


@router.delete("/{asignacion_id}", response_model=asignacion_schema.AsignacionResponse)
def delete_asignacion(asignacion_id: int, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    db_asignacion = asignacion_service.delete_asignacion(db, asignacion_id)
    if not db_asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return db_asignacion


# -----------------------------
# Relación Asignacion - Curso - Docente
# -----------------------------

@router.patch("/{asignacion_id}/cursos", response_model=List[asignacion_schema.AsignacionCursoDocenteResponse])
def actualizar_cursos(asignacion_id: int, data: asignacion_schema.CursosUpdate, db: Session = Depends(get_db)):
    return asignacion_service.actualizar_cursos_asignacion(db, asignacion_id, data.curso_ids)

@router.post("/relacion", response_model=asignacion_schema.AsignacionCursoDocenteResponse)
def add_asignacion_curso_docente(relacion: asignacion_schema.AsignacionCursoDocenteCreate, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return asignacion_service.add_asignacion_curso_docente(db, relacion)


@router.get("/{asignacion_id}/relaciones", response_model=List[asignacion_schema.AsignacionCursoDocenteResponse])
def get_asignacion_curso_docentes(asignacion_id: int, db: Session = Depends(get_db)):
    return asignacion_service.get_asignacion_curso_docentes(db, asignacion_id)


@router.patch("/{asignacion_id}/estado", response_model=asignacion_schema.AsignacionResponse)
def cambiar_estado_asignacion(
    asignacion_id: int,
    data: dict, 
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if "estado" not in data:
        raise HTTPException(status_code=400, detail="El campo 'estado' es requerido")

    estado_value = data["estado"]

    if isinstance(estado_value, str):
        estado_value = estado_value.lower() in ["true", "1", "yes"]
    elif isinstance(estado_value, int):
        estado_value = bool(estado_value)

    asignacion = asignacion_service.update_asignacion_estado(db, asignacion_id, estado_value)
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    return asignacion

@router.patch("/{asignacion_id}/relaciones/docente", response_model=asignacion_schema.AsignacionCursoDocenteResponse)
def actualizar_docente(asignacion_id: int, data: asignacion_schema.DocenteUpdate, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    relacion = asignacion_service.update_docente_curso_asignacion(
        db, asignacion_id, data.curso_id, data.docente_id
    )
    if not relacion:
        raise HTTPException(status_code=404, detail="No se encontró la relación asignación-curso")
    return relacion