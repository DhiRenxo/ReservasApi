from google.oauth2 import id_token
from google.auth.transport import requests
from config import settings

def verificar_token_google(token_id: str):
    try:
        idinfo = id_token.verify_oauth2_token(token_id, requests.Request())


        #if settings.ALLOWED_GOOGLE_DOMAIN and idinfo.get("hd") != settings.ALLOWED_GOOGLE_DOMAIN:
        #    return None  

        return {
            "correo": idinfo["email"],
            "nombre": idinfo.get("name", ""),
            "foto": idinfo.get("picture", ""),
            "verificado": idinfo.get("email_verified", False)
        }
    except Exception as e:
        print(" Token inválido:", e)
        return None
