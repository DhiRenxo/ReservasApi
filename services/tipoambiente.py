from sqlalchemy.orm import Session
from models.tipoambiente import TipoAmbiente
from schemas.tiposambiente import TipoAmbienteCreate

def get_all(db: Session):
    return db.query(TipoAmbiente).all()

def get_by_id(db: Session, id: int):
    return db.query(TipoAmbiente).filter(TipoAmbiente.id == id).first()

def create(db: Session, tipo: TipoAmbienteCreate):
    nuevo = TipoAmbiente(**tipo.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
