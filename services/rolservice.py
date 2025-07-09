from sqlalchemy.orm import Session
from models.rol import Rol
from schemas.rol import RolCreate

def get_all(db: Session):
    return db.query(Rol).all()

def create(db: Session, data: RolCreate):
    nuevo = Rol(nombre=data.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
