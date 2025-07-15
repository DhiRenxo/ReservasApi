from sqlalchemy.orm import Session
from models.cursos import Curso
from schemas.curso import CursoCreate

def crear_curso(db: Session, curso_data: CursoCreate):
    curso = Curso(**curso_data.dict())
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso

def listar_cursos(db: Session):
    return db.query(Curso).all()
