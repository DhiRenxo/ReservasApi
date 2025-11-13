from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # === Seguridad ===
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # === Base de Datos ===
    DATABASE_URL_ASYNC: str | None = None
    DATABASE_URL_SYNC: str | None = None

    # === Google Auth ===
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    ALLOWED_GOOGLE_DOMAIN: str = "continental.edu.pe"

    # === Envío de correos ===
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: str | None = None
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587

    # === Configuración del sistema ===
    RESERVA_TIEMPO_APROBACION_MAX_HORAS: int = 24
    DEFAULT_ADMIN_EMAIL: str | None = None

    # === Configuración general ===
    BACKEND_CORS_ORIGINS: str = "*"
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

settings = Settings()
