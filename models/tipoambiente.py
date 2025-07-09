from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class TipoAmbiente(Base):
    __tablename__ = "tipoambiente"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    colorhex = Column(String(7), nullable=True) 
    
    ambientes = relationship("Ambiente", back_populates="tipo_ambiente")