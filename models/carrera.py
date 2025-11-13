# models/docente.py
from sqlalchemy import Column, Integer, String, Boolean
from app.database import BaseSync

class Carrera(BaseSync):
    __tablename__ = "carrera"

    id=Column(Integer, primary_key=True, index=True)
    nombre= Column(String(50))
    nomenglatura= Column(String(1), unique=True)
    status = Column(Boolean, nullable=False, default=True)

    
    
