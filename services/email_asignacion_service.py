from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.asignacion import Asignacion
from models.AsignacionCursoDocente import AsignacionCursoDocente
from services.mailservice import enviar_email

async def enviar_notificacion_asignacion(db, asignacion_id: int):

    # Obtener asignación
    asignacion_result = await db.execute(
        select(Asignacion).filter(Asignacion.id == asignacion_id)
    )
    asignacion = asignacion_result.scalar_one_or_none()

    if not asignacion:
        return {"error": "Asignación no encontrada"}

    fecha_inicio = asignacion.fecha_inicio.strftime("%d/%m/%Y") if asignacion.fecha_inicio else "Sin fecha definida"

    # Obtener docentes asignados
    query = await db.execute(
        select(AsignacionCursoDocente)
        .options(selectinload(AsignacionCursoDocente.docente))
        .filter(AsignacionCursoDocente.asignacion_id == asignacion_id)
        .filter(AsignacionCursoDocente.docente_id.isnot(None))
    )
    asignaciones = query.scalars().all()

    if not asignaciones:
        return {"error": "No hay docentes asignados"}

    # Agrupar correos y contar asignaciones
    correos_count = {}
    for item in asignaciones:
        docente = item.docente
        if docente and docente.correo:
            correo = docente.correo.lower()
            correos_count[correo] = correos_count.get(correo, 0) + 1

    resultados = []

    # Enviar correos
    for correo, count in correos_count.items():
        mensaje = (
            f"Estimado docente,\n\n"
            f"Ha sido asignado(a) a {count} curso(s).\n"
            f"Fecha de inicio: {fecha_inicio}\n\n"
            f"Por favor ingrese al sistema para completar su disponibilidad.\n\n"
            f"Saludos,\n"
            f"Coordinación Académica"
        )

        result = await enviar_email(
            destinatario=correo, 
            asunto="Notificación de asignación de cursos",
            mensaje=mensaje
        )
        resultados.append({correo: result})

    return {
        "asignacion_id": asignacion_id,
        "docentes_notificados": len(correos_count),
        "resultados": resultados
    }
