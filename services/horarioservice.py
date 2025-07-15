from sqlalchemy.orm import Session
from models.horario import HorarioAcademico
from models.cursos import Curso
from models.docente import Docente
from models.ambiente import Ambiente
from schemas.horario import HorarioAcademicoCreate
from fastapi import HTTPException
import re

def validar_horario(horario: HorarioAcademicoCreate):
    if not re.match(r"^\d{2}:\d{2}$", horario.horainicio):
        raise HTTPException(status_code=400, detail="Hora inicio debe tener formato HH:MM")
    if not re.match(r"^\d{2}:\d{2}$", horario.horafin):
        raise HTTPException(status_code=400, detail="Hora fin debe tener formato HH:MM")
    if horario.horainicio >= horario.horafin:
        raise HTTPException(status_code=400, detail="Hora inicio debe ser menor que hora fin")

def crear_horario(db: Session, horario_data: HorarioAcademicoCreate):
    validar_horario(horario_data)

    curso = db.query(Curso).filter(Curso.codigo == horario_data.curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail=f"Curso con código '{horario_data.curso}' no encontrado")

    docente = db.query(Docente).filter(Docente.codigo == horario_data.docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail=f"Docente con sigla '{horario_data.docente}' no encontrado")

    ambiente = db.query(Ambiente).filter(Ambiente.id == horario_data.ambienteid).first()
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
    db.commit()
    db.refresh(horario)
    return horario

def listar_horarios(db: Session):
    return db.query(HorarioAcademico).all()

def actualizar_horario(db: Session, id: int, horario_data: HorarioAcademicoCreate):
    validar_horario(horario_data)

    horario = db.query(HorarioAcademico).filter_by(id=id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    curso = db.query(Curso).filter(Curso.codigo == horario_data.curso).first()
    if not curso:
        raise HTTPException(status_code=404, detail=f"Curso con código '{horario_data.curso}' no encontrado")

    docente = db.query(Docente).filter(Docente.codigo == horario_data.docente).first()
    if not docente:
        raise HTTPException(status_code=404, detail=f"Docente con sigla '{horario_data.docente}' no encontrado")

    ambiente = db.query(Ambiente).filter(Ambiente.id == horario_data.ambienteid).first()
    if not ambiente:
        raise HTTPException(status_code=404, detail=f"Ambiente ID '{horario_data.ambienteid}' no encontrado")

    horario.cursoid = curso.id
    horario.docenteid = docente.id
    horario.ambienteid = ambiente.id
    horario.diasemana = horario_data.diasemana
    horario.horainicio = horario_data.horainicio
    horario.horafin = horario_data.horafin
    horario.grupo = horario_data.grupo

    db.commit()
    db.refresh(horario)
    return horario

def eliminar_horario(db: Session, id: int):
    horario = db.query(HorarioAcademico).filter_by(id=id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    db.delete(horario)
    db.commit()
    return {"mensaje": "Horario eliminado correctamente"}
