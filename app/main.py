from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys

# ================== Cargar variables de entorno ==================
load_dotenv(".env")

# ================== Routers ==================
from controllers.admin import (
    ambienteadmin, tipoambiente, roladmin, usuarioadmin,
    cursoadmin, horarioadmin, docenteadmin, carreraadmin, seccionadmin
)
from controllers import (
    authcontroller, asignacioncontroller,
    disponibilidadcontroller, emailcontroller
)

# ================== App FastAPI ==================
app = FastAPI(title="Sistema de Reservas de Ambientes")

# ================== Middleware ==================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== Routers ==================
app.include_router(ambienteadmin.router)
app.include_router(tipoambiente.router)
app.include_router(roladmin.router)
app.include_router(usuarioadmin.router)
app.include_router(authcontroller.router)
app.include_router(cursoadmin.router)
app.include_router(horarioadmin.router)
app.include_router(docenteadmin.router)
app.include_router(asignacioncontroller.router)
app.include_router(carreraadmin.router)
app.include_router(seccionadmin.router)
app.include_router(disponibilidadcontroller.router)
app.include_router(emailcontroller.router)

# ================== Paths ==================
# Añadir ruta raíz (opcional)
@app.get("/")
async def root():
    return {"message": "Sistema de Reservas de Ambientes funcionando"}

# ================== Path para scripts/migraciones (opcional) ==================
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
