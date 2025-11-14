from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.asignacion import Asignacion
from models.AsignacionCursoDocente import AsignacionCursoDocente
from models.usuario import Usuario
from services.mailservice import enviar_email
from datetime import datetime, timedelta


async def enviar_notificacion_asignacion(db, asignacion_id: int):

    asignacion_result = await db.execute(
        select(Asignacion).filter(Asignacion.id == asignacion_id)
    )
    asignacion = asignacion_result.scalar_one_or_none()

    if not asignacion:
        return {"error": "Asignación no encontrada"}

    fecha_inicio = (
        asignacion.fecha_inicio.strftime("%d/%m/%Y")
        if asignacion.fecha_inicio else "Sin fecha definida"
    )

    # FECHA LÍMITE = HOY + 3 DÍAS
    fecha_limite = (datetime.now() + timedelta(days=3)).strftime("%d/%m/%Y")

    query = await db.execute(
        select(AsignacionCursoDocente)
        .options(selectinload(AsignacionCursoDocente.docente))
        .filter(AsignacionCursoDocente.asignacion_id == asignacion_id)
        .filter(AsignacionCursoDocente.docente_id.isnot(None))
    )

    asignaciones = query.scalars().all()

    if not asignaciones:
        return {"error": "No hay docentes asignados"}

    correos_count = {}
    nombres_docente = {}

    for item in asignaciones:
        docente = item.docente
        if docente and docente.correo:
            correo = docente.correo.lower()
            correos_count[correo] = correos_count.get(correo, 0) + 1

            # 🔍 CONSULTAR NOMBRE EN TABLA USUARIO
            usuario_result = await db.execute(
                select(Usuario).filter(Usuario.correo == correo)
            )
            usuario = usuario_result.scalar_one_or_none()

            nombres_docente[correo] = usuario.nombre if usuario else "Docente"

    resultados = []

    def plantilla_asignacion(nombre, count, fecha_inicio, fecha_limite):
        return f"""
    <html>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif;">

    <div style="max-width:600px; margin:auto; padding:24px; background:#ffffff; 
                border-radius:12px; border:1px solid #e5e5e5; line-height:1.65;">

    <h2 style="color:#B00020; text-align:center; font-size:22px; margin-bottom:12px;">
    📢 ATENCIÓN DOCENTES: Actualice su disponibilidad para dictado de cursos
    </h2>

    <p>Estimado/a <strong>{nombre}</strong>,</p>

    <p>
    Reciba un cordial saludo de parte del equipo de <strong>Programación Académica IC</strong>.
    </p>

    <p>
    Le informamos que se le ha asignado <strong>{count} curso(s)</strong> con fecha de inicio 
    <strong>{fecha_inicio}</strong>. Para continuar con el proceso, solicitamos registrar su 
    <strong>disponibilidad horaria</strong> indicando modalidades, turnos y horarios de preferencia.
    </p>

    <div style="text-align:center; margin-top:28px;">
        <a href="http://localhost:4200"
        style="background:#B00020; color:#fff; padding:14px 28px;
                text-decoration:none; border-radius:6px; font-size:16px;
                font-weight:bold; display:inline-block;">
            ACCEDER AL APLICATIVO
        </a>
    </div>

    <p style="margin-top:22px;">
    📘 <strong>Guía de usuario:</strong> <a href="[ENLACE_GUIA]" style="color:#B00020;">Descargar aquí</a>
    </p>

    <p style="margin-top:18px;">
    ⏰ <strong>FECHA LÍMITE:</strong> <span style="color:#B00020; font-size:18px;"><strong>{fecha_limite}</strong></span>
    </p>
    <div style="margin-top:22px; padding:14px 18px; background:#FFF4E5; 
                border-left:5px solid #FF9800; border-radius:6px;">
        <p style="margin:0; color:#B00020; font-size:15px; line-height:1.5;">
            ⚠️ <strong>Importante:</strong>  
            Recuerde que después de la fecha límite deberá informar cualquier modificación 
            en su disponibilidad. De lo contrario, se asumirá que su disponibilidad es 
            <strong>todo el día.</strong>
        </p>
    </div>


    <p>
    Por favor verifique su información y guarde los cambios.
    </p>

    <p style="margin-top:28px;">
    ¿Consultas o problemas técnicos?<br>
    📩 <strong>pacademicaic@continental.edu.pe</strong><br>
    📞 <strong>997218559</strong><br>
    🕘 <strong>Institulo Continental Calle REAL #123 Lun - Vie: 9:00 am - 6:00 pm</strong>
    </p>

    <p style="margin-top:30px;">
    Atentamente,<br>
    <strong>Equipo de Programación Académica IC</strong>
    </p>

    </div>
    </body>
    </html>
"""


    for correo, count in correos_count.items():
        nombre = nombres_docente.get(correo, "Docente")
        mensaje = plantilla_asignacion(nombre, count, fecha_inicio, fecha_limite)

        result = await enviar_email(
            destinatario=correo,
            asunto="📢 ATENCIÓN DOCENTE: Registre su disponibilidad",
            mensaje=mensaje
        )
        resultados.append({correo: result})

    return {
        "asignacion_id": asignacion_id,
        "docentes_notificados": len(correos_count),
        "resultados": resultados
    }


