from pydantic import BaseModel
from typing import Optional

class CursoBase(BaseModel):
    codigo: str
    nombre: str
    docente: str

class CursoCreate(CursoBase):
    pass

class CursoUpdate(CursoBase):
    pass

class CursoOut(CursoBase):
    id: int

    class Config:
        orm_mode = True
