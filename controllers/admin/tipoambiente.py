from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from services import tipoambiente
from schemas.tiposambiente import TipoAmbienteCreate, TipoAmbienteResponse
from utils.google_auth import get_current_user

router = APIRouter(prefix="/api/tiposambiente", tags=["TipoAmbiente"])

@router.get("/", response_model=list[TipoAmbienteResponse])
def listar_tipos(db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return tipoambiente.get_all(db)

@router.get("/{id}", response_model=TipoAmbienteResponse)
def obtener(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    rol = tipoambiente.get_by_id(db, id)
    if not rol:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return rol

@router.post("/", response_model=TipoAmbienteResponse)
def crear_tipo(tipo: TipoAmbienteCreate, db: Session = Depends(get_db), dict = Depends(get_current_user)):
    return tipoambiente.create(db, tipo)
