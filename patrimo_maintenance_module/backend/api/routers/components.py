from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.base import get_db
from backend.models import models
from ..schemas import ComponentInDB, ComponentCreate, ComponentUpdate

router = APIRouter(prefix="/components", tags=["components"])

@router.get("/", response_model=list[ComponentInDB])
def list_components(db: Session = Depends(get_db)):
    return db.query(models.Component).all()

@router.get("/{component_id}", response_model=ComponentInDB)
def get_component(component_id: int, db: Session = Depends(get_db)):
    comp = db.query(models.Component).filter(models.Component.id == component_id).first()
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Component not found")
    return comp

@router.post("/", response_model=ComponentInDB, status_code=status.HTTP_201_CREATED)
def create_component(payload: ComponentCreate, db: Session = Depends(get_db)):
    comp = models.Component(**payload.dict())
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp

@router.put("/{component_id}", response_model=ComponentInDB)
def update_component(component_id: int, payload: ComponentUpdate, db: Session = Depends(get_db)):
    comp = db.query(models.Component).filter(models.Component.id == component_id).first()
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Component not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(comp, key, value)
    db.commit()
    db.refresh(comp)
    return comp

@router.delete("/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_component(component_id: int, db: Session = Depends(get_db)):
    comp = db.query(models.Component).filter(models.Component.id == component_id).first()
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Component not found")
    db.delete(comp)
    db.commit()
    return None
