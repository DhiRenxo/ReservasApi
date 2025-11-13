from pydantic import BaseModel, Field, validator
from typing import Optional

class HorarioAcademicoBase(BaseModel):
    ambienteid: int = Field(..., gt=0)
    cursoid: int = Field(..., gt=0)
    docenteid: int = Field(..., gt=0)
    seccionid: int = Field(..., gt=0)
    diasemana: str = Field(..., max_length=15, description="Día de la semana (Lunes a Domingo)")
    horainicio: str = Field(..., pattern=r"^\d{2}:\d{2}$", max_length=5, description="Hora de inicio HH:MM")
    horafin: str = Field(..., pattern=r"^\d{2}:\d{2}$", max_length=5, description="Hora de fin HH:MM")

    @validator("diasemana")
    def validar_diasemana(cls, v):
        dias_validos = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        if v.capitalize() not in dias_validos:
            raise ValueError("El día debe estar entre Lunes y Domingo")
        return v.capitalize()

    @validator("horafin")
    def validar_horas(cls, fin, values):
        inicio = values.get("horainicio")
        if inicio and fin:
            h1, m1 = map(int, inicio.split(":"))
            h2, m2 = map(int, fin.split(":"))
            if (h2, m2) <= (h1, m1):
                raise ValueError("La hora de fin debe ser posterior a la de inicio")
        return fin


class HorarioAcademicoCreate(HorarioAcademicoBase):
    pass


class HorarioAcademico(HorarioAcademicoBase):
    id: int

    class Config:
        from_attributes = True
