from pydantic import BaseModel, Field
from typing import Optional

class DocenteBase(BaseModel):
    nombre: str
    codigo: str = Field(..., max_length=20, min_length=2)
    estado: bool = True
    correo: Optional[str] = None
    tipocontrato: str
    horassemanal: int
    horasactual: Optional[int] = None
    horastemporales: Optional[int] = None
    horastotales: Optional[int] = None
    horasdejara: Optional[int] = None
    observaciones: Optional[str] = None

class DocenteCreate(DocenteBase):
    pass

class DocenteUpdate(DocenteBase):
    pass

class DocenteOut(DocenteBase):
    id: int

    class Config:
        orm_mode = True
