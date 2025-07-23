from pydantic import BaseModel, Field

class CursoBase(BaseModel):
    codigo: str = Field(..., max_length=50)
    nombre: str
    horas: int
    ciclo: str
    plan: str
    carreid: int

class CursoCreate(CursoBase):
    pass

class CursoUpdate(CursoBase):
    pass

class CursoResponse(CursoBase):
    id: int
    estado: bool

    class Config:
        orm_mode = True