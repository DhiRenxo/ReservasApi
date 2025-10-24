from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.docente import Docente
from models.cursos import Curso
from models.asignacion import Asignacion
from models.AsignacionCursoDocente import AsignacionCursoDocente
from schemas.asignacion import (
    AsignacionCreate,
    AsignacionUpdate,
    AsignacionUpdateSecciones,
    AsignacionCursoDocenteCreate
)


# ------------------------------
# CRUD Asignacion (async)
# ------------------------------
async def create_asignacion(db: AsyncSession, asignacion: AsignacionCreate):
    db_asignacion = Asignacion(
        carreraid=asignacion.carreraid,
        plan=asignacion.plan,
        ciclo=asignacion.ciclo,
        modalidad=asignacion.modalidad,
        cantidad_secciones=asignacion.cantidad_secciones,
        seccion_asignada=asignacion.seccion_asignada,
        estado=asignacion.estado,
        fecha_inicio=asignacion.fecha_inicio,
        fecha_asignacion=datetime.utcnow()
    )
    db.add(db_asignacion)
    await db.commit()
    await db.refresh(db_asignacion)
    return db_asignacion


async def get_asignaciones(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Asignacion]:
    result = await db.execute(
        select(Asignacion).order_by(Asignacion.id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_asignacion(db: AsyncSession, asignacion_id: int) -> Optional[Asignacion]:
    result = await db.execute(
        select(Asignacion).filter(Asignacion.id == asignacion_id)
    )
    return result.scalar_one_or_none()


async def update_asignacion(db: AsyncSession, asignacion_id: int, asignacion: AsignacionUpdate):
    db_asignacion = await get_asignacion(db, asignacion_id)
    if not db_asignacion:
        return None

    for field, value in asignacion.dict(exclude_unset=True).items():
        setattr(db_asignacion, field, value)

    db_asignacion.fecha_modificada = datetime.utcnow()
    await db.commit()
    await db.refresh(db_asignacion)
    return db_asignacion


async def update_asignacion_secciones(db: AsyncSession, asignacion_id: int, update: AsignacionUpdateSecciones):
    db_asignacion = await get_asignacion(db, asignacion_id)
    if not db_asignacion:
        return None

    db_asignacion.cantidad_secciones = update.cantidad_secciones
    db_asignacion.fecha_modificada = datetime.utcnow()

    await db.commit()
    await db.refresh(db_asignacion)
    return db_asignacion


async def delete_asignacion(db: AsyncSession, asignacion_id: int):
    db_asignacion = await get_asignacion(db, asignacion_id)
    if not db_asignacion:
        return None
    db.delete(db_asignacion)
    await db.commit()
    return db_asignacion


# ------------------------------
# Relaciones AsignacionCursoDocente
# ------------------------------
async def add_asignacion_curso_docente(db: AsyncSession, relacion: AsignacionCursoDocenteCreate):
    db_relacion = AsignacionCursoDocente(
        asignacion_id=relacion.asignacion_id,
        curso_id=relacion.curso_id,
        docente_id=relacion.docente_id
    )
    db.add(db_relacion)
    await db.commit()
    await db.refresh(db_relacion)
    return db_relacion


async def get_asignacion_curso_docentes(db: AsyncSession, asignacion_id: int) -> List[AsignacionCursoDocente]:
    result = await db.execute(
        select(AsignacionCursoDocente).filter(AsignacionCursoDocente.asignacion_id == asignacion_id)
    )
    return result.scalars().all()


async def update_asignacion_estado(db: AsyncSession, asignacion_id: int, estado: bool):
    result = await db.execute(select(Asignacion).filter(Asignacion.id == asignacion_id))
    asignacion = result.scalar_one_or_none()
    if not asignacion:
        return None
    asignacion.estado = estado
    await db.commit()
    await db.refresh(asignacion)
    return asignacion


async def actualizar_cursos_asignacion(db: AsyncSession, asignacion_id: int, curso_ids: List[int]) -> List[AsignacionCursoDocente]:
    asignacion = await get_asignacion(db, asignacion_id)
    if not asignacion:
        return []

    cantidad_secciones = asignacion.cantidad_secciones or 1
    curso_ids = list(set(curso_ids))

    # obtener relaciones existentes
    result = await db.execute(
        select(AsignacionCursoDocente).filter(AsignacionCursoDocente.asignacion_id == asignacion_id)
    )
    relaciones_existentes = result.scalars().all()

    existentes = {(r.curso_id, r.seccion) for r in relaciones_existentes}
    secciones_presentes = {r.seccion for r in relaciones_existentes}
    secciones_a_crear = [s for s in range(1, cantidad_secciones + 1) if s not in secciones_presentes]

    for curso_id in curso_ids:
        for seccion in secciones_a_crear:
            clave = (curso_id, seccion)
            if clave in existentes:
                continue
            db_relacion = AsignacionCursoDocente(
                asignacion_id=asignacion_id,
                curso_id=curso_id,
                seccion=seccion,
                docente_id=None
            )
            db.add(db_relacion)
            existentes.add(clave)

    await db.commit()

    result = await db.execute(
        select(AsignacionCursoDocente).filter(AsignacionCursoDocente.asignacion_id == asignacion_id)
    )
    return result.scalars().all()


async def update_docente_curso_asignacion(db: AsyncSession, asignacion_id: int, curso_id: int, seccion: int, docente_id: int):
    result = await db.execute(
        select(AsignacionCursoDocente).filter(
            AsignacionCursoDocente.asignacion_id == asignacion_id,
            AsignacionCursoDocente.curso_id == curso_id,
            AsignacionCursoDocente.seccion == seccion
        )
    )
    relacion = result.scalar_one_or_none()

    if not relacion:
        return None

    relacion.docente_id = docente_id
    await db.commit()
    await db.refresh(relacion)
    return relacion


async def delete_seccion_asignacion(db: AsyncSession, asignacion_id: int, seccion: int):
    result = await db.execute(
        select(AsignacionCursoDocente).filter(
            AsignacionCursoDocente.asignacion_id == asignacion_id,
            AsignacionCursoDocente.seccion == seccion
        )
    )
    relaciones = result.scalars().all()

    if not relaciones:
        return None

    for r in relaciones:
        db.delete(r)

    await db.commit()
    return {"asignacion_id": asignacion_id, "seccion": seccion, "eliminados": len(relaciones)}


# ------------------------------
# Horas y bloques
# ------------------------------
async def recalcular_horas_docente(db: AsyncSession, docente_id: int):
    # Obtener docente
    result = await db.execute(select(Docente).filter(Docente.id == docente_id))
    docente = result.scalar_one_or_none()
    if not docente:
        return None

    # obtener relaciones del docente
    result = await db.execute(
        select(AsignacionCursoDocente).filter(AsignacionCursoDocente.docente_id == docente_id)
    )
    relaciones = result.scalars().all()

    horas_temporales = 0

    for rel in relaciones:
        # obtener curso y asignacion correspondientes
        curso_res = await db.execute(select(Curso).filter(Curso.id == rel.curso_id))
        curso = curso_res.scalar_one_or_none()

        asign_res = await db.execute(select(Asignacion).filter(Asignacion.id == rel.asignacion_id))
        asignacion = asign_res.scalar_one_or_none()

        if not curso or not asignacion:
            continue

        horas_curso = 0

        # Si es bloque: solo suma si está activo
        if getattr(rel, "es_bloque", False) and getattr(rel, "bloque", None) in ["A", "B"]:
            if getattr(rel, "activo", False):
                horas_curso = getattr(curso, "horas", 0) or 0
                if getattr(rel, "duplica_horas", False) and asignacion.modalidad and asignacion.modalidad.upper() == "PRESENCIAL":
                    horas_curso *= 2
        else:
            horas_curso = getattr(curso, "horas", 0) or 0

        horas_temporales += horas_curso

    # actualizar docente
    horas_reales = (getattr(docente, "horasactual", 0) or 0) - (getattr(docente, "horastemporales", 0) or 0)
    docente.horastemporales = horas_temporales
    docente.horasactual = horas_reales + horas_temporales

    await db.commit()
    await db.refresh(docente)
    return docente


async def activar_bloque(db: AsyncSession, relacion_id: int):
    result = await db.execute(
        select(AsignacionCursoDocente).filter(AsignacionCursoDocente.id == relacion_id)
    )
    relacion = result.scalar_one_or_none()
    if not relacion:
        return None

    if getattr(relacion, "es_bloque", False):
        # desactivar otros bloques del mismo curso/asignacion
        result = await db.execute(
            select(AsignacionCursoDocente).filter(
                AsignacionCursoDocente.asignacion_id == relacion.asignacion_id,
                AsignacionCursoDocente.curso_id == relacion.curso_id,
                AsignacionCursoDocente.es_bloque == True,
                AsignacionCursoDocente.id != relacion.id
            )
        )
        otros = result.scalars().all()
        for o in otros:
            o.activo = False

        relacion.activo = True

    if relacion.docente_id:
        await recalcular_horas_docente(db, relacion.docente_id)

    await db.commit()
    await db.refresh(relacion)

    return relacion



async def actualizar_comentario_disponibilidad(db: AsyncSession, relacion_id: int, data):
    result = await db.execute(
        select(AsignacionCursoDocente).filter(AsignacionCursoDocente.id == relacion_id)
    )
    relacion = result.scalar_one_or_none()
    if not relacion:
        return None

    if hasattr(data, "comentario") and data.comentario is not None:
        relacion.comentario = data.comentario

    if hasattr(data, "disponibilidad") and data.disponibilidad is not None:
        relacion.disponibilidad = data.disponibilidad

    await db.commit()
    await db.refresh(relacion)
    return relacion
