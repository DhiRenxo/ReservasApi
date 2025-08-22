# schemas/asignacion.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class AsignacionBase(BaseModel):
    carreraid: int
    plan: str
    ciclo: str
    modalidad: Optional[str] = None
    cantidad_secciones: int = 1
    secciones_asignadas: Optional[int] = None
    estado: Optional[bool] = True
    fecha_inicio: Optional[datetime] = None

class AsignacionCreate(AsignacionBase):
    pass

class AsignacionUpdate(BaseModel):
    plan: Optional[str] = None
    ciclo: Optional[str] = None
    modalidad: Optional[str] = None
    cantidad_secciones: Optional[int] = None
    secciones_asignadas: Optional[int] = None
    estado: Optional[bool] = None
    fecha_inicio: Optional[datetime] = None

class AsignacionUpdateSecciones(BaseModel):
    cantidad_secciones: int

class AsignacionUpdateEstado(BaseModel):
    estado: bool


class AsignacionResponse(AsignacionBase):
    id: int
    fecha_asignacion: datetime
    fecha_modificada: datetime

    class Config:
        orm_mode = True


class CursosUpdate(BaseModel):
    curso_ids: List[int]
    docente_id: Optional[int] = None

class AsignacionCursoDocenteBase(BaseModel):
    asignacion_id: int
    curso_id: int
    seccion: int
    docente_id: Optional[int] = None
    es_bloque: Optional[bool] = False
    bloque: Optional[str] = None   
    duplica_horas: Optional[bool] = False
    comentario: Optional[str] = None
    disponibilidad: Optional[str] = None

class AsignacionCursoDocenteCreate(AsignacionCursoDocenteBase):
    pass

class DocenteUpdate(BaseModel):
    curso_id: int
    seccion: int
    docente_id: int

class AsignacionCursoDocenteResponse(AsignacionCursoDocenteBase):
    id: int
    class Config:
        orm_mode = True
