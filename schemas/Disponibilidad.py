from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import time

class Horario(BaseModel):
    hora_inicio: str
    hora_fin: str

class DisponibilidadDocenteBase(BaseModel):
    docente_id: int
    dia: str = Field(..., max_length=20)
    modalidad: str = Field(..., max_length=20)
    turno: str = Field(..., max_length=10)  
    horarios: Optional[List[Horario]] = []

class DisponibilidadDocenteCreate(DisponibilidadDocenteBase):
    pass

class DisponibilidadDocenteUpdate(BaseModel):
    id: Optional[int]
    dia: Optional[str] = None
    modalidad: Optional[str] = None
    turno: Optional[str] = None
    horarios: Optional[List[Horario]]

class DisponibilidadDocenteResponse(DisponibilidadDocenteBase):
    class Config:
        orm_mode = True
