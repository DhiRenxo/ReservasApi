from pydantic import BaseModel

class TipoEventoBase(BaseModel):
    nombre: str

class TipoEventoCreate(TipoEventoBase):
    pass

class TipoEvento(TipoEventoBase):
    id: int

    class Config:
        orm_mode = True
