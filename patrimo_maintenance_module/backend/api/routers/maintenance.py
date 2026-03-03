from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.base import get_db
from backend.models import models
from backend.services import maintenance_service
from ..schemas import MaintenanceHistory, MaintenanceHistoryCreate, MaintenanceHistoryUpdate

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

@router.get("/", response_model=list[MaintenanceHistory])
def list_maintenance(db: Session = Depends(get_db)):
    return db.query(models.MaintenanceHistory).all()

@router.get("/{record_id}", response_model=MaintenanceHistory)
def get_maintenance(record_id: int, db: Session = Depends(get_db)):
    rec = db.query(models.MaintenanceHistory).filter(models.MaintenanceHistory.id == record_id).first()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return rec

@router.post("/", response_model=MaintenanceHistory, status_code=status.HTTP_201_CREATED)
def create_maintenance(payload: MaintenanceHistoryCreate, db: Session = Depends(get_db)):
    rec = models.MaintenanceHistory(**payload.dict())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

@router.put("/{record_id}", response_model=MaintenanceHistory)
def update_maintenance(record_id: int, payload: MaintenanceHistoryUpdate, db: Session = Depends(get_db)):
    rec = db.query(models.MaintenanceHistory).filter(models.MaintenanceHistory.id == record_id).first()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(rec, key, value)
    db.commit()
    db.refresh(rec)
    return rec

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_maintenance(record_id: int, db: Session = Depends(get_db)):
    rec = db.query(models.MaintenanceHistory).filter(models.MaintenanceHistory.id == record_id).first()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    db.delete(rec)
    db.commit()
    return None

@router.get("/upcoming/{days}", response_model=list[dict])
def upcoming_maintenance(days: int, db: Session = Depends(get_db)):
    """return list of components due for maintenance within `days` days"""
    comps = maintenance_service.get_upcoming_maintenance(db, days)
    # serialize minimal component info
    result = []
    for comp in comps:
        result.append({
            "id": comp.id,
            "name": comp.name,
            "property_id": comp.property_id,
        })
    return result
