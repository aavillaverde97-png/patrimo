from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil
import os
from tempfile import NamedTemporaryFile

from backend.database.base import get_db
from backend.services import excel_service
from ..schemas import ImportSummary

router = APIRouter(prefix="/import", tags=["import"])

@router.post("/excel", response_model=ImportSummary)
def import_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file type")
    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        props = excel_service.import_properties_from_excel(tmp_path, db)
        comps = excel_service.import_components_from_excel(tmp_path, db)
        maint = excel_service.import_maintenance_history_from_excel(tmp_path, db)
        return ImportSummary(properties=props, components=comps, maintenance_records=maint)
    finally:
        os.unlink(tmp_path)
