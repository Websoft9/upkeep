from dataclasses import dataclass


@dataclass(frozen=True)
class RecommendationRule:
    metric: str
    threshold: float
    risk_level: str
    message: str


DEFAULT_RULES = [
    RecommendationRule(
        metric="temperature_c",
        threshold=80,
        risk_level="medium",
        message="Inspect cooling or load conditions. Temperature is above the initial operating threshold.",
    ),
    RecommendationRule(
        metric="vibration_mm_s",
        threshold=12,
        risk_level="high",
        message="Inspect mechanical wear, mounting stability, or end-effector condition. Vibration is above the initial operating threshold.",
    ),
    RecommendationRule(
        metric="cycle_time_s",
        threshold=75,
        risk_level="medium",
        message="Review cycle drift and upstream or downstream dependencies. Cycle time is above the initial operating threshold.",
    ),
    RecommendationRule(
        metric="axis_load_pct",
        threshold=90,
        risk_level="high",
        message="Inspect joint load, tooling, or program path. Axis load is above the initial operating threshold.",
    ),
]
