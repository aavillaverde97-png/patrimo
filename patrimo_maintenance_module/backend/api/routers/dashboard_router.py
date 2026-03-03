from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database.base import get_db
from backend.models import models
from backend.services import maintenance_service, financial_impact_service
from ..schemas import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary", response_model=DashboardSummary)
def summary(db: Session = Depends(get_db)):
    total_components = db.query(func.count(models.Component.id)).scalar() or 0

    # near end of life: remaining life <= 1 year
    comps = db.query(models.Component).all()
    nearing = 0
    high_risk = 0
    comp_scores = []
    comp_list_for_reserve = []
    for comp in comps:
        if comp.installation_date and comp.useful_life_years:
            remaining = maintenance_service.calculate_remaining_life(comp.installation_date, comp.useful_life_years)
            if remaining <= 1:
                nearing += 1
        # risk score
        age = None
        if comp.installation_date:
            age = maintenance_service.calculate_component_age(comp.installation_date)
        failure_prob = financial_impact_service.failure_probability(age or 0, comp.useful_life_years or 1)
        score = financial_impact_service.calculate_component_risk_score(comp.criticality or 0, failure_prob)
        comp_scores.append(score)
        if score > 0.7:
            high_risk += 1
        comp_list_for_reserve.append({
            "replacement_cost": comp.replacement_cost,
            "useful_life_years": comp.useful_life_years,
        })

    total_annual_reserve = financial_impact_service.calculate_annual_reserve(comp_list_for_reserve)
    # for simplicity, estimated value impact treat as reserve * some factor 1.1
    estimated_value_impact = total_annual_reserve * 1.1

    return DashboardSummary(
        total_components=total_components,
        nearing_end_of_life=nearing,
        high_risk_components=high_risk,
        total_annual_reserve=total_annual_reserve,
        estimated_value_impact=estimated_value_impact,
    )
