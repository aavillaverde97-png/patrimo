from pydantic import BaseModel
from typing import Optional


class DolarResponse(BaseModel):
    compra: float
    venta: float
    promedio: float
    ultima_actualizacion: str


class ValuacionResponse(BaseModel):
    propietario_id: str
    nombre: Optional[str]
    noi_mensual: float
    noi_anual: float
    noi_ajustado_anual: float
    valor_capitalizacion_ars: float
    valor_descuento_flujos_ars: float
    dolar_blue: float
    valor_capitalizacion_usd: float
    valor_descuento_flujos_usd: float


class IfcElementResponse(BaseModel):
    element_id: str
    propiedades: dict
    financiero: Optional[ValuacionResponse] = None
