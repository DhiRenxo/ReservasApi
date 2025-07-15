from datetime import datetime
from pydantic import BaseModel

class BitacoraReservaBase(BaseModel):
    reservaid: int
    accion: str
    realizadopor: int
    fecha: datetime
    comentario: str | None = None

class BitacoraReservaCreate(BitacoraReservaBase):
    pass

class BitacoraReserva(BitacoraReservaBase):
    id: int

    model_config = {
        "from_attributes": True  
    }