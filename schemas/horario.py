from pydantic import BaseModel

class HorarioAcademicoBase(BaseModel):
    ambienteid: int
    diasemana: str
    horainicio: str
    horafin: str
    grupo: str
    curso: str
    docente: str

class HorarioAcademicoCreate(HorarioAcademicoBase):
    pass

class HorarioAcademico(HorarioAcademicoBase):
    id: int

    class Config:
        orm_mode = True
