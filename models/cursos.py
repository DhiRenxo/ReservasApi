from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from models.carrera import Carrera
from models.asignacion import asignacion_curso

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique = True)
    nombre = Column(String(50))
    horas = Column(Integer)
    ciclo = Column(String(50))
    plan = Column(String(10))
    carreid = Column(Integer, ForeignKey("carrera.id"))
    estado = Column(Boolean, default=True)
    horasasignadas = Column(Integer, nullable=True)

    carrera = relationship("Carrera")

    asignaciones = relationship("AsignacionDocenteTemporal", secondary=asignacion_curso, back_populates="cursos")
    
