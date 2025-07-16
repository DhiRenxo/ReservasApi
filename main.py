from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database import Base, engine
import os
import sys

# Routers
from controllers.admin import ambienteadmin, tipoambiente, roladmin, usuarioadmin, cursoadmin, horarioadmin, docenteadmin
from controllers import authcontroller,asignacioncontroller
# Aquí puedes agregar más routers si tienes

# Cargar variables de entorno
load_dotenv(".env")

app = FastAPI(title="Sistema de Reservas de Ambientes")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("BACKEND_CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas principales
app.include_router(ambienteadmin.router)
app.include_router(tipoambiente.router)
app.include_router(roladmin.router)
app.include_router(usuarioadmin.router)
app.include_router(authcontroller.router)
app.include_router(cursoadmin.router)
app.include_router(horarioadmin.router)
app.include_router(docenteadmin.router)
app.include_router(asignacioncontroller.router)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))



