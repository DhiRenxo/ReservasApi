# models/docente.py
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Docente(Base):
    __tablename__ = "docentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    codigo = Column(String(20), unique=True, nullable=False)
    estado = Column(Boolean, default=True)
    tipocontrato = Column(String(50), nullable = False)
    horassemanal = Column(Integer, nullable = False)
    horasactual = Column(Integer, nullable= True)
    