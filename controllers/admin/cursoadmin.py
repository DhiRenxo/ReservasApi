from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.curso import CursoCreate, CursoResponse
from services import cursoservice as curso_service

router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.post("/", response_model=CursoResponse)
def crear(curso: CursoCreate, db: Session = Depends(get_db)):
    return curso_service.crear_curso(db, curso)

@router.get("/", response_model=list[CursoResponse])
def listar(db: Session = Depends(get_db)):
    return curso_service.listar_cursos(db)
