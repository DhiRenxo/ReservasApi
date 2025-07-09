from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base
from utils.enums import EstadoAprobacion, RolUsuario

class AprobacionReserva(Base):
    __tablename__ = "aprobaciones"

    id = Column(Integer, primary_key=True)
    reservaid = Column(Integer, ForeignKey("reservas.id"))
    aprobadorid = Column(Integer, ForeignKey("usuarios.id"))
    tipoaprobador = Column(SqlEnum(RolUsuario))
    estado = Column(SqlEnum(EstadoAprobacion), default=EstadoAprobacion.PENDIENTE)
    fecha_respuesta = Column(DateTime)
    comentario = Column(String(255))

    reserva = relationship("Reserva")
    aprobador = relationship("Usuario")
