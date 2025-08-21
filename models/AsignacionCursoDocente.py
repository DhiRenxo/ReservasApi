from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
# ------------------------
# TABLA INTERMEDIA: Asignación + Curso + Docente
# ------------------------
class AsignacionCursoDocente(Base):
    __tablename__ = "asignacion_curso_docente"

    id = Column(Integer, primary_key=True, index=True)
    asignacion_id = Column(Integer, ForeignKey("asignaciones.id"))
    curso_id = Column(Integer, ForeignKey("cursos.id"))
    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=True)

    asignacion = relationship("Asignacion", back_populates="asignaciones_curso_docente")
    curso = relationship("Curso", back_populates="asignaciones_curso_docente")
    docente = relationship("Docente", back_populates="asignaciones_curso_docente")