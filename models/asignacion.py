from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# Tablas intermedias
asignacion_curso = Table(
    'asignacion_curso', Base.metadata,
    Column('asignacion_id', ForeignKey('asignaciones.id'), primary_key=True),
    Column('curso_id', ForeignKey('cursos.id'), primary_key=True)
)

asignacion_docente = Table(
    'asignacion_docente', Base.metadata,
    Column('asignacion_id', ForeignKey('asignaciones.id'), primary_key=True),
    Column('docente_id', ForeignKey('docentes.id'), primary_key=True)
)

class AsignacionDocenteTemporal(Base):
    __tablename__ = 'asignaciones'

    id = Column(Integer, primary_key=True, index=True)
    carreraid = Column(Integer)
    plan = Column(String)
    ciclo = Column(String)
    cantidad_secciones = Column(Integer)
    secciones_asignadas = Column(Integer)
    estado = Column(Boolean, default=True)
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificada = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cursos = relationship("Curso", secondary=asignacion_curso, back_populates="asignaciones")
    docentes = relationship("Docente", secondary=asignacion_docente, back_populates="asignaciones")
