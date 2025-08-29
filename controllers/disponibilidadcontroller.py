from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from utils.google_auth import get_current_user
from app.database import get_db
from models.DisponibilidadDocente import DisponibilidadDocente
from services.disponibilidadservice import DisponibilidadService, get_disponibilidades_by_docente
from schemas.Disponibilidad import (
    DisponibilidadDocenteCreate,
    DisponibilidadDocenteUpdate,
    DisponibilidadDocenteResponse
)

router = APIRouter(prefix="/disponibilidad", tags=["Disponibilidad Docente"])

# Crear o actualizar disponibilidad (usa service.create_or_update)
@router.post("/", response_model=DisponibilidadDocenteResponse)
def create_disponibilidad(
    data: DisponibilidadDocenteCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = DisponibilidadService(db)
    return service.create_or_update(data)


# Obtener disponibilidades de un docente (filtros opcionales)
@router.get("/docente/{docente_id}", response_model=List[DisponibilidadDocenteResponse])
def get_disponibilidad_docente(
    docente_id: int,
    modalidad: str | None = Query(None, description="Filtrar por modalidad"),
    turno: str | None = Query(None, description="Filtrar por turno"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = DisponibilidadService(db)
    disponibilidades = service.get_by_docente(docente_id, modalidad, turno)
    
    # En lugar de 404 → devolver lista vacía
    return disponibilidades or []



# Obtener disponibilidad por ID
@router.get("/{id}", response_model=DisponibilidadDocenteResponse)
def get_disponibilidad(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = DisponibilidadService(db)
    disponibilidad = service.get_by_id(id)
    if not disponibilidad:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")
    return disponibilidad


# Actualizar disponibilidad
@router.put("/{id}", response_model=DisponibilidadDocenteResponse)
def update_disponibilidad(
    id: int,
    data: DisponibilidadDocenteUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = DisponibilidadService(db)
    disponibilidad = service.update(id, data)
    if not disponibilidad:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")
    return disponibilidad


# Eliminar disponibilidad (docente_id + modalidad + turno + dia)
@router.delete("/")
def delete_disponibilidad(
    docente_id: int = Query(..., description="ID del docente"),
    modalidad: str = Query(..., description="Modalidad"),
    turno: str = Query(..., description="Turno"),
    dia: str = Query(..., description="Día"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    service = DisponibilidadService(db)
    eliminado = service.delete(docente_id, modalidad, turno, dia)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")
    return {"message": "Disponibilidad eliminada correctamente"}


@router.put(
    "/docente/{docente_id}/{modalidad}/{turno}", 
    response_model=List[DisponibilidadDocenteResponse]
)
def upsert_disponibilidades_docente(
    docente_id: int,
    modalidad: str,
    turno: str,
    disponibilidades_update: List[DisponibilidadDocenteUpdate],
    db: Session = Depends(get_db)
):
    updated_items = []

    for disp_data in disponibilidades_update:
        # Convertir horarios en dicts serializables
        horarios_dicts = [h.dict() for h in disp_data.horarios] if disp_data.horarios else []

        # Buscar si ya existe
        existente = db.query(DisponibilidadDocente).filter(
            DisponibilidadDocente.docente_id == docente_id,
            DisponibilidadDocente.dia == disp_data.dia,
            DisponibilidadDocente.modalidad == modalidad,
            DisponibilidadDocente.turno == turno
        ).first()

        if existente:
            # Actualizar
            existente.dia = disp_data.dia or existente.dia
            existente.horarios = horarios_dicts
            updated_items.append(existente)
        else:
            # Crear nuevo
            nuevo = DisponibilidadDocente(
                docente_id=docente_id,
                modalidad=modalidad,
                turno=turno,
                dia=disp_data.dia,
                horarios=horarios_dicts  # <-- ahora sí JSON válido
            )
            db.add(nuevo)
            updated_items.append(nuevo)

    db.commit()
    for u in updated_items:
        db.refresh(u)

    return updated_items