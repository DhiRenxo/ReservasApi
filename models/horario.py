from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from models.seccion import Seccion

class HorarioAcademico(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True)
    ambienteid = Column(Integer, ForeignKey("ambientes.id"))
    cursoid = Column(Integer,ForeignKey("cursos.id"))
    diasemana = Column(String(15))
    horainicio = Column(String(5))
    horafin = Column(String(5))
    docenteid = Column(Integer, ForeignKey("docentes.id"))
    seccionid = Column(Integer, ForeignKey("seccion.id"))

    ambiente = relationship("Ambiente")
    curso = relationship("Curso")
    docente = relationship("Docente")
    seccion = relationship("Seccion")                                                                                       