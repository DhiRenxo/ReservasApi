from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class EventoEspecial(Base):
    __tablename__ = "eventosespeciales"

    id = Column(Integer, primary_key=True)
    reservaid = Column(Integer, ForeignKey("reservas.id"))
    nombreevento = Column(String(100))
    fecha = Column(DateTime)
    horainicio = Column(String(5))
    horafin = Column(String(5))
    organizador = Column(String(100))
    observaciones = Column(String(255))

    ambiente = relationship("Reserva")

