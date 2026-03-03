from typing import List


def calcular_noi_ajustado(noi: float, fondo_mantenimiento: float) -> float:
    """NOI ajustado = NOI - Fondo mantenimiento"""
    return noi - fondo_mantenimiento


def calcular_valor_capitalizacion(noi: float, tasa: float) -> float:
    """Valor = NOI / r"""
    if tasa <= 0:
        raise ValueError("La tasa debe ser mayor a 0")
    return noi / tasa


def calcular_valor_descuento_flujos(flujos: List[float], tasa: float) -> float:
    """VP = suma de CF_n / (1+r)^n"""
    if tasa <= 0:
        raise ValueError("La tasa debe ser mayor a 0")
    return sum(cf / (1 + tasa) ** (n + 1) for n, cf in enumerate(flujos))


def proyectar_flujos(
    noi_base: float, crecimiento: float, horizonte: int
) -> List[float]:
    """Genera flujos anuales proyectados con crecimiento constante."""
    return [noi_base * (1 + crecimiento) ** n for n in range(horizonte)]
