from datetime import datetime
from pydantic import BaseModel

class EventoEspecialBase(BaseModel):
    ambienteid: int
    nombreevento: str
    fecha: datetime
    horainicio: str
    horafin: str
    organizador: str
    observaciones: str | None = None

class EventoEspecialCreate(EventoEspecialBase):
    pass

class EventoEspecial(EventoEspecialBase):
    id: int

    class Config:
        from_attributes = True 