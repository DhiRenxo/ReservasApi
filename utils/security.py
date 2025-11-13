from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings
from typing import Optional, Dict, Any

def crear_token_acceso(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    # Datetime en UTC con zona horaria explícita (mejor estándar)
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Se copia la info del usuario dentro del payload
    to_encode = {**data, "exp": expire}

    # Se agrega subject (email) si no lo trae
    if "sub" not in to_encode and "email" in data:
        to_encode["sub"] = data["email"]

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token
