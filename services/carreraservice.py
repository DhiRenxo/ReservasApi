from sqlalchemy.orm import Session
from models.carrera import Carrera
from schemas.carrera import CarreraCreate, CarreraUpdate

def get_all(db: Session):
    return db.query(Carrera).all()

def get_by_id(db: Session, carrera_id: int):
    return db.query(Carrera).filter(Carrera.id == carrera_id).first()

def create(db: Session, carrera: CarreraCreate):
    db_carrera = Carrera(**carrera.dict())
    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

def update(db: Session, carrera_id: int, carrera_update: CarreraUpdate):
    db_carrera = get_by_id(db, carrera_id)
    if not db_carrera:
        return None
    for key, value in carrera_update.dict().items():
        setattr(db_carrera, key, value)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

def delete(db: Session, carrera_id: int):
    db_carrera = get_by_id(db, carrera_id)
    if not db_carrera:
        return None
    db.delete(db_carrera)
    db.commit()
    return db_carrera
