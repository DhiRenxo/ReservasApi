from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from utils.google_auth import verificar_token_google
from utils.security import crear_token_acceso  
from schemas.token import TokenResponse, GoogleLoginRequest
from models.usuario import Usuario
from datetime import timedelta
from config import settings
from models.docente import Docente

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/google-login", response_model=TokenResponse)
def login_google(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    user_data = verificar_token_google(request.google_token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Token inválido o dominio no permitido.")

    usuario = db.query(Usuario).filter(Usuario.correo == user_data["correo"]).first()

    if not usuario:
        docente = db.query(Docente).filter(Docente.nombre == user_data["nombre"]).first()
        rol_id = 1 if docente else 6

        usuario = Usuario(
            nombre=user_data["nombre"],
            correo=user_data["correo"],
            estado=True,
            email_verificado=user_data["verificado"],
            foto_url=user_data["foto"],
            rolid=rol_id
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

    token = crear_token_acceso(
        data={"sub": usuario.correo, "id": usuario.id, "rol": usuario.rolid},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": token,
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rolid": usuario.rolid,
            "foto_url": usuario.foto_url
        }
    }