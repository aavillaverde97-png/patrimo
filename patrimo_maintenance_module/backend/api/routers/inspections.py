from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.base import get_db
from backend.models import models
from ..schemas import Inspection, InspectionCreate, InspectionUpdate

router = APIRouter(prefix="/inspections", tags=["inspections"])

@router.get("/", response_model=list[Inspection])
def list_inspections(db: Session = Depends(get_db)):
    return db.query(models.Inspection).all()

@router.get("/{inspection_id}", response_model=Inspection)
def get_inspection(inspection_id: int, db: Session = Depends(get_db)):
    insp = db.query(models.Inspection).filter(models.Inspection.id == inspection_id).first()
    if not insp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspection not found")
    return insp

@router.post("/", response_model=Inspection, status_code=status.HTTP_201_CREATED)
def create_inspection(payload: InspectionCreate, db: Session = Depends(get_db)):
    insp = models.Inspection(**payload.dict())
    db.add(insp)
    db.commit()
    db.refresh(insp)
    return insp

@router.put("/{inspection_id}", response_model=Inspection)
def update_inspection(inspection_id: int, payload: InspectionUpdate, db: Session = Depends(get_db)):
    insp = db.query(models.Inspection).filter(models.Inspection.id == inspection_id).first()
    if not insp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspection not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(insp, key, value)
    db.commit()
    db.refresh(insp)
    return insp

@router.delete("/{inspection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inspection(inspection_id: int, db: Session = Depends(get_db)):
    insp = db.query(models.Inspection).filter(models.Inspection.id == inspection_id).first()
    if not insp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inspection not found")
    db.delete(insp)
    db.commit()
    return None
