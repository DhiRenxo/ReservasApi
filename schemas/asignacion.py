# schemas/asignacion.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# -------- Asignación Base --------
class AsignacionBase(BaseModel):
    carreraid: int
    plan: str
    ciclo: str
    modalidad: Optional[str] = None
    cantidad_secciones: int = 1
    secciones_asignadas: Optional[int] = None
    estado: Optional[bool] = True
    fecha_inicio: Optional[datetime] = None

# -------- Crear Asignación --------
class AsignacionCreate(AsignacionBase):
    pass

# -------- Actualizar Asignación --------
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



# -------- Response --------
class AsignacionResponse(AsignacionBase):
    id: int
    fecha_asignacion: datetime
    fecha_modificada: datetime

    class Config:
        orm_mode = True


# -------- Relación AsignaciónCursoDocente --------
class AsignacionCursoDocenteBase(BaseModel):
    asignacion_id: int
    curso_id: int
    docente_id: int

class AsignacionCursoDocenteCreate(AsignacionCursoDocenteBase):
    pass

class AsignacionCursoDocenteResponse(AsignacionCursoDocenteBase):
    id: int
    class Config:
        orm_mode = True
