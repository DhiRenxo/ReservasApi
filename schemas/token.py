from pydantic import BaseModel
from typing import Optional

class GoogleLoginRequest(BaseModel):
    google_token: str

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    correo: str
    rolid: int
    foto_url: Optional[str]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
