from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, or_

from models.docente import Docente
from models.cursos import Curso
from models.asignacion import Asignacion
from models.carrera import Carrera
from models.AsignacionCursoDocente import AsignacionCursoDocente

from schemas.asignacion import (
    AsignacionCreate,
    AsignacionUpdate,
    AsignacionUpdateSecciones,
    AsignacionCursoDocenteCreate,
    CursosAsignadosDocenteResponse
)


# ------------------------------
# CRUD Asignación
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

    await db.delete(db_asignacion)
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
    asignacion = await get_asignacion(db, asignacion_id)
    if not asignacion:
        return None
    asignacion.estado = estado
    await db.commit()
    await db.refresh(asignacion)
    return asignacion


async def actualizar_cursos_asignacion(db: AsyncSession, asignacion_id: int, curso_ids: List[int]):
    asignacion = await get_asignacion(db, asignacion_id)
    if not asignacion:
        return []

    cantidad_secciones = asignacion.cantidad_secciones or 1
    curso_ids = list(set(curso_ids))

    if curso_ids:
        delete_stmt = delete(AsignacionCursoDocente).where(
            AsignacionCursoDocente.asignacion_id == asignacion_id,
        ).where(
            or_(
                AsignacionCursoDocente.curso_id.notin_(curso_ids),
                AsignacionCursoDocente.seccion > cantidad_secciones
            )
        )
    else:
        delete_stmt = delete(AsignacionCursoDocente).where(
            AsignacionCursoDocente.asignacion_id == asignacion_id,
        )

    await db.execute(delete_stmt)
    await db.flush()

    result = await db.execute(
        select(AsignacionCursoDocente).filter(AsignacionCursoDocente.asignacion_id == asignacion_id)
    )
    existentes = {(r.curso_id, r.seccion) for r in result.scalars().all()}

    for curso_id in curso_ids:
        for seccion in range(1, cantidad_secciones + 1):
            if (curso_id, seccion) not in existentes:
                db.add(
                    AsignacionCursoDocente(
                        asignacion_id=asignacion_id,
                        curso_id=curso_id,
                        seccion=seccion,
                        docente_id=None
                    )
                )

    await db.commit()

    result_final = await db.execute(
        select(AsignacionCursoDocente).filter(AsignacionCursoDocente.asignacion_id == asignacion_id)
    )
    return result_final.scalars().all()


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
    delete_stmt = delete(AsignacionCursoDocente).where(
        AsignacionCursoDocente.asignacion_id == asignacion_id,
        AsignacionCursoDocente.seccion == seccion
    )

    result = await db.execute(delete_stmt)
    await db.commit()

    return {"asignacion_id": asignacion_id, "seccion": seccion, "eliminados": result.rowcount}


# ------------------------------
# Horas y bloques
# ------------------------------
async def recalcular_horas_docente(db: AsyncSession, docente_id: int):
    result = await db.execute(select(Docente).filter(Docente.id == docente_id))
    docente = result.scalar_one_or_none()
    if not docente:
        return None

    result = await db.execute(
        select(AsignacionCursoDocente).filter(AsignacionCursoDocente.docente_id == docente_id)
    )
    relaciones = result.scalars().all()

    horas_temporales = 0
    for rel in relaciones:
        curso_res = await db.execute(select(Curso).filter(Curso.id == rel.curso_id))
        curso = curso_res.scalar_one_or_none()
        asign_res = await db.execute(select(Asignacion).filter(Asignacion.id == rel.asignacion_id))
        asignacion = asign_res.scalar_one_or_none()

        if not curso or not asignacion:
            continue

        horas_curso = 0

        if getattr(rel, "es_bloque", False) and getattr(rel, "bloque", None) in ["A", "B"]:
            if getattr(rel, "activo", False):
                horas_curso = getattr(curso, "horas", 0) or 0
                if getattr(rel, "duplica_horas", False) and asignacion.modalidad and asignacion.modalidad.upper() == "PRESENCIAL":
                    horas_curso *= 2
        else:
            horas_curso = getattr(curso, "horas", 0) or 0

        horas_temporales += horas_curso

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
        result = await db.execute(
            select(AsignacionCursoDocente).filter(
                AsignacionCursoDocente.asignacion_id == relacion.asignacion_id,
                AsignacionCursoDocente.curso_id == relacion.curso_id,
                AsignacionCursoDocente.es_bloque == True,
                AsignacionCursoDocente.id != relacion_id
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


async def obtener_cursos_por_correo(db: AsyncSession, correo: str):
    result_docente = await db.execute(select(Docente).filter(Docente.correo == correo))
    docente = result_docente.scalar_one_or_none()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    result_rel = await db.execute(
        select(AsignacionCursoDocente)
        .join(Asignacion)
        .filter(
            AsignacionCursoDocente.docente_id == docente.id,
            Asignacion.estado == True
        )
    )
    relaciones = result_rel.scalars().all()

    response = []
    for rel in relaciones:
        curso_res = await db.execute(select(Curso).filter(Curso.id == rel.curso_id))
        curso = curso_res.scalar_one_or_none()
        asign_res = await db.execute(select(Asignacion).filter(Asignacion.id == rel.asignacion_id))
        asign = asign_res.scalar_one_or_none()

        if not curso or not asign:
            continue

        carrera_res = await db.execute(select(Carrera).filter(Carrera.id == asign.carreraid))
        carrera = carrera_res.scalar_one_or_none()

        response.append(
            CursosAsignadosDocenteResponse(
                docente_id=docente.id,
                asignacion_id=asign.id,
                carreraid=asign.carreraid,
                carrera_nombre=carrera.nombre if carrera else None,
                plan=asign.plan,
                ciclo=asign.ciclo,
                modalidad=asign.modalidad,
                curso_id=curso.id,
                curso_nombre=curso.nombre,
                seccion=rel.seccion,
                estado=asign.estado,
                docente_nombre=docente.nombre,
                es_bloque=rel.es_bloque,
                bloque=rel.bloque,
                activo=rel.activo
            )
        )

    return response
