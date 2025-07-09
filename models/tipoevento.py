from sqlalchemy import Column, Integer, String
from app.database import Base

class TipoEvento(Base):
    __tablename__ = "tiposevento"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
