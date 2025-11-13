from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import BaseSync
from models.tipoambiente import TipoAmbiente


class Ambiente(BaseSync):
    __tablename__ = "ambientes"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique=True, nullable=False)
    tipoid = Column(Integer, ForeignKey("tipoambiente.id"), nullable=False)
    capacidad = Column(Integer, nullable=False)
    equipamiento = Column(String(255))
    ubicacion = Column(String(100))
    activo = Column(Boolean, default=True)

    tipo_ambiente = relationship("TipoAmbiente", back_populates="ambientes", lazy="selectin" )

