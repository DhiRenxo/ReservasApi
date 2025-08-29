from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from models.carrera import Carrera
from models.asignacionseccion import asignacion_seccion

class Seccion(Base):
    __tablename__ = "seccion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(10))
    carreraid = Column(Integer, ForeignKey("carrera.id"))
    ciclo = Column(Integer)
    letra = Column(String(1))
    turno = Column(String(1))
    serie = Column(Integer)
    modalidad = Column(String(20))
    fecha_creacion = Column(Date)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    estado = Column(Boolean, default=True)  

    carrera = relationship("Carrera")

    asignaciones = relationship(
        "Asignacion",
        secondary=asignacion_seccion,
        back_populates="secciones"
    )