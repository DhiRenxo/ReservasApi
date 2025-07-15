from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.horario import HorarioAcademicoCreate, HorarioAcademico
from services import horarioservice as horario_service
from utils.parser import extraer_horarios_de_texto
import fitz  # PyMuPDF

router = APIRouter(prefix="/horarios", tags=["Horarios"])

@router.post("/", response_model=HorarioAcademico)
def crear(horario: HorarioAcademicoCreate, db: Session = Depends(get_db)):
    return horario_service.crear_horario(db, horario)

@router.get("/", response_model=list[HorarioAcademico])
def listar(db: Session = Depends(get_db)):
    return horario_service.listar_horarios(db)

@router.put("/{id}", response_model=HorarioAcademico)
def actualizar(id: int, horario: HorarioAcademicoCreate, db: Session = Depends(get_db)):
    return horario_service.actualizar_horario(db, id, horario)

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    return horario_service.eliminar_horario(db, id)

@router.post("/upload-pdf", response_model=list[HorarioAcademico])
def subir_pdf_y_convertir(archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    contenido = archivo.file.read()
    texto = ""
    with fitz.open(stream=contenido, filetype="pdf") as pdf:
        for pagina in pdf:
            texto += pagina.get_text()

    registros = extraer_horarios_de_texto(texto, db)

    resultados = []
    for r in registros:
        try:
            obj = HorarioAcademicoCreate(**r)
            creado = horario_service.crear_horario(db, obj)
            resultados.append(creado)
        except Exception as e:
            resultados.append({"error": str(e), "registro": r})

    return resultados
