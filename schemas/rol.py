from pydantic import BaseModel

class RolBase(BaseModel):
    nombre: str  # ahora cualquier string es válido

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: str  # cualquier string

class RolResponse(RolBase):
    id: int

    class Config:
        orm_mode = True
