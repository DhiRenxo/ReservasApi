from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioDocenteCodigoUpdate
from datetime import datetime

def get_all(db: Session):
    return db.query(Usuario).all()

def get_by_id(db: Session, id: int):
    return db.query(Usuario).filter(Usuario.id == id).first()

def create(db: Session, data: UsuarioCreate):
    nuevo = Usuario(
        nombre=data.nombre,
        correo=data.correo,
        foto_url=data.foto_url,
        email_verificado=data.email_verificado,
        estado=data.estado,
        rolid=data.rolid,
        fechacreacion=datetime.utcnow()
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def update(db: Session, id: int, data: UsuarioUpdate):
    usuario = get_by_id(db, id)
    if usuario:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(usuario, key, value)
        usuario.fechaactualizacion = datetime.utcnow()
        db.commit()
        db.refresh(usuario)
    return usuario

def delete(db: Session, id: int):
    usuario = get_by_id(db, id)
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario

def actualizar_cod_docente_service(db: Session, usuario_id: int, datos: UsuarioDocenteCodigoUpdate):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 🔒 Verificar que el usuario tenga rol docente (ejemplo: rolid = 2)
    if usuario.rolid != 1:
        raise HTTPException(status_code=403, detail="Solo los usuarios con rol docente pueden tener un código docente")

    # Actualizar el código docente si se envía
    if datos.cod_docente:
        usuario.cod_docente = datos.cod_docente

    db.commit()
    db.refresh(usuario)
    return usuario