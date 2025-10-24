from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.seccion import Seccion
from schemas.seccion import SeccionCreate, SeccionUpdate
from datetime import date

# Crear nueva sección
async def crear_seccion(db: AsyncSession, seccion: SeccionCreate):
    nueva = Seccion(**seccion.dict())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

# Obtener todas las secciones
async def obtener_secciones(db: AsyncSession):
    result = await db.execute(select(Seccion))
    return result.scalars().all()

# Obtener sección por ID
async def obtener_seccion_por_id(db: AsyncSession, id: int):
    result = await db.execute(select(Seccion).filter(Seccion.id == id))
    return result.scalar_one_or_none()

# Actualizar sección
async def actualizar_seccion(db: AsyncSession, id: int, seccion_update: SeccionUpdate):
    db_seccion = await obtener_seccion_por_id(db, id)
    if db_seccion:
        for attr, value in seccion_update.dict(exclude_unset=True).items():
            setattr(db_seccion, attr, value)
        await db.commit()
        await db.refresh(db_seccion)
    return db_seccion

# Eliminar sección
async def eliminar_seccion(db: AsyncSession, id: int):
    db_seccion = await obtener_seccion_por_id(db, id)
    if db_seccion:
        await db.delete(db_seccion)
        await db.commit()
    return db_seccion

# Servicio 1: Actualizar solo estado y poner fecha_fin si se desactiva
async def actualizar_estado_seccion(db: AsyncSession, id: int, nuevo_estado: bool):
    db_seccion = await obtener_seccion_por_id(db, id)
    if not db_seccion:
        return None

    db_seccion.estado = nuevo_estado
    if not nuevo_estado:
        db_seccion.fecha_fin = date.today()
    await db.commit()
    await db.refresh(db_seccion)
    return db_seccion

# Servicio 2: Si se activa una sección ya terminada, crear una nueva
async def reactivar_seccion_creando_nueva(db: AsyncSession, id: int, nuevo_inicio: date, nuevo_fin: date):
    seccion_original = await obtener_seccion_por_id(db, id)
    if not seccion_original:
        return None

    if seccion_original.estado:  # Ya está activa
        return seccion_original

    # Crear nueva sección con fechas nuevas
    nueva_seccion = Seccion(
        nombre=seccion_original.nombre,
        carreraid=seccion_original.carreraid,
        ciclo=seccion_original.ciclo,
        letra=seccion_original.letra,
        turno=seccion_original.turno,
        serie=seccion_original.serie,
        fecha_creacion=date.today(),
        fecha_inicio=nuevo_inicio,
        fecha_fin=nuevo_fin,
        estado=True
    )
    db.add(nueva_seccion)
    await db.commit()
    await db.refresh(nueva_seccion)
    return nueva_seccion
