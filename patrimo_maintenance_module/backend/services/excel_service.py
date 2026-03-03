import os
import pandas as pd
from sqlalchemy.orm import Session
from typing import Tuple

from ..models import models

REQUIRED_PROPERTY_COLUMNS = {"type", "address", "surface", "year_built"}
REQUIRED_COMPONENT_COLUMNS = {"property_id", "ifc_global_id", "name", "category", "installation_date", "useful_life_years", "replacement_cost", "criticality", "maintenance_frequency_months", "maintenance_type", "current_condition"}
REQUIRED_MAINTENANCE_COLUMNS = {"component_id", "date", "type", "description", "cost", "provider"}


def _validate_columns(df: pd.DataFrame, required: set[str]) -> None:
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")


def import_properties_from_excel(file_path: str, db: Session) -> int:
    df = pd.read_excel(file_path, sheet_name="properties")
    _validate_columns(df, REQUIRED_PROPERTY_COLUMNS)
    count = 0
    for _, row in df.iterrows():
        prop = models.Property(
            type=row["type"],
            address=row["address"],
            surface=row.get("surface"),
            year_built=row.get("year_built"),
        )
        db.add(prop)
        count += 1
    db.commit()
    return count


def import_components_from_excel(file_path: str, db: Session) -> int:
    df = pd.read_excel(file_path, sheet_name="components")
    _validate_columns(df, REQUIRED_COMPONENT_COLUMNS)
    count = 0
    for _, row in df.iterrows():
        comp = models.Component(
            property_id=row["property_id"],
            ifc_global_id=row.get("ifc_global_id"),
            name=row.get("name"),
            category=row.get("category"),
            installation_date=row.get("installation_date"),
            useful_life_years=row.get("useful_life_years"),
            replacement_cost=row.get("replacement_cost"),
            criticality=row.get("criticality"),
            maintenance_frequency_months=row.get("maintenance_frequency_months"),
            maintenance_type=row.get("maintenance_type"),
            current_condition=row.get("current_condition"),
        )
        db.add(comp)
        count += 1
    db.commit()
    return count


def import_maintenance_history_from_excel(file_path: str, db: Session) -> int:
    df = pd.read_excel(file_path, sheet_name="maintenance_history")
    _validate_columns(df, REQUIRED_MAINTENANCE_COLUMNS)
    count = 0
    for _, row in df.iterrows():
        rec = models.MaintenanceHistory(
            component_id=row["component_id"],
            date=row["date"],
            type=row.get("type"),
            description=row.get("description"),
            cost=row.get("cost"),
            provider=row.get("provider"),
        )
        db.add(rec)
        count += 1
    db.commit()
    return count
