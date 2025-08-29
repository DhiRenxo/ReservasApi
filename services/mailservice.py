# services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

from sqlalchemy.orm import Session
from models.usuario import Usuario
from models.docente import Docente
from models.AsignacionCursoDocente import AsignacionCursoDocente


class EmailService:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def enviar_email(self, destinatarios: List[str], asunto: str, mensaje: str):
        # Configurar el mensaje
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = ", ".join(destinatarios)
        msg['Subject'] = asunto
        msg.attach(MIMEText(mensaje, 'plain'))

        # Conexión al servidor SMTP
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, destinatarios, msg.as_string())


def obtener_correos_docentes(db: Session, asignacion_id: int) -> list[str]:
    # Buscar los docentes asignados a esta asignación
    docentes_asignados = db.query(AsignacionCursoDocente).filter(
        AsignacionCursoDocente.asignacion_id == asignacion_id
    ).all()

    correos = []
    for asignacion in docentes_asignados:
        docente = db.query(Docente).filter(Docente.id == asignacion.docente_id).first()
        if docente:
            # Buscar usuario con ese nombre y rol docente
            usuario = db.query(Usuario).filter(
                Usuario.nombre == docente.nombre,
                Usuario.rolid == 1  # rol docente
            ).first()
            if usuario:
                correos.append(usuario.correo)
    return correos