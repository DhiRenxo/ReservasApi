from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_async_db
from schemas.curso import CursoCreate, CursoUpdate, CursoResponse
from models.cursos import Curso
from utils.google_auth import get_current_user
from typing import List

router = APIRouter(prefix="/cursos", tags=["Cursos"])


@router.get("/", response_model=List[CursoResponse])
async def list_cursos(db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    result = await db.execute(select(Curso))
    return result.scalars().all()


@router.get("/activos", response_model=List[CursoResponse])
async def list_activos(db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    result = await db.execute(select(Curso).where(Curso.estado == True))
    return result.scalars().all()


@router.get("/filtro", response_model=List[CursoResponse])
async def cursos_por_filtros(
    carreid: int,
    plan: str,
    ciclo: str,
    modalidad: str,
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(
        select(Curso).where(
            Curso.carreid == carreid,
            Curso.plan == plan,
            Curso.ciclo == ciclo,
            Curso.modalidad == modalidad,
            Curso.estado == True
        )
    )
    return result.scalars().all()


@router.get("/{curso_id}", response_model=CursoResponse)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    result = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso = result.scalar_one_or_none()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


@router.post("/", response_model=CursoResponse)
async def create_curso(curso: CursoCreate, db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    db_curso = Curso(**curso.dict())
    db.add(db_curso)
    await db.commit()
    await db.refresh(db_curso)
    return db_curso


@router.put("/{curso_id}", response_model=CursoResponse)
async def update_curso(curso_id: int, curso_data: CursoUpdate, db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    result = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso = result.scalar_one_or_none()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    for field, value in curso_data.dict().items():
        setattr(curso, field, value)
    await db.commit()
    await db.refresh(curso)
    return curso


@router.patch("/{curso_id}/cambiar-estado", response_model=CursoResponse)
async def toggle_estado(curso_id: int, db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    result = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso = result.scalar_one_or_none()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso.estado = not curso.estado
    await db.commit()
    await db.refresh(curso)
    return curso


@router.patch("/{curso_id}/actualizar-horas/{horas}", response_model=CursoResponse)
async def actualizar_horas(curso_id: int, horas: int, db: AsyncSession = Depends(get_async_db), user: dict = Depends(get_current_user)):
    result = await db.execute(select(Curso).where(Curso.id == curso_id))
    curso = result.scalar_one_or_none()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso.horas = horas
    await db.commit()
    await db.refresh(curso)
    return curso


@router.post("/bulk", response_model=List[CursoResponse])
async def create_cursos_bulk(cursos: List[CursoCreate], db: AsyncSession = Depends(get_async_db)):
    db_cursos = [Curso(**curso.dict()) for curso in cursos]
    db.add_all(db_cursos)
    await db.commit()
    for curso in db_cursos:
        await db.refresh(curso)
    return db_cursos
