from datetime import datetime
from pydantic import BaseModel

class AprobacionReservaBase(BaseModel):
    reservaid: int
    aprobadorid: int
    tipoaprobador: str
    estado: str
    fecharespuesta: datetime
    comentario: str | None = None

class AprobacionReservaCreate(AprobacionReservaBase):
    pass

class AprobacionReserva(AprobacionReservaBase):
    id: int

    class Config:
        from_attributes = True 