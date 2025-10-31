# schemas/asignacion.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# -----------------------------
# ASIGNACION
# -----------------------------
class AsignacionBase(BaseModel):
    carreraid: int
    plan: str
    ciclo: str
    modalidad: Optional[str] = None
    cantidad_secciones: int = 1
    seccion_asignada: Optional[bool] = False
    estado: Optional[bool] = True
    fecha_inicio: Optional[datetime] = None


class AsignacionCreate(AsignacionBase):
    pass


class AsignacionUpdate(BaseModel):
    plan: Optional[str] = None
    ciclo: Optional[str] = None
    modalidad: Optional[str] = None
    cantidad_secciones: Optional[int] = None
    seccion_asignada: Optional[bool] = False
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


# -----------------------------
# RELACION ASIGNACION - CURSO - DOCENTE
# -----------------------------
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
    activo: bool


class AsignacionCursoDocenteCreate(AsignacionCursoDocenteBase):
    pass


class DocenteUpdate(BaseModel):
    curso_id: int
    seccion: int
    docente_id: int


class AsignacionCursoDocenteComentarioUpdate(BaseModel):
    comentario: Optional[str] = None
    disponibilidad: Optional[str] = None


class AsignacionCursoDocenteUpdate(BaseModel):
    es_bloque: Optional[bool] = None
    bloque: Optional[str] = None  
    duplica_horas: Optional[bool] = None
    comentario: Optional[str] = None
    disponibilidad: Optional[str] = None
    activo: Optional[bool] = None

class CursosAsignadosDocenteResponse(BaseModel):
    docente_id: int
    asignacion_id: int
    carreraid: int
    carrera_nombre: str | None
    plan: str
    ciclo: str
    modalidad: Optional[str]
    curso_id: int
    curso_nombre: str
    seccion: Optional[int]
    estado: bool
    docente_nombre: str
    es_bloque: Optional[bool] = False
    bloque: Optional[str] = None
    activo: Optional[bool] = None


class AsignacionCursoDocenteResponse(AsignacionCursoDocenteBase):
    id: int
    activo: bool

    class Config:
        orm_mode = True
