from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(slots=True)
class OptimizationObjective:
    name: str
    weight: float


@dataclass(slots=True)
class Recommendation:
    recommendation_id: str
    recommendation_type: str
    description: str
    expected_benefit: str


@dataclass(slots=True)
class OptimizationRunResult:
    run_id: str
    score: float
    metrics: Dict[str, float] = field(default_factory=dict)
    recommendations: List[Recommendation] = field(default_factory=list)
