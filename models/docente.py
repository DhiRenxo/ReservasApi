from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Docente(Base):
    __tablename__ = "docentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    codigo = Column(String(20), nullable=False, unique=True)
    estado = Column(Boolean, default=True)
    tipocontrato = Column(String(50), nullable=False)
    horassemanal = Column(Integer, nullable=False)
    horasactual = Column(Integer, nullable=True)
    horastemporales = Column(Integer, nullable=True)
    horastotales = Column(Integer, nullable=True)
    horasdejara = Column(Integer, nullable=True)
    observaciones = Column(String, nullable=True)

    asignaciones_curso_docente = relationship(
        "AsignacionCursoDocente",
        back_populates="docente"
    )
