from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.routers import dolar, valuacion, ifc
from app.services.dolar_service import actualizar_dolar
from app.config import DOLAR_REFRESH_HORAS

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Carga inicial del dólar al arrancar
    await actualizar_dolar()
    # Refresca cada N horas
    scheduler.add_job(
        actualizar_dolar,
        "interval",
        hours=DOLAR_REFRESH_HORAS,
        id="dolar_refresh",
    )
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="Pátrimo API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(dolar.router)
app.include_router(valuacion.router)
app.include_router(ifc.router)

# Sirve el frontend desde /frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/health")
def health():
    return {"status": "ok", "app": "Pátrimo API v0.1"}
