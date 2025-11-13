from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db as get_db
import services.docenteservice as docente_service
from schemas.docente import DocenteCreate, DocenteUpdate, DocenteOut
from typing import List
from utils.google_auth import get_current_user

router = APIRouter(prefix="/api/docentes", tags=["Docentes"])

@router.get("/", response_model=List[DocenteOut])
async def listar(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    return await docente_service.listar_docentes(db)

@router.get("/{docente_id}", response_model=DocenteOut)
async def obtener(docente_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    docente = await docente_service.obtener_docente(db, docente_id)
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return docente

@router.post("/", response_model=DocenteOut)
async def crear(docente: DocenteCreate, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    return await docente_service.crear_docente(db, docente)

@router.put("/{docente_id}", response_model=DocenteOut)
async def actualizar(docente_id: int, docente: DocenteUpdate, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    actualizado = await docente_service.actualizar_docente(db, docente_id, docente)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return actualizado

@router.delete("/{docente_id}", response_model=DocenteOut)
async def eliminar(docente_id: int, db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    eliminado = await docente_service.eliminar_docente(db, docente_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return eliminado
