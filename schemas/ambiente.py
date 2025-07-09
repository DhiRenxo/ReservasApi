from pydantic import BaseModel, Field
from typing import Optional
from schemas.tiposambiente import TipoAmbienteResponse

class AmbienteBase(BaseModel):
    codigo: str = Field(..., max_length=7, min_length=3)
    tipoid: int
    capacidad: int = Field(..., gt=0)
    equipamiento: Optional[str] = None
    ubicacion: str
    activo: bool = True

class AmbienteCreate(AmbienteBase):
    pass

class AmbienteUpdate(AmbienteBase):
    pass

class AmbienteResponse(AmbienteBase):
    id: int
    tipo_ambiente: TipoAmbienteResponse 

    class Config:
        orm_mode = True
