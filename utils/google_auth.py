from google.oauth2 import id_token
from google.auth.transport import requests
from config import settings
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()

def verificar_token_google(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        
        # Aquí se verifica el dominio
        email = idinfo.get("email")
        hd = idinfo.get("hd")  # hosted domain

        if settings.ALLOWED_GOOGLE_DOMAIN and hd != settings.ALLOWED_GOOGLE_DOMAIN:
            return None

        return {
            "correo": email,
            "nombre": idinfo.get("name"),
            "verificado": idinfo.get("email_verified"),
            "foto": idinfo.get("picture")
        }
    except Exception as e:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    # lo que ya tienes:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("id")
        email = payload.get("sub")
        rol = payload.get("rol")
        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido: información incompleta")
        return {"id": user_id, "email": email, "rol": rol}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
