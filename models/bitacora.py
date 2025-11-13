from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import BaseSync

class BitacoraReserva(BaseSync):
    __tablename__ = "bitacorareservas"

    id = Column(Integer, primary_key=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"))
    accion = Column(String(100))
    realizadopor = Column(Integer) 
    fecha = Column(DateTime)
    comentario = Column(String(255))

    reserva = relationship("Reserva")
