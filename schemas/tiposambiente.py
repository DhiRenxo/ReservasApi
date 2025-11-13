from pydantic import BaseModel

class TipoAmbienteBase(BaseModel):
    nombre: str
    colorhex: str | None = None

class TipoAmbienteCreate(TipoAmbienteBase):
    pass

class TipoAmbienteResponse(TipoAmbienteBase):
    id: int

    class Config:
        from_attributes = True 