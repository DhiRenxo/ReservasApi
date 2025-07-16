from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class AsignacionDocenteTemporal(Base):
    __tablename__ = "asignacion"

    id = Column(Integer, primary_key=True, index=True)
    
    docenteid = Column(Integer, ForeignKey("docentes.id"), nullable=False)
    cursoid = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    carreraid = Column(Integer, ForeignKey("carrera.id"), nullable=False)
    ciclo = Column(String(10), nullable=False)  
    cantidad_secciones = Column(Integer, nullable=False)
    secciones_asignadas = Column(Integer, nullable=False)
    horas_curso = Column(Integer, nullable=False)
    horas_actuales = Column(Integer, nullable=False) 
    horas_dejara = Column(Integer, nullable=True)     
    horas_totales = Column(Integer, nullable=True)  
    observaciones = Column(String, nullable=True)
    fecha_asignacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificada = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


    docente = relationship("Docente")
    cursos = relationship("Curso")
    carrera = relationship("Carrera")
