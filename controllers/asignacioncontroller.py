from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db as get_async_db
import services.asignacionservice as asignacion_service
import schemas.asignacion as asignacion_schema
from services.asignacionservice import recalcular_horas_docente
from typing import List
from utils.google_auth import get_current_user
from models.AsignacionCursoDocente import AsignacionCursoDocente 

router = APIRouter(
    prefix="/asignaciones",
    tags=["Asignaciones"]
)


@router.post("/", response_model=asignacion_schema.AsignacionResponse)
async def create_asignacion(
    asignacion: asignacion_schema.AsignacionCreate,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await asignacion_service.create_asignacion(db, asignacion)


@router.get("/", response_model=List[asignacion_schema.AsignacionResponse])
async def get_asignaciones(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await asignacion_service.get_asignaciones(db, skip, limit)


@router.get("/{asignacion_id}", response_model=asignacion_schema.AsignacionResponse)
async def get_asignacion(
    asignacion_id: int,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    db_asignacion = await asignacion_service.get_asignacion(db, asignacion_id)
    if not db_asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return db_asignacion


@router.put("/{asignacion_id}", response_model=asignacion_schema.AsignacionResponse)
async def update_asignacion(
    asignacion_id: int,
    asignacion: asignacion_schema.AsignacionUpdate,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    db_asignacion = await asignacion_service.update_asignacion(db, asignacion_id, asignacion)
    if not db_asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return db_asignacion


@router.patch("/{asignacion_id}/secciones", response_model=asignacion_schema.AsignacionResponse)
async def update_asignacion_secciones(
    asignacion_id: int,
    update: asignacion_schema.AsignacionUpdateSecciones,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    db_asignacion = await asignacion_service.update_asignacion_secciones(db, asignacion_id, update)
    if not db_asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return db_asignacion


@router.delete("/{asignacion_id}", response_model=asignacion_schema.AsignacionResponse)
async def delete_asignacion(
    asignacion_id: int,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    db_asignacion = await asignacion_service.delete_asignacion(db, asignacion_id)
    if not db_asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    return db_asignacion


@router.patch("/{asignacion_id}/cursos", response_model=List[asignacion_schema.AsignacionCursoDocenteResponse])
async def actualizar_cursos(
    asignacion_id: int,
    data: asignacion_schema.CursosUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    return await asignacion_service.actualizar_cursos_asignacion(db, asignacion_id, data.curso_ids)


@router.post("/relacion", response_model=asignacion_schema.AsignacionCursoDocenteResponse)
async def add_asignacion_curso_docente(
    relacion: asignacion_schema.AsignacionCursoDocenteCreate,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    return await asignacion_service.add_asignacion_curso_docente(db, relacion)


@router.get("/{asignacion_id}/relaciones", response_model=List[asignacion_schema.AsignacionCursoDocenteResponse])
async def get_asignacion_curso_docentes(
    asignacion_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    return await asignacion_service.get_asignacion_curso_docentes(db, asignacion_id)


@router.patch("/{asignacion_id}/estado", response_model=asignacion_schema.AsignacionResponse)
async def cambiar_estado_asignacion(
    asignacion_id: int,
    data: dict,
    db: AsyncSession = Depends(get_async_db),
    user: dict = Depends(get_current_user)
):
    if "estado" not in data:
        raise HTTPException(status_code=400, detail="El campo 'estado' es requerido")

    estado_value = data["estado"]

    if isinstance(estado_value, str):
        estado_value = estado_value.lower() in ["true", "1", "yes"]
    elif isinstance(estado_value, int):
        estado_value = bool(estado_value)

    asignacion = await asignacion_service.update_asignacion_estado(db, asignacion_id, estado_value)
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    return asignacion


@router.patch("/{asignacion_id}/relaciones/docente", response_model=asignacion_schema.AsignacionCursoDocenteResponse)
async def actualizar_docente(
    asignacion_id: int,
    data: asignacion_schema.DocenteUpdate,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    relacion = await asignacion_service.update_docente_curso_asignacion(
        db, asignacion_id, data.curso_id, data.seccion, data.docente_id
    )
    if not relacion:
        raise HTTPException(status_code=404, detail="No se encontró la relación asignación-curso-sección")
    return relacion


@router.delete("/{asignacion_id}/secciones/{seccion}")
async def delete_seccion_asignacion(
    asignacion_id: int,
    seccion: int,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    result = await asignacion_service.delete_seccion_asignacion(db, asignacion_id, seccion)
    if not result:
        raise HTTPException(status_code=404, detail="No se encontraron relaciones para esa sección")
    return result


@router.put("/recalcular/{docente_id}", response_model=dict)
async def endpoint_recalcular_horas(
    docente_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    docente = await recalcular_horas_docente(db, docente_id)
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return {
        "id": docente.id,
        "nombre": docente.nombre,
        "horasactual": docente.horasactual,
        "horastemporales": docente.horastemporales,
    }


@router.patch("/relaciones/{relacion_id}", response_model=asignacion_schema.AsignacionCursoDocenteResponse)
async def actualizar_relacion(
    relacion_id: int,
    data: asignacion_schema.AsignacionCursoDocenteUpdate,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    relacion = await db.get(AsignacionCursoDocente, relacion_id)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(relacion, field, value)

    await db.commit()
    await db.refresh(relacion)
    return relacion


@router.patch("/relaciones/{relacion_id}/activar", response_model=asignacion_schema.AsignacionCursoDocenteResponse)
async def activar_bloque_relacion(
    relacion_id: int,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    relacion = await asignacion_service.activar_bloque(db, relacion_id)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return relacion


@router.patch("/relaciones/{relacion_id}/comentario", response_model=asignacion_schema.AsignacionCursoDocenteResponse)
async def actualizar_comentario_y_disponibilidad(
    relacion_id: int,
    data: asignacion_schema.AsignacionCursoDocenteComentarioUpdate,
    db: AsyncSession = Depends(get_async_db),
    dict = Depends(get_current_user)
):
    relacion = await asignacion_service.actualizar_comentario_disponibilidad(db, relacion_id, data)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return relacion


@router.put("/relaciones/{relacion_id}/desactivar-bloque")
async def desactivar_bloque(
    relacion_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    relacion = await db.get(AsignacionCursoDocente, relacion_id)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")

    relacion.activo = False
    await db.commit()
    await db.refresh(relacion)
    return {"id": relacion.id, "activo": relacion.activo}
