from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from services.asignaciondocenteservice import AsignacionDocenteService
from utils.google_auth import get_current_user

router = APIRouter(prefix="/asignacion-docente", tags=["Asignación Docente"])

@router.get("/horas/{docente_id}")
def obtener_horas_docente(docente_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    service = AsignacionDocenteService(db)
    horas = service.calcular_horas_temporales(docente_id)
    return {"docente_id": docente_id, "horastemporales": horas}

@router.get("/horas-todos")
def obtener_horas_todos(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    service = AsignacionDocenteService(db)
    return service.calcular_horas_todos_docentes()
