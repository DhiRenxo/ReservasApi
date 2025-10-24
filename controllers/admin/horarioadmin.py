from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db as get_async_db
from schemas.horario import HorarioAcademicoCreate, HorarioAcademico
from services import horarioservice as horario_service
from utils.parser import extraer_horarios_de_texto
import fitz  # PyMuPDF
from typing import List

router = APIRouter(prefix="/horarios", tags=["Horarios"])


@router.post("/", response_model=HorarioAcademico)
async def crear(
    horario: HorarioAcademicoCreate,
    db: AsyncSession = Depends(get_async_db)
):
    return await horario_service.crear_horario(db, horario)


@router.get("/", response_model=List[HorarioAcademico])
async def listar(db: AsyncSession = Depends(get_async_db)):
    return await horario_service.listar_horarios(db)


@router.put("/{id}", response_model=HorarioAcademico)
async def actualizar(
    id: int,
    horario: HorarioAcademicoCreate,
    db: AsyncSession = Depends(get_async_db)
):
    return await horario_service.actualizar_horario(db, id, horario)


@router.delete("/{id}")
async def eliminar(id: int, db: AsyncSession = Depends(get_async_db)):
    return await horario_service.eliminar_horario(db, id)


@router.post("/upload-pdf", response_model=List[HorarioAcademico])
async def subir_pdf_y_convertir(
    archivo: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db)
):
    contenido = await archivo.read()
    texto = ""
    with fitz.open(stream=contenido, filetype="pdf") as pdf:
        for pagina in pdf:
            texto += pagina.get_text()

    registros = extraer_horarios_de_texto(texto, db)

    resultados = []
    for r in registros:
        try:
            obj = HorarioAcademicoCreate(**r)
            creado = await horario_service.crear_horario(db, obj)
            resultados.append(creado)
        except Exception as e:
            resultados.append({"error": str(e), "registro": r})

    return resultados
