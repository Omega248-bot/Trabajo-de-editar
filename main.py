import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse  # Importante

from database import db
from vistas import router as vistas_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_qgvYbXeI78EM@ep-patient-math-apihp7g4-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )
    await db.connect(database_url)
    yield
    await db.close()


app = FastAPI(lifespan=lifespan)

# Ruta para la raíz / que redirige a /productos
@app.get("/")
async def raiz():
    return RedirectResponse(url="/productos")

app.include_router(vistas_router)