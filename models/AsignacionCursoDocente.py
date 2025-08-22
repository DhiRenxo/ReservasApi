from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class AsignacionCursoDocente(Base):
    __tablename__ = "asignacion_curso_docente"

    id = Column(Integer, primary_key=True, index=True)
    asignacion_id = Column(Integer, ForeignKey("asignaciones.id"))
    curso_id = Column(Integer, ForeignKey("cursos.id"))
    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=True)
    seccion = Column(Integer, default=1)
    es_bloque = Column(Boolean, default=False)       
    bloque = Column(String(1), nullable=True)        
    duplica_horas = Column(Boolean, default=False)   
    comentario = Column(Text, nullable=True)         
    disponibilidad = Column(String(50), nullable=True)  

    asignacion = relationship("Asignacion", back_populates="asignaciones_curso_docente")
    curso = relationship("Curso", back_populates="asignaciones_curso_docente")
    docente = relationship("Docente", back_populates="asignaciones_curso_docente")
