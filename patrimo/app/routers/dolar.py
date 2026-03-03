from fastapi import APIRouter, HTTPException
from app.services.dolar_service import get_dolar
from app.models.schemas import DolarResponse

router = APIRouter(prefix="/dolar", tags=["dolar"])


@router.get("", response_model=DolarResponse)
def dolar():
    """Devuelve tipo de cambio USD/ARS blue desde caché."""
    try:
        return get_dolar()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
