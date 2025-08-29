from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Tabla intermedia (many-to-many) entre Asignacion y Seccion
asignacion_seccion = Table(
    "asignacion_seccion",
    Base.metadata,
    Column("asignacion_id", Integer, ForeignKey("asignaciones.id"), primary_key=True),
    Column("seccion_id", Integer, ForeignKey("seccion.id"), primary_key=True)
)

