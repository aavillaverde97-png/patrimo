import openpyxl
from app.config import EXCEL_PATH


def _libro():
    return openpyxl.load_workbook(EXCEL_PATH, data_only=True)


def _hoja_a_lista(nombre_hoja: str) -> list[dict]:
    """Convierte una hoja en lista de dicts usando la primera fila como headers."""
    wb = _libro()
    ws = wb[nombre_hoja]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [
        str(h).strip() if h is not None else f"col_{i}"
        for i, h in enumerate(rows[0])
    ]
    return [
        dict(zip(headers, row))
        for row in rows[1:]
        if any(v is not None for v in row)
    ]


# ── AJUSTAR estas 3 constantes con tus headers exactos ──────────────────
PROP_ID_COL    = "id"            # columna ID en hoja propietarios
ING_FK_COL     = "propietario_id"  # columna FK en hoja ingresos
ING_MONTO_COL  = "monto"         # columna de monto en hoja ingresos
# ────────────────────────────────────────────────────────────────────────


def get_todos_propietarios() -> list[dict]:
    return _hoja_a_lista("propietarios")


def get_propietario(propietario_id: str) -> dict | None:
    for p in get_todos_propietarios():
        if str(p.get(PROP_ID_COL, "")).strip() == str(propietario_id).strip():
            return p
    return None


def get_ingresos_propietario(propietario_id: str) -> list[dict]:
    return [
        r for r in _hoja_a_lista("ingresos")
        if str(r.get(ING_FK_COL, "")).strip() == str(propietario_id).strip()
    ]


def calcular_noi_mensual(propietario_id: str) -> float:
    """Promedia los montos de ingresos del propietario."""
    montos = []
    for i in get_ingresos_propietario(propietario_id):
        v = i.get(ING_MONTO_COL)
        if v is not None:
            try:
                montos.append(
                    float(str(v).replace("$", "").replace(",", "").strip())
                )
            except (ValueError, TypeError):
                pass
    return sum(montos) / len(montos) if montos else 0.0


def get_todos_administradores() -> list[dict]:
    return _hoja_a_lista("administradores")
