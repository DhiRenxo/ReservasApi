from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import BaseSync
from datetime import datetime
from models.asignacionseccion import asignacion_seccion

# ------------------------
# ASIGNACION
# ------------------------
class Asignacion(BaseSync):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    carreraid = Column(Integer)
    plan = Column(String(10), nullable=False)
    ciclo = Column(String(10), nullable=False)
    modalidad = Column(String(20))
    cantidad_secciones = Column(Integer)
    seccion_asignada = Column(Boolean, default= False)
    nombreseccion = Column(String(10), nullable=True)
    estado = Column(Boolean, default=True)
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificada = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_inicio = Column(DateTime)

    asignaciones_curso_docente = relationship(
        "AsignacionCursoDocente",
        back_populates="asignacion"
    )

    secciones = relationship(
        "Seccion",
        secondary=asignacion_seccion,
        back_populates="asignaciones"
    )
