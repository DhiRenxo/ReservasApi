from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from models.carrera import Carrera

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique = True)
    nombre = Column(String(50))
    ciclo = Column(String(50))
    carreid = Column(Integer, ForeignKey("carrera.id"))

    carrera = relationship("Carrera")

    
