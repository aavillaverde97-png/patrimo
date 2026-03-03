
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship

# reuse shared Base from database layer
from ..database.base import Base

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    address = Column(String)
    surface = Column(Numeric)
    year_built = Column(Integer)

    # relationships
    components = relationship("Component", back_populates="property", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Property(id={self.id}, type={self.type}, address={self.address})>"

class Component(Base):
    __tablename__ = "components"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), index=True)
    ifc_global_id = Column(String, index=True)
    name = Column(String)
    category = Column(String)
    installation_date = Column(Date)
    useful_life_years = Column(Integer)
    replacement_cost = Column(Numeric)
    criticality = Column(Integer)
    maintenance_frequency_months = Column(Integer)
    maintenance_type = Column(String)
    current_condition = Column(String)

    # relationships
    property = relationship("Property", back_populates="components")
    maintenance_history = relationship("MaintenanceHistory", back_populates="component", cascade="all, delete-orphan")
    inspections = relationship("Inspection", back_populates="component", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Component(id={self.id}, name={self.name}, property_id={self.property_id})>"

class MaintenanceHistory(Base):
    __tablename__ = "maintenance_history"
    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(Integer, ForeignKey("components.id", ondelete="CASCADE"), index=True)
    date = Column(Date, index=True)
    type = Column(String)
    description = Column(String)
    cost = Column(Numeric)
    provider = Column(String)

    # relationships
    component = relationship("Component", back_populates="maintenance_history")

    def __repr__(self):
        return f"<MaintenanceHistory(id={self.id}, component_id={self.component_id}, date={self.date})>"

class Inspection(Base):
    __tablename__ = "inspections"
    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(Integer, ForeignKey("components.id", ondelete="CASCADE"), index=True)
    date = Column(Date, index=True)
    measured_variable = Column(String)
    value = Column(Numeric)
    critical_threshold = Column(Numeric)
    result = Column(String)

    # relationships
    component = relationship("Component", back_populates="inspections")

    def __repr__(self):
        return f"<Inspection(id={self.id}, component_id={self.component_id}, date={self.date})>"
