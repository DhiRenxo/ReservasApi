from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from utils.enums import RolUsuario  

class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)  
    
    usuarios = relationship("Usuario", back_populates="rol")
