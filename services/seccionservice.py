from sqlalchemy.orm import Session
from models.seccion import Seccion
from schemas.seccion import SeccionCreate, SeccionUpdate
from datetime import date, timedelta

def crear_seccion(db: Session, seccion: SeccionCreate):
    nueva = Seccion(**seccion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def obtener_secciones(db: Session):
    return db.query(Seccion).all()

def obtener_seccion_por_id(db: Session, id: int):
    return db.query(Seccion).filter(Seccion.id == id).first()

def actualizar_seccion(db: Session, id: int, seccion_update: SeccionUpdate):
    db_seccion = db.query(Seccion).filter(Seccion.id == id).first()
    if db_seccion:
        for attr, value in seccion_update.dict(exclude_unset=True).items():
            setattr(db_seccion, attr, value)
        db.commit()
        db.refresh(db_seccion)
    return db_seccion

def eliminar_seccion(db: Session, id: int):
    db_seccion = db.query(Seccion).filter(Seccion.id == id).first()
    if db_seccion:
        db.delete(db_seccion)
        db.commit()
    return db_seccion

# Servicio 1: Actualizar solo estado y poner fecha_fin si se desactiva
def actualizar_estado_seccion(db: Session, id: int, nuevo_estado: bool):
    db_seccion = db.query(Seccion).filter(Seccion.id == id).first()
    if not db_seccion:
        return None

    db_seccion.estado = nuevo_estado
    if not nuevo_estado:
        db_seccion.fecha_fin = date.today()
    db.commit()
    db.refresh(db_seccion)
    return db_seccion

# Servicio 2: Si se activa una sección ya terminada, crear una nueva
def reactivar_seccion_creando_nueva(db: Session, id: int, nuevo_inicio: date, nuevo_fin: date):
    seccion_original = db.query(Seccion).filter(Seccion.id == id).first()
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
    db.commit()
    db.refresh(nueva_seccion)
    return nueva_seccion

