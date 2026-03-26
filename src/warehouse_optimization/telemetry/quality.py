from math import sqrt


def compute_uncertainty_2d(std_x: float, std_y: float) -> float:
    return sqrt((std_x**2) + (std_y**2))


def classify_uncertainty(uncertainty_2d: float) -> str:
    if uncertainty_2d <= 1.0:
        return "good"
    if uncertainty_2d <= 2.5:
        return "review"
    return "poor"


def usable_for_route_analysis(quality_status: str) -> bool:
    return quality_status != "poor"
