import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ================= Async (App) =================
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL_ASYNC = os.getenv("DATABASE_URL_ASYNC")

# Engine async para la app
engine_async = create_async_engine(
    DATABASE_URL_ASYNC,
    echo=False,
    future=True
)

# Session async
AsyncSessionLocal = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

# Base declarativa para async
BaseAsync = declarative_base()

# Dependency async para FastAPI
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

# ================= Sync (Migraciones) =================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL_SYNC = os.getenv("DATABASE_URL_SYNC")

# Engine sync para migraciones
engine_sync = create_engine(
    DATABASE_URL_SYNC,
    echo=False,
    future=True
)

# Session sync
SessionLocal = sessionmaker(
    bind=engine_sync,
    autocommit=False,
    autoflush=False
)

# Base declarativa para sync
BaseSync = declarative_base()

# Dependency sync (opcional)
def get_db_sync():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
