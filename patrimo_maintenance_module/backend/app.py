
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.database.base import init_db
from backend.api.routers import (
    properties as properties_router,
    components as components_router,
    maintenance as maintenance_router,
    inspections as inspections_router,
    import_router,
    dashboard_router,
)

app = FastAPI(title="Patrimo Maintenance API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # ensure database tables exist
    init_db()

# include routers
app.include_router(properties_router.router)
app.include_router(components_router.router)
app.include_router(maintenance_router.router)
app.include_router(inspections_router.router)
app.include_router(import_router.router)
app.include_router(dashboard_router.router)

@app.get("/health")
def health():
    return {"status": "Patrimo maintenance module running"}

# generic exception handler
@app.exception_handler(Exception)
def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )
