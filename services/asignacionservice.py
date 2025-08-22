# services/asignacion.py
from sqlalchemy.orm import Session
from datetime import datetime
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

# -----------------------------
# CRUD Asignacion
# -----------------------------

def create_asignacion(db: Session, asignacion: AsignacionCreate):
    db_asignacion = Asignacion(
        carreraid=asignacion.carreraid,
        plan=asignacion.plan,
        ciclo=asignacion.ciclo,
        modalidad=asignacion.modalidad,
        cantidad_secciones=asignacion.cantidad_secciones,
        secciones_asignadas=asignacion.secciones_asignadas,
        estado=asignacion.estado,
        fecha_inicio=asignacion.fecha_inicio,
        fecha_asignacion=datetime.utcnow()
    )
    db.add(db_asignacion)
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion


def get_asignaciones(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Asignacion)
        .order_by(Asignacion.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_asignacion(db: Session, asignacion_id: int):
    return db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()


def update_asignacion(db: Session, asignacion_id: int, asignacion: AsignacionUpdate):
    db_asignacion = get_asignacion(db, asignacion_id)
    if not db_asignacion:
        return None

    for field, value in asignacion.dict(exclude_unset=True).items():
        setattr(db_asignacion, field, value)

    db_asignacion.fecha_modificada = datetime.utcnow()
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion


def update_asignacion_secciones(db: Session, asignacion_id: int, update: AsignacionUpdateSecciones):
    db_asignacion = get_asignacion(db, asignacion_id)
    if not db_asignacion:
        return None

    db_asignacion.cantidad_secciones = update.cantidad_secciones
    db_asignacion.fecha_modificada = datetime.utcnow()

    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion


def delete_asignacion(db: Session, asignacion_id: int):
    db_asignacion = get_asignacion(db, asignacion_id)
    if not db_asignacion:
        return None
    db.delete(db_asignacion)
    db.commit()
    return db_asignacion


# -----------------------------
# Relación Asignacion - Curso - Docente
# -----------------------------

def add_asignacion_curso_docente(db: Session, relacion: AsignacionCursoDocenteCreate):
    db_relacion = AsignacionCursoDocente(
        asignacion_id=relacion.asignacion_id,
        curso_id=relacion.curso_id,
        docente_id=relacion.docente_id
    )
    db.add(db_relacion)
    db.commit()
    db.refresh(db_relacion)
    return db_relacion


def get_asignacion_curso_docentes(db: Session, asignacion_id: int):
    return db.query(AsignacionCursoDocente).filter(
        AsignacionCursoDocente.asignacion_id == asignacion_id
    ).all()


def update_asignacion_estado(db: Session, asignacion_id: int, estado: bool):
    asignacion = db.query(Asignacion).filter(Asignacion.id == asignacion_id).first()
    if not asignacion:
        return None
    asignacion.estado = estado
    db.commit()
    db.refresh(asignacion)
    return asignacion

def actualizar_cursos_asignacion(db: Session, asignacion_id: int, curso_ids: list[int]):
    asignacion = get_asignacion(db, asignacion_id)
    if not asignacion:
        return []

    cantidad_secciones = asignacion.cantidad_secciones or 1

    # 🔹 Deduplicar curso_ids que llegan del front
    curso_ids = list(set(curso_ids))

    # Relaciones existentes
    relaciones_existentes = db.query(AsignacionCursoDocente).filter(
        AsignacionCursoDocente.asignacion_id == asignacion_id
    ).all()

    # Set de (curso_id, seccion) ya presentes
    existentes = {(r.curso_id, r.seccion) for r in relaciones_existentes}

    # ¿Qué secciones faltan crear?
    secciones_presentes = {r.seccion for r in relaciones_existentes}
    secciones_a_crear = [s for s in range(1, cantidad_secciones + 1) if s not in secciones_presentes]

    # Crear sólo lo que falta y actualizar el set en caliente
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

    db.commit()

    return db.query(AsignacionCursoDocente).filter(
        AsignacionCursoDocente.asignacion_id == asignacion_id
    ).all()



def update_docente_curso_asignacion(db: Session, asignacion_id: int, curso_id: int, seccion: int, docente_id: int):
    relacion = db.query(AsignacionCursoDocente).filter(
        AsignacionCursoDocente.asignacion_id == asignacion_id,
        AsignacionCursoDocente.curso_id == curso_id,
        AsignacionCursoDocente.seccion == seccion
    ).first()
    
    if not relacion:
        return None
    
    relacion.docente_id = docente_id
    db.commit()
    db.refresh(relacion)
    return relacion

def delete_seccion_asignacion(db: Session, asignacion_id: int, seccion: int):
    relaciones = db.query(AsignacionCursoDocente).filter(
        AsignacionCursoDocente.asignacion_id == asignacion_id,
        AsignacionCursoDocente.seccion == seccion
    ).all()

    if not relaciones:
        return None

    for r in relaciones:
        db.delete(r)

    db.commit()
    return {"asignacion_id": asignacion_id, "seccion": seccion, "eliminados": len(relaciones)}

def recalcular_horas_docente(db: Session, docente_id: int):
    docente = db.query(Docente).filter(Docente.id == docente_id).first()
    if not docente:
        return None

    relaciones = (
        db.query(AsignacionCursoDocente)
        .filter(AsignacionCursoDocente.docente_id == docente_id)
        .all()
    )

    horas_temporales = 0
    for rel in relaciones:
        curso = db.query(Curso).filter(Curso.id == rel.curso_id).first()
        if not curso:
            continue

        horas_curso = curso.horas

        if rel.es_bloque and rel.duplica_horas and curso.modalidad.lower() == "presencial":
            horas_curso *= 2   

        horas_temporales += horas_curso

    horas_reales = (docente.horasactual or 0) - (docente.horastemporales or 0)

    docente.horastemporales = horas_temporales
    docente.horasactual = horas_reales + horas_temporales

    db.commit()
    db.refresh(docente)
    return docente
