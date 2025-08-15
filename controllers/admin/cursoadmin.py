from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.curso import CursoCreate, CursoUpdate, CursoResponse
from models.cursos import Curso
from utils.google_auth import get_current_user
from typing import List


router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.get("/", response_model=list[CursoResponse])
def list_cursos(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return db.query(Curso).all()

@router.get("/activos", response_model=list[CursoResponse])
def list_activos(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return db.query(Curso).filter(Curso.estado == True).all()

@router.get("/filtro", response_model=list[CursoResponse])
def cursos_por_filtros(
    carreid: int,
    plan: str,
    ciclo: str,
    modalidad: str,
    db: Session = Depends(get_db)
):
    cursos = db.query(Curso).filter(
        Curso.carreid == carreid,
        Curso.plan == plan,
        Curso.ciclo == ciclo,
        Curso.modalidad == modalidad,
        Curso.estado == True
    ).all()

    return cursos


@router.get("/{curso_id}", response_model=CursoResponse)
def get_curso(curso_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.post("/", response_model=CursoResponse)
def create_curso(curso: CursoCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    db_curso = Curso(**curso.dict())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

@router.put("/{curso_id}", response_model=CursoResponse)
def update_curso(curso_id: int, curso_data: CursoUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    for field, value in curso_data.dict().items():
        setattr(curso, field, value)
    db.commit()
    db.refresh(curso)
    return curso

@router.patch("/{curso_id}/cambiar-estado", response_model=CursoResponse)
def toggle_estado(curso_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso.estado = not curso.estado
    db.commit()
    db.refresh(curso)
    return curso

@router.patch("/{curso_id}/actualizar-horas/{horas}", response_model=CursoResponse)
def actualizar_horas(curso_id: int, horas: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso.horas = horas
    db.commit()
    db.refresh(curso)
    return curso

@router.post("/bulk", response_model=list[CursoResponse])
def create_cursos_bulk(
    cursos: List[CursoCreate],
    db: Session = Depends(get_db)
):
    db_cursos = [Curso(**curso.dict()) for curso in cursos]
    db.add_all(db_cursos)
    db.commit()
    for curso in db_cursos:
        db.refresh(curso)
    return db_cursos
