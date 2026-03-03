from fastapi import APIRouter, HTTPException, Query
from app.services.excel_service import get_propietario, calcular_noi_mensual
from app.services.financiero_service import (
    calcular_noi_ajustado,
    calcular_valor_capitalizacion,
    calcular_valor_descuento_flujos,
    proyectar_flujos,
)
from app.services.dolar_service import get_dolar
from app.models.schemas import ValuacionResponse

router = APIRouter(prefix="/valuacion", tags=["valuacion"])


@router.get("/{propietario_id}", response_model=ValuacionResponse)
def valuacion(
    propietario_id: str,
    tasa_cap: float            = Query(default=0.04, description="Tasa de capitalización"),
    tasa_descuento: float      = Query(default=0.06, description="Tasa de descuento DCF"),
    fondo_mantenimiento: float = Query(default=0.0,  description="Reserva mensual ARS"),
    horizonte_anios: int       = Query(default=10,   description="Años proyección DCF"),
    crecimiento_renta: float   = Query(default=0.03, description="Crecimiento anual renta"),
):
    prop = get_propietario(propietario_id)
    if not prop:
        raise HTTPException(404, detail=f"Propietario '{propietario_id}' no encontrado")

    noi_mensual  = calcular_noi_mensual(propietario_id)
    noi_anual    = noi_mensual * 12
    noi_ajustado = calcular_noi_ajustado(noi_anual, fondo_mantenimiento * 12)

    valor_cap = calcular_valor_capitalizacion(noi_ajustado, tasa_cap)
    flujos    = proyectar_flujos(noi_ajustado, crecimiento_renta, horizonte_anios)
    valor_dcf = calcular_valor_descuento_flujos(flujos, tasa_descuento)

    tc = get_dolar()["promedio"]

    return ValuacionResponse(
        propietario_id             = propietario_id,
        nombre                     = str(prop.get("nombre", "")),
        noi_mensual                = round(noi_mensual, 2),
        noi_anual                  = round(noi_anual, 2),
        noi_ajustado_anual         = round(noi_ajustado, 2),
        valor_capitalizacion_ars   = round(valor_cap, 2),
        valor_descuento_flujos_ars = round(valor_dcf, 2),
        dolar_blue                 = tc,
        valor_capitalizacion_usd   = round(valor_cap / tc, 2),
        valor_descuento_flujos_usd = round(valor_dcf / tc, 2),
    )
