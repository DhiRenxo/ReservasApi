from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from models.ambiente import Ambiente
from models.tipoambiente import TipoAmbiente
from schemas.ambiente import AmbienteCreate, AmbienteUpdate


def get_all(db: Session):
    return db.query(Ambiente).options(joinedload(Ambiente.tipo_ambiente)).all()


def get_by_id(db: Session, id: int):
    return db.query(Ambiente).options(joinedload(Ambiente.tipo_ambiente)).filter(Ambiente.id == id).first()


def create(db: Session, data: AmbienteCreate):

    existe = db.query(Ambiente).filter(Ambiente.codigo == data.codigo).first()
    if existe:
        raise HTTPException(status_code=400, detail="El código ya existe")


    tipo = db.query(TipoAmbiente).filter(TipoAmbiente.id == data.tipoid).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de ambiente no válido")

    nuevo = Ambiente(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update(db: Session, id: int, data: AmbienteUpdate):
    ambiente = get_by_id(db, id)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")


    if data.codigo != ambiente.codigo:
        existe = db.query(Ambiente).filter(Ambiente.codigo == data.codigo).first()
        if existe:
            raise HTTPException(status_code=400, detail="El código ya existe")

    tipo = db.query(TipoAmbiente).filter(TipoAmbiente.id == data.tipoid).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de ambiente no válido")

    for key, value in data.dict().items():
        setattr(ambiente, key, value)

    db.commit()
    db.refresh(ambiente)
    return ambiente


def delete(db: Session, id: int):
    ambiente = get_by_id(db, id)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")
    
    db.delete(ambiente)
    db.commit()
    return ambiente
