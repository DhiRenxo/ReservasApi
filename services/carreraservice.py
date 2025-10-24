from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.carrera import Carrera
from schemas.carrera import CarreraCreate, CarreraUpdate
from typing import List, Optional


# ------------------------------
# CRUD Carrera (async)
# ------------------------------

async def get_all(db: AsyncSession) -> List[Carrera]:
    result = await db.execute(select(Carrera))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, carrera_id: int) -> Optional[Carrera]:
    result = await db.execute(select(Carrera).filter(Carrera.id == carrera_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, carrera: CarreraCreate) -> Carrera:
    db_carrera = Carrera(**carrera.dict())
    db.add(db_carrera)
    await db.commit()
    await db.refresh(db_carrera)
    return db_carrera


async def update(db: AsyncSession, carrera_id: int, carrera_update: CarreraUpdate) -> Optional[Carrera]:
    db_carrera = await get_by_id(db, carrera_id)
    if not db_carrera:
        return None

    for key, value in carrera_update.dict(exclude_unset=True).items():
        setattr(db_carrera, key, value)

    await db.commit()
    await db.refresh(db_carrera)
    return db_carrera


async def delete(db: AsyncSession, carrera_id: int) -> Optional[Carrera]:
    db_carrera = await get_by_id(db, carrera_id)
    if not db_carrera:
        return None

    db.delete(db_carrera)
    await db.commit()
    return db_carrera
