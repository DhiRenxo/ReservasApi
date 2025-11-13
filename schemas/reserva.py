from datetime import datetime
from pydantic import BaseModel
from .usuario import Usuario
from .ambiente import Ambiente
from .tipoevento import TipoEvento

class ReservaBase(BaseModel):
    usuarioid: int
    ambienteid: int
    tipoeventoid: int
    motivo: str
    fecha: datetime
    horainicio: str
    horafin: str
    estado: str
    fechasolicitud: datetime
    fecharespuesta: datetime | None = None
    respondidopor: int | None = None

class ReservaCreate(ReservaBase):
    pass

class Reserva(ReservaBase):
    id: int
    usuario: Usuario
    ambiente: Ambiente
    tipoevento: TipoEvento

    class Config:
        from_attributes = True 