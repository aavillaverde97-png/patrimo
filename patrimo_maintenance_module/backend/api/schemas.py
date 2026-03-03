from __future__ import annotations
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

# property schemas
class PropertyBase(BaseModel):
    type: Optional[str] = None
    address: Optional[str] = None
    surface: Optional[float] = None
    year_built: Optional[int] = None

class PropertyCreate(PropertyBase):
    type: str
    address: str

class PropertyUpdate(PropertyBase):
    pass

class ComponentInDB(BaseModel):
    id: int
    property_id: int
    ifc_global_id: Optional[str]
    name: Optional[str]
    category: Optional[str]
    installation_date: Optional[date]
    useful_life_years: Optional[int]
    replacement_cost: Optional[float]
    criticality: Optional[int]
    maintenance_frequency_months: Optional[int]
    maintenance_type: Optional[str]
    current_condition: Optional[str]

    class Config:
        orm_mode = True

class Property(PropertyBase):
    id: int
    components: List[ComponentInDB] = []

    class Config:
        orm_mode = True

# component schemas
class ComponentBase(BaseModel):
    property_id: int
    ifc_global_id: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    installation_date: Optional[date] = None
    useful_life_years: Optional[int] = None
    replacement_cost: Optional[float] = None
    criticality: Optional[int] = None
    maintenance_frequency_months: Optional[int] = None
    maintenance_type: Optional[str] = None
    current_condition: Optional[str] = None

class ComponentCreate(ComponentBase):
    property_id: int

class ComponentUpdate(ComponentBase):
    pass

class MaintenanceHistoryBase(BaseModel):
    component_id: int
    date: date
    type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    provider: Optional[str] = None

class MaintenanceHistoryCreate(MaintenanceHistoryBase):
    component_id: int
    date: date

class MaintenanceHistoryUpdate(MaintenanceHistoryBase):
    pass

class MaintenanceHistory(MaintenanceHistoryBase):
    id: int

    class Config:
        orm_mode = True

class InspectionBase(BaseModel):
    component_id: int
    date: date
    measured_variable: Optional[str] = None
    value: Optional[float] = None
    critical_threshold: Optional[float] = None
    result: Optional[str] = None

class InspectionCreate(InspectionBase):
    component_id: int
    date: date

class InspectionUpdate(InspectionBase):
    pass

class Inspection(InspectionBase):
    id: int

    class Config:
        orm_mode = True

# dashboard / import response schemas
class ImportSummary(BaseModel):
    properties: int = 0
    components: int = 0
    maintenance_records: int = 0

class DashboardSummary(BaseModel):
    total_components: int
    nearing_end_of_life: int
    high_risk_components: int
    total_annual_reserve: float
    estimated_value_impact: float
