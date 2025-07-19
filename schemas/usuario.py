from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: EmailStr
    foto_url: Optional[HttpUrl] = None
    email_verificado: Optional[bool] = False
    estado: Optional[bool] = True
    fechacreacion: Optional[datetime]
    fechaactualizacion: Optional[datetime]
    rolid: int

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    foto_url: Optional[HttpUrl] = None
    estado: Optional[bool] = None
    rolid: Optional[int] = None
    fechaactualizacion: Optional[datetime]

class UsuarioResponse(UsuarioBase):
    id: int
    fechacreacion: Optional[datetime]

    class Config:
        orm_mode = True