from sqlalchemy.orm import Session
from typing import List, Optional
from models.DisponibilidadDocente import DisponibilidadDocente
from schemas.Disponibilidad import DisponibilidadDocenteCreate, DisponibilidadDocenteUpdate


class DisponibilidadService:
    def __init__(self, db: Session):
        self.db = db

    # Crear o actualizar disponibilidad según modalidad, turno y docente
    def create_or_update(self, data: DisponibilidadDocenteCreate) -> DisponibilidadDocente:
        # Buscar si ya existe una disponibilidad para el docente con misma modalidad y turno
        disponibilidad = self.db.query(DisponibilidadDocente).filter(
            DisponibilidadDocente.docente_id == data.docente_id,
            DisponibilidadDocente.modalidad == data.modalidad,
            DisponibilidadDocente.turno == data.turno,
            DisponibilidadDocente.dia == data.dia
        ).first()

        horarios_serializados = [
            {"hora_inicio": str(h.hora_inicio), "hora_fin": str(h.hora_fin)}
            for h in data.horarios
        ] if data.horarios else None

        if disponibilidad:
            # 👉 Si existe, actualizamos
            disponibilidad.horarios = horarios_serializados
            self.db.commit()
            self.db.refresh(disponibilidad)
            return disponibilidad
        else:
            # 👉 Si no existe, creamos
            nueva = DisponibilidadDocente(
                docente_id=data.docente_id,
                dia=data.dia,
                modalidad=data.modalidad,
                turno=data.turno,
                horarios=horarios_serializados
            )
            self.db.add(nueva)
            self.db.commit()
            self.db.refresh(nueva)
            return nueva

    # Obtener todas las disponibilidades de un docente (con filtros opcionales)
    def get_by_docente(
        self,
        docente_id: int,
        modalidad: Optional[str] = None,
        turno: Optional[str] = None
    ) -> List[DisponibilidadDocente]:
        query = self.db.query(DisponibilidadDocente).filter(
            DisponibilidadDocente.docente_id == docente_id
        )
        if modalidad:
            query = query.filter(DisponibilidadDocente.modalidad == modalidad)
        if turno:
            query = query.filter(DisponibilidadDocente.turno == turno)
        return query.all()

    # Obtener disponibilidad por ID
    def get_by_id(self, id: int) -> Optional[DisponibilidadDocente]:
        return self.db.query(DisponibilidadDocente).filter(DisponibilidadDocente.id == id).first()

    # Actualizar disponibilidad (solo si coinciden los tres campos)
    def update(self, id: int, data: DisponibilidadDocenteUpdate) -> Optional[DisponibilidadDocente]:
        disponibilidad = self.get_by_id(id)
        if not disponibilidad:
            return None

        # Validar que coincide modalidad y turno
        if (
            data.modalidad and data.modalidad != disponibilidad.modalidad or
            data.turno and data.turno != disponibilidad.turno or
            data.dia and data.dia != disponibilidad.dia
        ):
            # 👉 Si no coincide, se guarda como nuevo registro
            return self.create_or_update(DisponibilidadDocenteCreate(**data.dict()))

        update_data = data.dict(exclude_unset=True)
        if "horarios" in update_data and update_data["horarios"] is not None:
            update_data["horarios"] = [
                {"hora_inicio": str(h.hora_inicio), "hora_fin": str(h.hora_fin)}
                for h in update_data["horarios"]
            ]

        for key, value in update_data.items():
            setattr(disponibilidad, key, value)

        self.db.commit()
        self.db.refresh(disponibilidad)
        return disponibilidad

    # Eliminar disponibilidad (debe coincidir con modalidad y turno)
    def delete(self, docente_id: int, modalidad: str, turno: str, dia: str) -> bool:
        disponibilidad = self.db.query(DisponibilidadDocente).filter(
            DisponibilidadDocente.docente_id == docente_id,
            DisponibilidadDocente.modalidad == modalidad,
            DisponibilidadDocente.turno == turno,
            DisponibilidadDocente.dia == dia
        ).first()
        if not disponibilidad:
            return False
        self.db.delete(disponibilidad)
        self.db.commit()
        return True


def get_disponibilidades_by_docente(db: Session, docente_id: int):
    return db.query(DisponibilidadDocente).filter(DisponibilidadDocente.docente_id == docente_id).all()
