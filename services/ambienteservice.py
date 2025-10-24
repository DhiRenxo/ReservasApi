from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from models.ambiente import Ambiente
from models.tipoambiente import TipoAmbiente
from schemas.ambiente import AmbienteCreate, AmbienteUpdate


async def get_all(db: AsyncSession):
    result = await db.execute(
        select(Ambiente).options(selectinload(Ambiente.tipo_ambiente))
    )
    return result.scalars().all()


async def get_by_id(db: AsyncSession, id: int):
    result = await db.execute(
        select(Ambiente)
        .options(selectinload(Ambiente.tipo_ambiente))
        .filter(Ambiente.id == id)
    )
    return result.scalars().first()


async def create(db: AsyncSession, data: AmbienteCreate):
    # Validar código único
    existe = await db.execute(
        select(Ambiente).filter(Ambiente.codigo == data.codigo)
    )
    if existe.scalars().first():
        raise HTTPException(status_code=400, detail="El código ya existe")

    # Validar tipo
    tipo = await db.execute(
        select(TipoAmbiente).filter(TipoAmbiente.id == data.tipoid)
    )
    if not tipo.scalars().first():
        raise HTTPException(status_code=404, detail="Tipo de ambiente no válido")

    nuevo = Ambiente(**data.dict())
    db.add(nuevo)

    await db.commit()
    await db.refresh(nuevo)
    return nuevo


async def update(db: AsyncSession, id: int, data: AmbienteUpdate):
    ambiente = await get_by_id(db, id)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")

    # Validar código único si cambió
    if data.codigo != ambiente.codigo:
        existe = await db.execute(
            select(Ambiente).filter(Ambiente.codigo == data.codigo)
        )
        if existe.scalars().first():
            raise HTTPException(status_code=400, detail="El código ya existe")

    # Validar tipo
    tipo = await db.execute(
        select(TipoAmbiente).filter(TipoAmbiente.id == data.tipoid)
    )
    if not tipo.scalars().first():
        raise HTTPException(status_code=404, detail="Tipo de ambiente no válido")

    for key, value in data.dict().items():
        setattr(ambiente, key, value)

    await db.commit()
    await db.refresh(ambiente)
    return ambiente


async def delete(db: AsyncSession, id: int):
    ambiente = await get_by_id(db, id)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")

    await db.delete(ambiente)
    await db.commit()
    return ambiente


async def actualizar_estado_ambiente(db: AsyncSession, id: int, nuevo_estado: bool):
    result = await db.execute(
        select(Ambiente).filter(Ambiente.id == id)
    )
    db_ambiente = result.scalars().first()

    if not db_ambiente:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")

    db_ambiente.activo = nuevo_estado
    await db.commit()
    await db.refresh(db_ambiente)
    return {"estado": db_ambiente.activo}
