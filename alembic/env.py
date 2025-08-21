import os
import sys
from logging.config import fileConfig
from models.usuario import Usuario
from models.ambiente import Ambiente
from models.tipoambiente import TipoAmbiente  
from models.rol import Rol
from models.tipoevento import TipoEvento
from models.reserva import Reserva
from models.aprobacion import AprobacionReserva
from models.horario import HorarioAcademico
from models.eventoespecial import EventoEspecial
from models.bitacora import BitacoraReserva
from models.cursos import Curso
from models.docente import Docente
from models.carrera import Carrera
from models.seccion import Seccion
from models.asignacion import Asignacion
from models.AsignacionCursoDocente import AsignacionCursoDocente


from sqlalchemy import engine_from_config, pool
from alembic import context

# Añadir el path base del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Importar Base y modelos
from app.database import Base

# Configuración de Alembic
config = context.config

# Configurar logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata para autogenerar migraciones
target_metadata = Base.metadata

# Leer DATABASE_URL del .env
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("❌ DATABASE_URL no está definida en el archivo .env")

# Setear en la configuración de Alembic
config.set_main_option("sqlalchemy.url", database_url)

# Migraciones en modo offline
def run_migrations_offline() -> None:
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# Migraciones en modo online
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

# Ejecutar migraciones
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


