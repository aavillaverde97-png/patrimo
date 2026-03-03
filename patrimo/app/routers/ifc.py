from fastapi import APIRouter
from app.models.schemas import IfcElementResponse, ValuacionResponse
from app.services.excel_service import get_propietario, calcular_noi_mensual
from app.services.financiero_service import (
    calcular_noi_ajustado,
    calcular_valor_capitalizacion,
    calcular_valor_descuento_flujos,
    proyectar_flujos,
)
from app.services.dolar_service import get_dolar

router = APIRouter(prefix="/ifc-element", tags=["ifc"])

# ── Mapa GUID IFC → propietario_id ──────────────────────────────────────
# Completar con los GUIDs reales que aparecen en el viewer al clickear
IFC_PROPIETARIO_MAP: dict[str, str] = {
    # "3qiAqfncb8c8muWH37BaDC": "1",
}
# ────────────────────────────────────────────────────────────────────────


@router.get("/{element_id}", response_model=IfcElementResponse)
def ifc_element(element_id: str):
    propietario_id = IFC_PROPIETARIO_MAP.get(element_id)
    financiero = None

    if propietario_id:
        prop     = get_propietario(propietario_id)
        noi_m    = calcular_noi_mensual(propietario_id)
        noi_a    = noi_m * 12
        noi_aj   = calcular_noi_ajustado(noi_a, 0)
        val_cap  = calcular_valor_capitalizacion(noi_aj, 0.04)
        flujos   = proyectar_flujos(noi_aj, 0.03, 10)
        val_dcf  = calcular_valor_descuento_flujos(flujos, 0.06)
        tc       = get_dolar()["promedio"]

        financiero = ValuacionResponse(
            propietario_id             = propietario_id,
            nombre                     = str(prop.get("nombre", "")) if prop else "",
            noi_mensual                = round(noi_m, 2),
            noi_anual                  = round(noi_a, 2),
            noi_ajustado_anual         = round(noi_aj, 2),
            valor_capitalizacion_ars   = round(val_cap, 2),
            valor_descuento_flujos_ars = round(val_dcf, 2),
            dolar_blue                 = tc,
            valor_capitalizacion_usd   = round(val_cap / tc, 2),
            valor_descuento_flujos_usd = round(val_dcf / tc, 2),
        )

    return IfcElementResponse(
        element_id  = element_id,
        propiedades = {
            "id":     element_id,
            "mapeado": propietario_id is not None,
        },
        financiero = financiero,
    )
