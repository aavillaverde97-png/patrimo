
from typing import Iterable


def calculate_monthly_reserve(replacement_cost: float, useful_life_years: int) -> float:
    return replacement_cost / (useful_life_years * 12)


def calculate_noi_adjusted(noi: float, monthly_reserve: float) -> float:
    return noi - (monthly_reserve * 12)


def calculate_property_value(noi_adjusted: float, cap_rate: float) -> float:
    return noi_adjusted / cap_rate


def failure_probability(current_age: int, useful_life_years: int) -> float:
    if useful_life_years <= 0:
        return 1.0
    return min(max(current_age / useful_life_years, 0.0), 1.0)


def calculate_component_risk_score(criticality: int, failure_prob: float) -> float:
    # simple weighted score
    return criticality * 0.6 + failure_prob * 0.4


def calculate_property_risk_score(component_scores: Iterable[float]) -> float:
    # average of component scores
    comp_list = list(component_scores)
    if not comp_list:
        return 0.0
    return sum(comp_list) / len(comp_list)


def adjust_noi_for_risk(noi: float, risk_score: float) -> float:
    # reduce NOI proportionally to risk (risk_score between 0-1)
    return noi * (1 - risk_score)


def calculate_annual_reserve(components: Iterable[dict]) -> float:
    # each component dict must have replacement_cost and useful_life_years
    total = 0.0
    for comp in components:
        rc = comp.get("replacement_cost", 0) or 0
        life = comp.get("useful_life_years", 1) or 1
        total += calculate_monthly_reserve(rc, life) * 12
    return total
