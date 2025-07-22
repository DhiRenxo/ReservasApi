from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.rol import RolCreate, RolResponse
from services import rolservice
from utils.google_auth import get_current_user 

router = APIRouter(prefix="/api/roles", tags=["Roles"])

@router.get("/", response_model=list[RolResponse])
def listar(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return rolservice.get_all(db)

@router.get("/{id}", response_model=RolResponse)
def obtener(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    rol = rolservice.get_by_id(db, id)
    if not rol:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return rol

@router.post("/", response_model=RolResponse)
def crear(data: RolCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return rolservice.create(db, data)

