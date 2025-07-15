from sqlalchemy.orm import Session
from models.docente import Docente
from schemas.docente import DocenteCreate, DocenteUpdate

def listar_docentes(db: Session):
    return db.query(Docente).filter(Docente.estado == True).all()

def obtener_docente(db: Session, docente_id: int):
    return db.query(Docente).filter(Docente.id == docente_id).first()

def crear_docente(db: Session, docente: DocenteCreate):
    db_docente = Docente(**docente.dict())
    db.add(db_docente)
    db.commit()
    db.refresh(db_docente)
    return db_docente

def actualizar_docente(db: Session, docente_id: int, docente: DocenteUpdate):
    db_docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if db_docente:
        for key, value in docente.dict().items():
            setattr(db_docente, key, value)
        db.commit()
        db.refresh(db_docente)
    return db_docente

def eliminar_docente(db: Session, docente_id: int):
    db_docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if db_docente:
        db_docente.estado = False
        db.commit()
    return db_docente
