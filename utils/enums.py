from enum import Enum

class RolUsuario(str, Enum):
    DOCENTE = "DOCENTE"
    COORDINADOR = "COORDINADOR"
    SOPORTETI = "SOPORTE DE TI"
    PROGRAMACION = "PROGRAMACION"
    ADMINISTRADOR = "ADMINISTRADOR"

class EstadoReserva(str, Enum):
    PENDIENTE = "PENDIENTE"
    APROBADA = "APROBADA"
    RECHAZADA = "RECHAZADA"

class EstadoAprobacion(str, Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
