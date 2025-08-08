from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AsignacionBase(BaseModel):
    carreraid: int
    plan: str
    ciclo: str
    modalidad: str
    cantidad_secciones: int
    secciones_asignadas: int
    estado: Optional[bool] = True

class AsignacionCreate(AsignacionBase):
    curso_ids: List[int]
    docente_ids: Optional[List[int]] = None  

class AsignacionUpdate(AsignacionBase):
    curso_ids: Optional[List[int]] = None  
    docente_ids: Optional[List[int]] = None

class AsignacionEstadoUpdate(BaseModel):
    estado: bool

class AsignacionDelete(BaseModel):
    id: int

class AsignacionSchema(AsignacionBase):
    id: int
    fecha_asignacion: datetime
    fecha_modificada: Optional[datetime]

    class Config:
        orm_mode = True
