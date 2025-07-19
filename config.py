import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    ALLOWED_GOOGLE_DOMAIN = "continental.edu.pe"

    # Envío de correos
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")

    # Reserva
    RESERVA_TIEMPO_APROBACION_MAX_HORAS = int(os.getenv("RESERVA_TIEMPO_APROBACION_MAX_HORAS", 24))
    DEFAULT_ADMIN_EMAIL = os.getenv("DEFAULT_ADMIN_EMAIL")

    # CORS
    BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", "").split(",")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

settings = Settings()
