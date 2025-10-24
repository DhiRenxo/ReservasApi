from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.cursos import Curso
from schemas.curso import CursoCreate, CursoUpdate
from typing import List, Optional


# ------------------------------
# CRUD Curso (async)
# ------------------------------

async def get_all(db: AsyncSession) -> List[Curso]:
    result = await db.execute(select(Curso))
    return result.scalars().all()


async def get_active(db: AsyncSession) -> List[Curso]:
    result = await db.execute(select(Curso).filter(Curso.estado == True))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, curso_id: int) -> Optional[Curso]:
    result = await db.execute(select(Curso).filter(Curso.id == curso_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, curso: CursoCreate) -> Curso:
    db_curso = Curso(**curso.dict())
    db.add(db_curso)
    await db.commit()
    await db.refresh(db_curso)
    return db_curso


async def update(db: AsyncSession, curso_id: int, curso_data: CursoUpdate) -> Optional[Curso]:
    curso = await get_by_id(db, curso_id)
    if curso:
        for field, value in curso_data.dict(exclude_unset=True).items():
            setattr(curso, field, value)
        await db.commit()
        await db.refresh(curso)
    return curso


async def toggle_estado(db: AsyncSession, curso_id: int) -> Optional[Curso]:
    curso = await get_by_id(db, curso_id)
    if curso:
        curso.estado = not curso.estado
        await db.commit()
        await db.refresh(curso)
    return curso


async def update_horas(db: AsyncSession, curso_id: int, horas: int) -> Optional[Curso]:
    curso = await get_by_id(db, curso_id)
    if curso:
        curso.horas = horas
        await db.commit()
        await db.refresh(curso)
    return curso


async def get_by_carrera_plan_ciclo(
    db: AsyncSession, carreid: int, plan: str, ciclo: str, modalidad: str
) -> List[Curso]:
    result = await db.execute(
        select(Curso).filter(
            Curso.carreid == carreid,
            Curso.plan == plan,
            Curso.ciclo == ciclo,
            Curso.modalidad == modalidad,
            Curso.estado == True
        )
    )
    return result.scalars().all()
