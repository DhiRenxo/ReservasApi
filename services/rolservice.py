from sqlalchemy.future import select
from fastapi import HTTPException
from models.rol import Rol
from schemas.rol import RolCreate, RolUpdate


async def get_all(db):
    result = await db.execute(select(Rol))
    return result.scalars().all()


async def get_by_id(db, id: int):
    result = await db.execute(
        select(Rol).filter(Rol.id == id)
    )
    return result.scalar_one_or_none()


async def create(db, data: RolCreate):
    # Verificar duplicado
    result = await db.execute(select(Rol).filter(Rol.nombre == data.nombre))
    existente = result.scalar_one_or_none()
    if existente:
        raise HTTPException(status_code=400, detail="El rol ya existe")

    nuevo = Rol(nombre=data.nombre)
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


async def update(db, id: int, data: RolUpdate):
    rol = await get_by_id(db, id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    rol.nombre = data.nombre
    await db.commit()
    await db.refresh(rol)
    return rol
