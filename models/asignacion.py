from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# ------------------------
# ASIGNACION
# ------------------------
class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    carreraid = Column(Integer)
    plan = Column(String, nullable=False)
    ciclo = Column(String, nullable=False)
    modalidad = Column(String(20))
    cantidad_secciones = Column(Integer)
    secciones_asignadas = Column(Integer)
    estado = Column(Boolean, default=True)
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificada = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_inicio = Column(DateTime)

    asignaciones_curso_docente = relationship(
        "AsignacionCursoDocente",
        back_populates="asignacion"
    )