# ============================================================
# CONFIRMACIÓN DE HORARIO
# ============================================================

async def enviar_confirmacion_horario(db, asignacion_id: int):

    asignacion_result = await db.execute(
        select(Asignacion).filter(Asignacion.id == asignacion_id)
    )
    asignacion = asignacion_result.scalar_one_or_none()

    if not asignacion:
        return {"error": "Asignación no encontrada"}

    query = await db.execute(
        select(AsignacionCursoDocente)
        .options(selectinload(AsignacionCursoDocente.docente))
        .filter(AsignacionCursoDocente.asignacion_id == asignacion_id)
        .filter(AsignacionCursoDocente.docente_id.isnot(None))
    )

    asignaciones = query.scalars().all()

    if not asignaciones:
        return {"error": "No hay docentes asignados"}

    correos = {}
    nombres_docente = {}

    for item in asignaciones:
        docente = item.docente
        if docente and docente.correo:
            correo = docente.correo.lower()
            correos[correo] = True

            # 🔍 OBTENER NOMBRE DESDE USUARIO
            usuario_result = await db.execute(
                select(Usuario).filter(Usuario.correo == correo)
            )
            usuario = usuario_result.scalar_one_or_none()
            nombres_docente[correo] = usuario.nombre if usuario else "Docente"

    resultados = []

    def plantilla_confirmacion(nombre):
        return f"""
    <html>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif;">

    <div style="max-width:600px; margin:auto; padding:24px; background:#ffffff;
                border-radius:12px; border:1px solid #e5e5e5; line-height:1.65;">

    <h2 style="color:#2E7D32; text-align:center; font-size:22px; margin-bottom:12px;">
    📘 Confirmación de carga horaria asignada
    </h2>

    <p>Estimado/a <strong>{nombre}</strong>,</p>

    <p>
    Su horario académico ha sido <strong>registrado y publicado exitosamente</strong>.
    </p>

    <div style="text-align:center; margin-top:28px;">
        <a href="[ENLACE HORARIO]"
        style="background:#2E7D32; color:#fff; padding:12px 24px; 
                text-decoration:none; border-radius:6px; font-size:16px;
                display:inline-block;">
            Consultar mi horario
        </a>
    </div>

    <p style="margin-top:28px;">
    ¿Consultas o problemas técnicos?<br>
    📩 <strong>[email de soporte]</strong><br>
    📞 <strong>[número de contacto]</strong><br>
    🕘 <strong>[horario de atención]</strong>
    </p>

    <p style="margin-top:30px;">
    Atentamente,<br>
    <strong>Equipo de Programación Académica IC</strong>
    </p>

    </div>
    </body>
    </html>
    """


    for correo in correos.keys():
        nombre = nombres_docente.get(correo, "Docente")
        mensaje = plantilla_confirmacion(nombre)

        result = await enviar_email(
            destinatario=correo,
            asunto="📘 Confirmación de carga horaria asignada",
            mensaje=mensaje
        )
        resultados.append({correo: result})

    return {
        "asignacion_id": asignacion_id,
        "docentes_notificados": len(correos),
        "resultados": resultados
    }
