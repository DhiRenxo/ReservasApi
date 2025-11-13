from sqlalchemy.future import select
from fastapi import HTTPException
from models.docente import Docente
from models.usuario import Usuario
from schemas.docente import DocenteCreate, DocenteUpdate
from datetime import datetime

ROL_DOCENTE = 7
ROL_INVITADO = 1


async def listar_docentes(db):
    result = await db.execute(select(Docente).filter(Docente.estado == True))
    return result.scalars().all()


async def obtener_docente(db, docente_id: int):
    result = await db.execute(select(Docente).filter(Docente.id == docente_id))
    return result.scalar_one_or_none()


from fastapi.encoders import jsonable_encoder

async def crear_docente(db, data: DocenteCreate):
    # Verificar si ya existe docente con ese correo
    existente = await db.execute(select(Docente).filter(Docente.correo == data.correo))
    if existente.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="El docente ya está registrado")

    db_docente = Docente(**data.dict())
    db.add(db_docente)
    await db.commit()
    await db.refresh(db_docente)

    usuario_result = await db.execute(select(Usuario).filter(Usuario.correo == data.correo))
    usuario = usuario_result.scalar_one_or_none()

    if usuario and usuario.rolid != ROL_DOCENTE:
        usuario.rolid = ROL_DOCENTE
        usuario.fechaactualizacion = datetime.utcnow()
        await db.commit()
        await db.refresh(usuario)

    return db_docente


async def actualizar_docente(db, docente_id: int, data: DocenteUpdate):
    docente = await obtener_docente(db, docente_id)
    if docente:
        for k, v in data.dict(exclude_unset=True).items():
            setattr(docente, k, v)
        await db.commit()
        await db.refresh(docente)
    return docente


async def eliminar_docente(db, docente_id: int):
    docente = await obtener_docente(db, docente_id)
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    docente.estado = False
    await db.commit()
    await db.refresh(docente)

    # ✅ Al desactivar docente, bajar el rol del usuario
    usuario_result = await db.execute(select(Usuario).filter(Usuario.correo == docente.correo))
    usuario = usuario_result.scalar_one_or_none()

    if usuario and usuario.rolid == ROL_DOCENTE:
        usuario.rolid = ROL_INVITADO
        usuario.fechaactualizacion = datetime.utcnow()
        await db.commit()
        await db.refresh(usuario)

    return docente
