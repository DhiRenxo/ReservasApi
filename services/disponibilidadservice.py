from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from models.DisponibilidadDocente import DisponibilidadDocente
from models.docente import Docente
from schemas.Disponibilidad import DisponibilidadDocenteCreate, DisponibilidadDocenteUpdate


class DisponibilidadService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_docente_by_correo(self, correo: str) -> Optional[Docente]:
        result = await self.db.execute(select(Docente).filter(Docente.correo == correo))
        return result.scalar_one_or_none()

    def _serialize_horarios(self, horarios: List) -> List[dict]:
        """
        Convierte los horarios a un formato JSON serializable.
        Acepta datetime.time o strings en formato "HH:MM".
        """
        import datetime
        serialized = []
        for h in horarios:
            hora_inicio = h.get("hora_inicio")
            hora_fin = h.get("hora_fin")
            if isinstance(hora_inicio, datetime.time):
                hora_inicio = hora_inicio.strftime("%H:%M")
            if isinstance(hora_fin, datetime.time):
                hora_fin = hora_fin.strftime("%H:%M")
            serialized.append({"hora_inicio": hora_inicio, "hora_fin": hora_fin})
        return serialized

    async def create_or_update(self, data: DisponibilidadDocenteCreate, correo_docente: str) -> DisponibilidadDocente:
        docente = await self.get_docente_by_correo(correo_docente)
        if not docente:
            return None

        result = await self.db.execute(
            select(DisponibilidadDocente).filter(
                DisponibilidadDocente.docente_id == docente.id,
                DisponibilidadDocente.modalidad == data.modalidad,
                DisponibilidadDocente.turno == data.turno,
                DisponibilidadDocente.dia == data.dia
            )
        )
        disponibilidad = result.scalar_one_or_none()

        horarios_serializados = self._serialize_horarios([h.dict() for h in data.horarios]) if data.horarios else []

        if disponibilidad:
            disponibilidad.horarios = horarios_serializados
            await self.db.commit()
            await self.db.refresh(disponibilidad)
            return disponibilidad
        else:
            nueva = DisponibilidadDocente(
                docente_id=docente.id,
                dia=data.dia,
                modalidad=data.modalidad,
                turno=data.turno,
                horarios=horarios_serializados
            )
            self.db.add(nueva)
            await self.db.commit()
            await self.db.refresh(nueva)
            return nueva

    async def get_by_docente(
        self,
        docente_id: int,
        modalidad: Optional[str] = None,
        turno: Optional[str] = None
    ) -> List[DisponibilidadDocente]:
        query = select(DisponibilidadDocente).filter(DisponibilidadDocente.docente_id == docente_id)
        if modalidad:
            query = query.filter(DisponibilidadDocente.modalidad == modalidad)
        if turno:
            query = query.filter(DisponibilidadDocente.turno == turno)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Optional[DisponibilidadDocente]:
        result = await self.db.execute(select(DisponibilidadDocente).filter(DisponibilidadDocente.id == id))
        return result.scalar_one_or_none()

    async def update(self, id: int, data: DisponibilidadDocenteUpdate, correo_docente: str) -> Optional[DisponibilidadDocente]:
        docente = await self.get_docente_by_correo(correo_docente)
        if not docente:
            return None

        disponibilidad = await self.get_by_id(id)
        if not disponibilidad or disponibilidad.docente_id != docente.id:
            return None

        update_data = data.dict(exclude_unset=True)
        if "horarios" in update_data and update_data["horarios"] is not None:
            update_data["horarios"] = self._serialize_horarios([h.dict() for h in update_data["horarios"]])

        for key, value in update_data.items():
            setattr(disponibilidad, key, value)

        await self.db.commit()
        await self.db.refresh(disponibilidad)
        return disponibilidad

    async def delete(self, dia: str, modalidad: str, turno: str, correo_docente: str) -> bool:
        docente = await self.get_docente_by_correo(correo_docente)
        if not docente:
            return False

        result = await self.db.execute(
            select(DisponibilidadDocente).filter(
                DisponibilidadDocente.docente_id == docente.id,
                DisponibilidadDocente.modalidad == modalidad,
                DisponibilidadDocente.turno == turno,
                DisponibilidadDocente.dia == dia
            )
        )
        disponibilidad = result.scalar_one_or_none()
        if not disponibilidad:
            return False

        await self.db.delete(disponibilidad)
        await self.db.commit()
        return True
