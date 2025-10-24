from google.oauth2 import id_token
from google.auth.transport import requests
from config import settings
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()

# ✅ Mantiene compatibilidad con async
async def verificar_token_google(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        email = idinfo.get("email")
        hd = idinfo.get("hd")   # Dominio (solo si es G Suite)
        
        # ✅ Validación opcional
        if settings.ALLOWED_GOOGLE_DOMAIN:
            if hd != settings.ALLOWED_GOOGLE_DOMAIN:
                return None

        return {
            "correo": email,
            "nombre": idinfo.get("name"),
            "verificado": idinfo.get("email_verified"),
            "foto": idinfo.get("picture"),
        }
    
    except ValueError:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id: int = payload.get("id")
        email: str = payload.get("sub")
        rol: str = payload.get("rol")

        if not email or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: sin usuario"
            )

        return {"id": user_id, "email": email, "rol": rol}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado o inválido"
        )
