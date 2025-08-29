from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: EmailStr
    foto_url: Optional[HttpUrl] = None
    email_verificado: Optional[bool] = False
    estado: Optional[bool] = True
    rolid: int
    calle_tipo: Optional[str] = None
    calle_nombre: Optional[str] = None
    calle_numero: Optional[str] = None
    ciudad: Optional[str] = None
    departamento: Optional[str] = None
    telefono: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_numero: Optional[str] = None
    correo_alternativo: Optional[EmailStr] = None
    fechacreacion: Optional[datetime] = None
    fechaactualizacion: Optional[datetime] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    foto_url: Optional[HttpUrl] = None
    estado: Optional[bool] = None
    rolid: Optional[int] = None

    calle_tipo: Optional[str] = None
    calle_nombre: Optional[str] = None
    calle_numero: Optional[str] = None
    ciudad: Optional[str] = None
    departamento: Optional[str] = None

    telefono: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_numero: Optional[str] = None

    correo_alternativo: Optional[EmailStr] = None
    fechaactualizacion: Optional[datetime] = None

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
