from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)  # usado para login
    foto_url = Column(String(255), nullable=True)
    email_verificado = Column(Boolean, default=False)
    rolid = Column(Integer, ForeignKey("roles.id"))
    estado = Column(Boolean, default=True)
    fechacreacion = Column(DateTime, default=func.now())
    fechaactualizacion = Column(DateTime, onupdate=func.now())
    calle_tipo = Column(String(20), nullable=True)      # Ej: Av., Jr., Psj.
    calle_nombre = Column(String(100), nullable=True)   # Nombre de la calle
    calle_numero = Column(String(10), nullable=True)    # Número de la calle
    ciudad = Column(String(50), nullable=True)    # Ciudad
    departamento = Column(String(50), nullable=True)  # Departamento
    telefono = Column(String(20), nullable=True)
    contacto_nombre = Column(String(50), nullable=True)
    contacto_numero = Column(String(20), nullable=True)
    correo_alternativo = Column(String(100), nullable=True)
    cod_docente = Column(String(5), nullable=True)

    rol = relationship("Rol", back_populates="usuarios")
