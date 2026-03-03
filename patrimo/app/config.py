import os
from dotenv import load_dotenv

load_dotenv()

EXCEL_PATH          = os.getenv("EXCEL_PATH", "data/Central.xlsx")
IFC_PATH            = os.getenv("IFC_PATH",   "data/modelo.ifc")
DOLAR_API_URL       = "https://dolarapi.com/v1/dolares/blue"
DOLAR_REFRESH_HORAS = 6
