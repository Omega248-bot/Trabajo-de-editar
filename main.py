import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import db
from vistas import router as vistas_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Obtiene la cadena de conexión desde la variable de entorno DATABASE_URL
    database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_qgvYbXeI78EM@ep-patient-math-apihp7g4-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )
    # Al arrancar la aplicación se crea el pool de conexiones a PostgreSQL.
    await db.connect(database_url)
    yield
    # Al apagar la aplicación, el pool se cierra para liberar las conexiones.
    await db.close()


app = FastAPI(lifespan=lifespan)

app.include_router(vistas_router)