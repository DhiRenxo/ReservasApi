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


def create_asignacion(db: Session, asignacion: AsignacionCreate):
    db_asignacion = Asignacion(
        carreraid=asignacion.carreraid,
        plan=asignacion.plan,
        ciclo=asignacion.ciclo,
        modalidad=asignacion.modalidad,
        cantidad_secciones=asignacion.cantidad_secciones,
        seccion_asignada = asignacion.seccion_asignada,
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
    curso_ids = list(set(curso_ids))

    relaciones_existentes = db.query(AsignacionCursoDocente).filter(
        AsignacionCursoDocente.asignacion_id == asignacion_id
    ).all()

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
        asignacion = db.query(Asignacion).filter(Asignacion.id == rel.asignacion_id).first()
        if not curso or not asignacion:
            continue

        horas_curso = 0  

        # ✅ Si es bloque: solo suma si está activo
        if rel.es_bloque and rel.bloque in ["A", "B"]:
            if rel.activo:
                horas_curso = curso.horas
                if rel.duplica_horas and asignacion.modalidad and asignacion.modalidad.upper() == "PRESENCIAL":
                    horas_curso *= 2

        # ✅ Si no es bloque: suma siempre (sin importar activo)
        else:
            horas_curso = curso.horas

        horas_temporales += horas_curso

    # ✅ Actualizar horas del docente
    horas_reales = (docente.horasactual or 0) - (docente.horastemporales or 0)
    docente.horastemporales = horas_temporales
    docente.horasactual = horas_reales + horas_temporales

    db.commit()
    db.refresh(docente)
    return docente



def activar_bloque(db: Session, relacion_id: int):
    relacion = db.query(AsignacionCursoDocente).filter(
        AsignacionCursoDocente.id == relacion_id
    ).first()

    if not relacion:
        return None

    if relacion.es_bloque:
        db.query(AsignacionCursoDocente).filter(
            AsignacionCursoDocente.asignacion_id == relacion.asignacion_id,
            AsignacionCursoDocente.curso_id == relacion.curso_id,
            AsignacionCursoDocente.es_bloque == True,
            AsignacionCursoDocente.id != relacion.id
        ).update({AsignacionCursoDocente.activo: False})

        relacion.activo = True

    db.commit()
    db.refresh(relacion)

    if relacion.docente_id:
        recalcular_horas_docente(db, relacion.docente_id)

    return relacion


def actualizar_comentario_disponibilidad(db: Session, relacion_id: int, data):
    relacion = db.query(AsignacionCursoDocente).filter(AsignacionCursoDocente.id == relacion_id).first()
    if not relacion:
        return None

    if data.comentario is not None:
        relacion.comentario = data.comentario

    if data.disponibilidad is not None:
        relacion.disponibilidad = data.disponibilidad

    db.commit()
    db.refresh(relacion)
    return relacion
