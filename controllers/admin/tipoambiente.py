from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from services import tipoambiente
from schemas.tiposambiente import TipoAmbienteCreate, TipoAmbienteResponse

router = APIRouter(prefix="/api/tiposambiente", tags=["TipoAmbiente"])

@router.get("/", response_model=list[TipoAmbienteResponse])
def listar_tipos(db: Session = Depends(get_db)):
    return tipoambiente.get_all(db)

@router.post("/", response_model=TipoAmbienteResponse)
def crear_tipo(tipo: TipoAmbienteCreate, db: Session = Depends(get_db)):
    return tipoambiente.create(db, tipo)
