from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.horario import HorarioAcademico
from models.cursos import Curso
from models.docente import Docente
from models.ambiente import Ambiente
from schemas.horario import HorarioAcademicoCreate
from fastapi import HTTPException
import re


async def validar_horario(horario: HorarioAcademicoCreate):
    if not re.match(r"^\d{2}:\d{2}$", horario.horainicio):
        raise HTTPException(status_code=400, detail="Hora inicio debe tener formato HH:MM")
    if not re.match(r"^\d{2}:\d{2}$", horario.horafin):
        raise HTTPException(status_code=400, detail="Hora fin debe tener formato HH:MM")
    if horario.horainicio >= horario.horafin:
        raise HTTPException(status_code=400, detail="Hora inicio debe ser menor que hora fin")


async def crear_horario(db: AsyncSession, horario_data: HorarioAcademicoCreate):
    await validar_horario(horario_data)

    result_curso = await db.execute(select(Curso).filter(Curso.codigo == horario_data.curso))
    curso = result_curso.scalar_one_or_none()
    if not curso:
        raise HTTPException(status_code=404, detail=f"Curso con código '{horario_data.curso}' no encontrado")

    result_docente = await db.execute(select(Docente).filter(Docente.codigo == horario_data.docente))
    docente = result_docente.scalar_one_or_none()
    if not docente:
        raise HTTPException(status_code=404, detail=f"Docente con sigla '{horario_data.docente}' no encontrado")

    result_ambiente = await db.execute(select(Ambiente).filter(Ambiente.id == horario_data.ambienteid))
    ambiente = result_ambiente.scalar_one_or_none()
    if not ambiente:
        raise HTTPException(status_code=404, detail=f"Ambiente ID '{horario_data.ambienteid}' no encontrado")

    horario = HorarioAcademico(
        ambienteid=ambiente.id,
        cursoid=curso.id,
        docenteid=docente.id,
        diasemana=horario_data.diasemana,
        horainicio=horario_data.horainicio,
        horafin=horario_data.horafin,
        grupo=horario_data.grupo
    )

    db.add(horario)
    await db.commit()
    await db.refresh(horario)
    return horario


async def listar_horarios(db: AsyncSession):
    result = await db.execute(select(HorarioAcademico))
    return result.scalars().all()


async def actualizar_horario(db: AsyncSession, id: int, horario_data: HorarioAcademicoCreate):
    await validar_horario(horario_data)

    result_horario = await db.execute(select(HorarioAcademico).filter_by(id=id))
    horario = result_horario.scalar_one_or_none()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    result_curso = await db.execute(select(Curso).filter(Curso.codigo == horario_data.curso))
    curso = result_curso.scalar_one_or_none()
    if not curso:
        raise HTTPException(status_code=404, detail=f"Curso con código '{horario_data.curso}' no encontrado")

    result_docente = await db.execute(select(Docente).filter(Docente.codigo == horario_data.docente))
    docente = result_docente.scalar_one_or_none()
    if not docente:
        raise HTTPException(status_code=404, detail=f"Docente con sigla '{horario_data.docente}' no encontrado")

    result_ambiente = await db.execute(select(Ambiente).filter(Ambiente.id == horario_data.ambienteid))
    ambiente = result_ambiente.scalar_one_or_none()
    if not ambiente:
        raise HTTPException(status_code=404, detail=f"Ambiente ID '{horario_data.ambienteid}' no encontrado")

    horario.cursoid = curso.id
    horario.docenteid = docente.id
    horario.ambienteid = ambiente.id
    horario.diasemana = horario_data.diasemana
    horario.horainicio = horario_data.horainicio
    horario.horafin = horario_data.horafin
    horario.grupo = horario_data.grupo

    await db.commit()
    await db.refresh(horario)
    return horario


async def eliminar_horario(db: AsyncSession, id: int):
    result_horario = await db.execute(select(HorarioAcademico).filter_by(id=id))
    horario = result_horario.scalar_one_or_none()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    await db.delete(horario)
    await db.commit()
    return {"mensaje": "Horario eliminado correctamente"}
