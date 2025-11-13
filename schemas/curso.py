from pydantic import BaseModel, Field
from typing import Optional

class CursoBase(BaseModel):
    codigo: str = Field(..., max_length=50)
    modalidad: str 
    nombre: str
    horas: int
    ciclo: str
    plan: str
    carreid: int
    horasasignadas: Optional[str] = None

class CursoCreate(CursoBase):
    pass

class CursoUpdate(CursoBase):
    pass

class CursoResponse(CursoBase):
    id: int
    estado: bool

    class Config:
        from_attributes = True 