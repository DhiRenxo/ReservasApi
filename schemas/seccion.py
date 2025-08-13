from pydantic import BaseModel
from datetime import date
from typing import Optional

class SeccionBase(BaseModel):
    nombre: str
    carreraid: int
    ciclo: int
    letra: str
    turno: str
    serie: int
    modalidad: Optional[str] = None
    fecha_creacion: Optional[date] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[bool] = True

class SeccionCreate(SeccionBase):
    pass

class SeccionUpdate(SeccionBase):
    pass

class SeccionEstado(BaseModel):
    modalidad: str
    estado: bool

class Seccion(BaseModel):
    id: int
    nombre: str
    carreraid: int
    ciclo: int
    letra: str
    turno: str
    serie: int
    modalidad: Optional[str] = None
    fecha_creacion: Optional[date]
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    estado: bool

    class Config:
        orm_mode = True
