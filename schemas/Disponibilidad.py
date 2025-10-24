from pydantic import BaseModel
from typing import List, Optional
from datetime import time

class Horario(BaseModel):
    hora_inicio: time
    hora_fin: time

class DisponibilidadDocenteBase(BaseModel):
    dia: str
    modalidad: str
    turno: str
    horarios: Optional[List[Horario]] = []

class DisponibilidadDocenteCreate(DisponibilidadDocenteBase):
    pass

class DisponibilidadDocenteUpdate(BaseModel):
    dia: Optional[str] = None
    modalidad: Optional[str] = None
    turno: Optional[str] = None
    horarios: Optional[List[Horario]] = None

class DisponibilidadDocenteResponse(DisponibilidadDocenteBase):
    id: int
    docente_id: int

    class Config:
        orm_mode = True
