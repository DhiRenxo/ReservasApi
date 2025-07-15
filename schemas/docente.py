from pydantic import BaseModel, Field

class DocenteBase(BaseModel):
    nombre: str
    codigo: str = Field(..., max_length=20, min_length=2)
    estado: bool = True
    tipocontrato: str
    horassemanal: int
    horasactual: int = 0  

class DocenteCreate(DocenteBase):
    pass

class DocenteUpdate(DocenteBase):
    pass

class DocenteOut(DocenteBase):
    id: int

    class Config:
        from_attributes = True
