from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import seccion as schemas
from services import seccionservice as service
from app.database import get_db
from datetime import date
from utils.google_auth import get_current_user


router = APIRouter(prefix="/secciones", tags=["Secciones"])

@router.post("/", response_model=schemas.Seccion)
def crear_seccion(seccion: schemas.SeccionCreate, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return service.crear_seccion(db, seccion)

@router.get("/", response_model=list[schemas.Seccion])
def listar_secciones(db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return service.obtener_secciones(db)

@router.get("/{id}", response_model=schemas.Seccion)
def obtener_seccion(id: int, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    seccion = service.obtener_seccion_por_id(db, id)
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    return seccion

@router.put("/{id}", response_model=schemas.Seccion)
def actualizar_seccion(id: int, seccion: schemas.SeccionUpdate, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return service.actualizar_seccion(db, id, seccion)

@router.delete("/{id}", response_model=schemas.Seccion)
def eliminar_seccion(id: int, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return service.eliminar_seccion(db, id)

@router.patch("/estado/{id}", response_model=schemas.Seccion)
def cambiar_estado(id: int, estado_obj: schemas.SeccionEstado, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return service.actualizar_estado_seccion(db, id, estado_obj.estado)


@router.post("/reactivar/{id}", response_model=schemas.Seccion)
def reactivar_seccion(
    id: int,
    nuevo_inicio: date,
    nuevo_fin: date,
    db: Session = Depends(get_db),
    dict = Depends(get_current_user)
):
    return service.reactivar_seccion_creando_nueva(db, id, nuevo_inicio, nuevo_fin)

