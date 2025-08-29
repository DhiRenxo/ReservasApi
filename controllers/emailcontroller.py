from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from services.mailservice import EmailService, obtener_correos_docentes

router = APIRouter(prefix="/api/email", tags=["Email"])

# Configuración de tu administrador
SMTP_SERVER = "smtp.continental.edu.pe"
SMTP_PORT = 587
ADMIN_EMAIL = "75838996@continental.edu.pe"
ADMIN_PASSWORD = "nrps romb lbhb eepq"

email_service = EmailService(SMTP_SERVER, SMTP_PORT, ADMIN_EMAIL, ADMIN_PASSWORD)

@router.post("/enviar-asignacion/{asignacion_id}")
def enviar_email_asignacion(asignacion_id: int, asunto: str, mensaje: str, db: Session = Depends(get_db)):
    destinatarios = obtener_correos_docentes(db, asignacion_id)
    if not destinatarios:
        return {"msg": "No se encontraron docentes para esta asignación."}
    
    email_service.enviar_email(destinatarios, asunto, mensaje)
    return {"msg": f"Correo enviado a {len(destinatarios)} docente(s)."}
