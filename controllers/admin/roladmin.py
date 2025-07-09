from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.rol import RolCreate, RolResponse
from services import rolservice

router = APIRouter(prefix="/api/roles", tags=["Roles"])

@router.get("/", response_model=list[RolResponse])
def listar(db: Session = Depends(get_db)):
    return rolservice.get_all(db)

@router.post("/", response_model=RolResponse)
def crear(data: RolCreate, db: Session = Depends(get_db)):
    return rolservice.create(db, data)
