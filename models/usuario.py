from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    foto_url = Column(String(255), nullable=True)
    email_verificado = Column(Boolean, default=False)
    rolid = Column(Integer, ForeignKey("roles.id"))
    estado = Column(Boolean, default=True)
    fechacreacion = Column(DateTime, default=func.now())
    fechaactualizacion = Column(DateTime, onupdate=func.now())

    rol = relationship("Rol", back_populates="usuarios")
