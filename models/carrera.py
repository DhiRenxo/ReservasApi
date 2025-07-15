# models/docente.py
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Carrera(Base):
    __tablename__ = "carrera"

    id=Column(Integer, primary_key=True, index=True)
    nombre= Column(String(50))
    nomenglatura= Column(String(1), unique=True)
    
    
