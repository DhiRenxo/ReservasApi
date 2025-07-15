from pydantic import BaseModel, Field

class CarreraBase(BaseModel):
    nombre: str
    nomenglatura: str = Field(..., max_length=1, min_length=1)

class CarreraCreate(CarreraBase):
    pass

class CarreraUpdate(CarreraBase):
    pass

class CarreraOut(CarreraBase):
    id: int

    class Config:
        from_attributes = True
