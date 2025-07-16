from sqlalchemy.orm import Session
from models.asignacion import AsignacionDocenteTemporal
from schemas.asignacion import AsignacionCreate, AsignacionUpdate
from datetime import date
from sqlalchemy import cast, Date

def crear_asignacion(db: Session, asignacion: AsignacionCreate):
    horas_totales = asignacion.horas_actuales + (asignacion.horas_curso * asignacion.secciones_asignadas)
    db_asignacion = AsignacionDocenteTemporal(
        **asignacion.dict(),
        horas_totales=horas_totales
    )
    db.add(db_asignacion)
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion


def obtener_asignaciones(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(AsignacionDocenteTemporal)
        .order_by(AsignacionDocenteTemporal.id)  # 👈 Importante: Añade un ORDER BY
        .offset(skip)
        .limit(limit)
        .all()
    )


def obtener_asignacion_por_id(db: Session, asignacion_id: int):
    return db.query(AsignacionDocenteTemporal).filter(AsignacionDocenteTemporal.id == asignacion_id).first()


def actualizar_asignacion(db: Session, asignacion_id: int, datos: AsignacionUpdate):
    asignacion = obtener_asignacion_por_id(db, asignacion_id)
    if not asignacion:
        return None

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(asignacion, campo, valor)

    if datos.horas_curso or datos.secciones_asignadas or datos.horas_actuales:
        asignacion.horas_totales = (
            datos.horas_actuales or asignacion.horas_actuales
        ) + ( (datos.horas_curso or asignacion.horas_curso) * (datos.secciones_asignadas or asignacion.secciones_asignadas) )

    db.commit()
    db.refresh(asignacion)
    return asignacion


def eliminar_asignacion(db: Session, asignacion_id: int):
    asignacion = obtener_asignacion_por_id(db, asignacion_id)
    if asignacion:
        db.delete(asignacion)
        db.commit()
    return asignacion

def obtener_asignaciones_por_fecha(db: Session, fecha: date):
    return (
        db.query(AsignacionDocenteTemporal)
        .filter(cast(AsignacionDocenteTemporal.fecha_asignacion, Date) == fecha)
        .order_by(AsignacionDocenteTemporal.id)
        .all()
    )