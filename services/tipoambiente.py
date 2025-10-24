from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.tipoambiente import TipoAmbiente
from schemas.tiposambiente import TipoAmbienteCreate

# Obtener todos los tipos de ambiente
async def get_all(db: AsyncSession):
    result = await db.execute(select(TipoAmbiente))
    return result.scalars().all()

# Obtener tipo de ambiente por ID
async def get_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(TipoAmbiente).filter(TipoAmbiente.id == id))
    return result.scalar_one_or_none()

# Crear nuevo tipo de ambiente
async def create(db: AsyncSession, tipo: TipoAmbienteCreate):
    nuevo = TipoAmbiente(**tipo.dict())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return nuevo
