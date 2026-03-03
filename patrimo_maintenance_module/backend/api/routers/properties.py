from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.base import get_db
from backend.models import models
from ..schemas import Property, PropertyCreate, PropertyUpdate

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("/", response_model=list[Property])
def list_properties(db: Session = Depends(get_db)):
    return db.query(models.Property).all()

@router.get("/{property_id}", response_model=Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return prop

@router.post("/", response_model=Property, status_code=status.HTTP_201_CREATED)
def create_property(payload: PropertyCreate, db: Session = Depends(get_db)):
    prop = models.Property(**payload.dict())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop

@router.put("/{property_id}", response_model=Property)
def update_property(property_id: int, payload: PropertyUpdate, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(prop, key, value)
    db.commit()
    db.refresh(prop)
    return prop

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    db.delete(prop)
    db.commit()
    return None
