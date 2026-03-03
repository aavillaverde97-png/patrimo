# Pátrimo — Setup

## Estructura
```
patrimo/
├── main.py
├── requirements.txt
├── data/
│   ├── Central.xlsx        ← tu Excel
│   └── modelo.ifc          ← tu archivo IFC
├── app/
│   ├── config.py
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── excel_service.py
│   │   ├── financiero_service.py
│   │   └── dolar_service.py
│   └── routers/
│       ├── dolar.py
│       ├── valuacion.py
│       └── ifc.py
└── frontend/
    ├── index.html
    └── viewer.js
```

## Setup

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Copiar archivos de datos
#    - Poner Central.xlsx en /data/
#    - Poner modelo.ifc en /data/

# 4. Correr el servidor
uvicorn main:app --reload
```

## Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | /health | Estado del servidor |
| GET | /dolar | Tipo de cambio blue (caché) |
| GET | /valuacion/{id} | Valuación completa del propietario |
| GET | /ifc-element/{id} | Propiedades IFC + datos financieros |

### Ejemplo valuación con parámetros
```
GET /valuacion/1?tasa_cap=0.04&fondo_mantenimiento=15000&horizonte_anios=10
```

## Ajustes obligatorios antes de correr

### 1. excel_service.py — líneas 20-22
Cambiar los nombres de columna por los headers exactos de tu Excel:
```python
PROP_ID_COL   = "id"             # columna ID en hoja propietarios
ING_FK_COL    = "propietario_id" # columna FK en hoja ingresos
ING_MONTO_COL = "monto"          # columna de monto en hoja ingresos
```

### 2. ifc.py — diccionario IFC_PROPIETARIO_MAP
Completar con los GUIDs del modelo IFC mapeados a IDs del Excel.
Los GUIDs aparecen en el panel del viewer al clickear cada elemento:
```python
IFC_PROPIETARIO_MAP = {
    "3qiAqfncb8c8muWH37BaDC": "1",
}
```

## Ver el frontend
Abrir http://localhost:8000 en el browser después de correr uvicorn.
Usar el botón "Cargar IFC" para abrir el modelo.
