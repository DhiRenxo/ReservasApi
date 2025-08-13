from sqlalchemy.orm import Session
from models.asignacion import AsignacionDocenteTemporal
from models.docente import Docente

class AsignacionDocenteService:
    def __init__(self, db: Session):
        self.db = db

    def calcular_horas_temporales(self, docente_id: int) -> int:
        horas_totales = 0

        asignaciones = (
            self.db.query(AsignacionDocenteTemporal)
            .join(AsignacionDocenteTemporal.docentes)
            .filter(Docente.id == docente_id)
            .all()
        )

        for asignacion in asignaciones:
            for curso in asignacion.cursos:
                horas_totales += curso.horas or 0

        docente = self.db.query(Docente).filter(Docente.id == docente_id).first()
        if docente:
            docente.horastemporales = horas_totales
            self.db.commit()
            self.db.refresh(docente)

        return horas_totales

    def calcular_horas_todos_docentes(self):
        docentes = self.db.query(Docente).all()
        resultado = []
        for docente in docentes:
            horas = self.calcular_horas_temporales(docente.id)
            resultado.append({
                "docente_id": docente.id,
                "nombre": docente.nombre,
                "horastemporales": horas
            })
        return resultado
