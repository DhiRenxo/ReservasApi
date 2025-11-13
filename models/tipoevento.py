from sqlalchemy import Column, Integer, String
from app.database import BaseSync

class TipoEvento(BaseSync):
    __tablename__ = "tiposevento"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
