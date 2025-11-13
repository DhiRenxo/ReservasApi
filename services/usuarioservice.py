from sqlalchemy.future import select
from fastapi import HTTPException
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioDocenteCodigoUpdate
from datetime import datetime

ROL_DOCENTE = 7


async def get_all(db):
    result = await db.execute(select(Usuario))
    return result.scalars().all()


async def get_by_id(db, id: int):
    result = await db.execute(select(Usuario).filter(Usuario.id == id))
    return result.scalar_one_or_none()


async def create(db, data: UsuarioCreate):

    # ✅ Evitar correos duplicados
    existing = await db.execute(select(Usuario).filter(Usuario.correo == data.correo))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="El correo ya está en uso")

    nuevo = Usuario(**data.dict())
    nuevo.fechacreacion = datetime.utcnow()

    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo


async def update(db, id: int, data: UsuarioUpdate):
    usuario = await get_by_id(db, id)
    if usuario:
        for k, v in data.dict(exclude_unset=True).items():
            setattr(usuario, k, v)
        usuario.fechaactualizacion = datetime.utcnow()
        await db.commit()
        await db.refresh(usuario)
    return usuario


async def delete(db, id: int):
    usuario = await get_by_id(db, id)
    if usuario:
        await db.delete(usuario)
        await db.commit()
    return usuario


async def actualizar_cod_docente_service(db, usuario_id: int, datos: UsuarioDocenteCodigoUpdate):
    usuario = await get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.rolid != ROL_DOCENTE:
        raise HTTPException(status_code=403, detail="Solo docentes pueden tener código docente")

    if datos.cod_docente:
        usuario.cod_docente = datos.cod_docente
        usuario.fechaactualizacion = datetime.utcnow()

    await db.commit()
    await db.refresh(usuario)
    return usuario
