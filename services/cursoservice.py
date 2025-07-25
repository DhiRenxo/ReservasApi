from sqlalchemy.orm import Session
from models.cursos import Curso
from schemas.curso import CursoCreate, CursoUpdate

def get_all(db: Session):
    return db.query(Curso).all()

def get_active(db: Session):
    return db.query(Curso).filter(Curso.estado == True).all()

def get_by_id(db: Session, curso_id: int):
    return db.query(Curso).filter(Curso.id == curso_id).first()

def create(db: Session, curso: CursoCreate):
    db_curso = Curso(**curso.dict())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

def update(db: Session, curso_id: int, curso_data: CursoUpdate):
    curso = get_by_id(db, curso_id)
    if curso:
        for field, value in curso_data.dict().items():
            setattr(curso, field, value)
        db.commit()
        db.refresh(curso)
    return curso

def toggle_estado(db: Session, curso_id: int):
    curso = get_by_id(db, curso_id)
    if curso:
        curso.estado = not curso.estado
        db.commit()
        db.refresh(curso)
    return curso

def update_horas(db: Session, curso_id: int, horas: int):
    curso = get_by_id(db, curso_id)
    if curso:
        curso.horas = horas
        db.commit()
        db.refresh(curso)
    return curso

def get_by_carrera_plan_ciclo(db: Session, carreid: int, plan: str, ciclo: str):
    return db.query(Curso).filter(
        Curso.carreid == carreid,
        Curso.plan == plan,
        Curso.ciclo == ciclo,
        Curso.estado == True
    ).all()
