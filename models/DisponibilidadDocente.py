from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class DisponibilidadDocente(Base):
    __tablename__ = "disponibilidad_docente"

    id = Column(Integer, primary_key=True, index=True)
    
    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=False)
    docente = relationship("Docente", back_populates="disponibilidades")

    dia = Column(String(20), nullable=False)        
    modalidad = Column(String(20), nullable=False) 
    turno = Column(String(10), nullable=False)  
    horarios = Column(JSON, nullable=True, default=[])  
