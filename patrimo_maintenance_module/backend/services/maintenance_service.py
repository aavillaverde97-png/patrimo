
from datetime import date
from typing import Optional


def needs_preventive_maintenance(last_service_date: date, frequency_months: int) -> bool:
    delta = (date.today().year - last_service_date.year) * 12 + (date.today().month - last_service_date.month)
    return delta >= frequency_months


def calculate_component_age(installation_date: date) -> int:
    today = date.today()
    years = today.year - installation_date.year
    if (today.month, today.day) < (installation_date.month, installation_date.day):
        years -= 1
    return years


def calculate_remaining_life(installation_date: date, useful_life_years: int) -> int:
    age = calculate_component_age(installation_date)
    remaining = useful_life_years - age
    return remaining if remaining >= 0 else 0


def maintenance_alert_level(criticality: int,
                            remaining_life: int,
                            failure_probability: float) -> str:
    """Return LOW, MEDIUM or HIGH"""
    score = 0
    # weight: criticality 50%, remaining life 30%, failure prob 20%
    score += (criticality or 0) * 0.5
    score += (1 - (remaining_life / max(remaining_life, 1))) * 0.3
    score += (failure_probability or 0) * 0.2
    if score > 0.7:
        return "HIGH"
    elif score > 0.4:
        return "MEDIUM"
    else:
        return "LOW"


def get_upcoming_maintenance(db, days_ahead: int):
    """Query components whose next scheduled maintenance falls within days_ahead"""
    from sqlalchemy import func
    from ..models import models

    today = date.today()
    target = today.replace(day=today.day)  # dummy to satisfy linters
    # simplistic: we examine maintenance_history to find last service date
    sub = db.query(models.MaintenanceHistory.component_id,
                   func.max(models.MaintenanceHistory.date).label("last_date"))
    sub = sub.group_by(models.MaintenanceHistory.component_id).subquery()
    comps = db.query(models.Component).outerjoin(
        sub, models.Component.id == sub.c.component_id
    ).all()
    upcoming = []
    for comp in comps:
        last_date = None
        if comp.maintenance_history:
            last_date = max(m.date for m in comp.maintenance_history)
        else:
            last_date = comp.installation_date
        if last_date:
            next_due = last_date
            # add frequency months
            import datetime
            month = next_due.month - 1 + (comp.maintenance_frequency_months or 0)
            year = next_due.year + month // 12
            month = month % 12 + 1
            day = min(next_due.day, 28)
            next_due = datetime.date(year, month, day)
            delta = (next_due - today).days
            if 0 <= delta <= days_ahead:
                upcoming.append(comp)
    return upcoming
