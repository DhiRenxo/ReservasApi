import smtplib
from email.mime.text import MIMEText
from app.config import settings

async def enviar_email(destinatario: str, asunto: str, mensaje: str) -> str:
    try:
        msg = MIMEText(mensaje, "html", "utf-8")
        msg["Subject"] = asunto
        msg["From"] = settings.MAIL_FROM
        msg["To"] = destinatario

        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            server.starttls()
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.sendmail(settings.MAIL_FROM, destinatario, msg.as_string())

        return "✅ Enviado"
    except Exception as e:
        return f"❌ Error: {str(e)}"
