from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AsignacionBase(BaseModel):
    docenteid: int
    cursoid: int
    carreraid: int
    ciclo: str
    cantidad_secciones: int
    secciones_asignadas: int
    horas_curso: int
    horas_actuales: int
    horas_dejara: Optional[int] = None
    horas_totales: Optional[int] = None
    observaciones: Optional[str] = None


class AsignacionCreate(AsignacionBase):
    pass


class AsignacionUpdate(BaseModel):
    cantidad_secciones: Optional[int]
    secciones_asignadas: Optional[int]
    horas_curso: Optional[int]
    horas_actuales: Optional[int]
    horas_dejara: Optional[int]
    horas_totales: Optional[int]
    observaciones: Optional[str]

    model_config = {
        "from_attributes": True  
    }


class AsignacionResponse(AsignacionBase):
    id: int
    fecha_asignacion: datetime
    fecha_modificada: datetime

    model_config = {
        "from_attributes": True  
    }
