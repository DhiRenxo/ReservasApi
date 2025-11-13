from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import BaseSync
from models.carrera import Carrera

class Curso(BaseSync):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique = True)
    modalidad = Column(String(30))
    nombre = Column(String(500))
    horas = Column(Integer)
    ciclo = Column(String(50))
    plan = Column(String(10))
    carreid = Column(Integer, ForeignKey("carrera.id"))
    estado = Column(Boolean, default=True)
    horasasignadas = Column(Integer, nullable=True)

    carrera = relationship("Carrera")

    asignaciones_curso_docente = relationship(
        "AsignacionCursoDocente",
        back_populates="curso"
    ) 
    
