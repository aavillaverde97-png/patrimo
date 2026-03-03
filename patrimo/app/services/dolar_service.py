import httpx
from datetime import datetime
from app.config import DOLAR_API_URL

_cache: dict = {}


async def actualizar_dolar() -> None:
    """Llama a la API y guarda en caché. Ejecutado al inicio y por scheduler."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(DOLAR_API_URL)
            r.raise_for_status()
            d = r.json()
            _cache.update({
                "compra":  float(d["compra"]),
                "venta":   float(d["venta"]),
                "promedio": round(
                    (float(d["compra"]) + float(d["venta"])) / 2, 2
                ),
                "ultima_actualizacion": datetime.now().isoformat(),
            })
    except Exception as e:
        print(f"[dolar_service] Error actualizando: {e}")


def get_dolar() -> dict:
    """Devuelve el valor en caché. Nunca llama a la API directamente."""
    if not _cache:
        raise RuntimeError(
            "Tipo de cambio no disponible aún. Reintentar en segundos."
        )
    return _cache
