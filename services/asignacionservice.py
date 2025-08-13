from sqlalchemy.orm import Session
from models.asignacion import AsignacionDocenteTemporal
from models.cursos import Curso
from models.docente import Docente
from schemas.asignacion import (
    AsignacionCreate,
    AsignacionUpdate,
    AsignacionEstadoUpdate,
    AsignacionDelete,
    AsignacionCantidadUpdate
)
from datetime import datetime


# Crear asignación
def crear_asignacion(db: Session, asignacion: AsignacionCreate):
    nueva_asignacion = AsignacionDocenteTemporal(
        carreraid=asignacion.carreraid,
        modalidad=asignacion.modalidad,
        plan=asignacion.plan,
        ciclo=asignacion.ciclo,
        cantidad_secciones=asignacion.cantidad_secciones,
        secciones_asignadas=asignacion.secciones_asignadas,
        fecha_inicio=asignacion.fecha_inicio,
        estado=asignacion.estado
    )

    cursos = db.query(Curso).filter(Curso.id.in_(asignacion.curso_ids)).all()
    nueva_asignacion.cursos = cursos

    if asignacion.docente_ids:
        docentes = db.query(Docente).filter(Docente.id.in_(asignacion.docente_ids)).all()
        nueva_asignacion.docentes = docentes

    db.add(nueva_asignacion)
    db.commit()
    db.refresh(nueva_asignacion)
    return nueva_asignacion


# Obtener todas las asignaciones
def obtener_asignaciones(db: Session):
    return db.query(AsignacionDocenteTemporal).all()

# Obtener por ID
def obtener_asignacion_por_id(db: Session, asignacion_id: int):
    return db.query(AsignacionDocenteTemporal).filter(AsignacionDocenteTemporal.id == asignacion_id).first()

# Actualizar asignación completa
def actualizar_asignacion(db: Session, asignacion_id: int, datos: AsignacionUpdate):
    asignacion = obtener_asignacion_por_id(db, asignacion_id)
    if not asignacion:
        return None

    asignacion.carreraid = datos.carreraid
    asignacion.plan = datos.plan
    asignacion.ciclo = datos.ciclo
    asignacion.cantidad_secciones = datos.cantidad_secciones
    asignacion.secciones_asignadas = datos.secciones_asignadas
    asignacion.estado = datos.estado

    # Actualizar cursos
    if datos.curso_ids:
        cursos = db.query(Curso).filter(Curso.id.in_(datos.curso_ids)).all()
        asignacion.cursos = cursos

    # Actualizar docentes si se pasan
    if datos.docente_ids is not None:
        docentes = db.query(Docente).filter(Docente.id.in_(datos.docente_ids)).all()
        asignacion.docentes = docentes

    db.commit()
    db.refresh(asignacion)
    return asignacion

# Cambiar solo el estado
def actualizar_estado_asignacion(db: Session, asignacion_id: int, estado_data: AsignacionEstadoUpdate):
    asignacion = obtener_asignacion_por_id(db, asignacion_id)
    if not asignacion:
        return None

    asignacion.estado = estado_data.estado
    db.commit()
    db.refresh(asignacion)
    return asignacion

# Eliminar (soft delete)
def eliminar_asignacion(db: Session, delete_data: AsignacionDelete):
    asignacion = obtener_asignacion_por_id(db, delete_data.id)
    if not asignacion:
        return None

    asignacion.estado = False
    db.commit()
    return asignacion

def actualizar_cantidad_secciones(db: Session, asignacion_id: int, data: AsignacionCantidadUpdate):
    asignacion = db.query(AsignacionDocenteTemporal).filter(AsignacionDocenteTemporal.id == asignacion_id).first()
    
    if not asignacion:
        return None  

    asignacion.cantidad_secciones = data.cantidad_secciones
    asignacion.fecha_modificada = datetime.utcnow()
    db.commit()
    db.refresh(asignacion)
    
    return asignacion