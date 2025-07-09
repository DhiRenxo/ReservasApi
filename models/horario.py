from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class HorarioAcademico(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True)
    ambienteid = Column(Integer, ForeignKey("ambientes.id"))
    cursoid = Column(Integer,ForeignKey("cursos.id"))
    diasemana = Column(String(15))
    horainicio = Column(String(5))
    horafin = Column(String(5))
    grupo = Column(String(50))
    curso = Column(String(100))
    docente = Column(String(100))

    ambiente = relationship("Ambiente")
    curso = relationship("Cursos")
