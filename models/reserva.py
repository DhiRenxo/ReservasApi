from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base
from utils.enums import EstadoReserva

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True)
    solicitante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    aprobador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    ambiente_id = Column(Integer, ForeignKey("ambientes.id"))
    tipo_evento_id = Column(Integer, ForeignKey("tiposevento.id"))

    motivo = Column(String(255))
    fecha = Column(DateTime)
    hora_inicio = Column(DateTime)
    hora_fin = Column(DateTime)
    estado = Column(SqlEnum(EstadoReserva), default=EstadoReserva.PENDIENTE)
    fecha_solicitud = Column(DateTime)
    fecha_respuesta = Column(DateTime)

    solicitante = relationship("Usuario", foreign_keys=[solicitante_id], back_populates="reservas_solicitadas")
    aprobador = relationship("Usuario", foreign_keys=[aprobador_id], back_populates="reservas_aprobadas")
    ambiente = relationship("Ambiente")
    tipo_evento = relationship("TipoEvento")
