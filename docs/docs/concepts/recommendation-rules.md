---
sidebar_position: 3
---

# Recommendation Rules

The MVP uses a transparent, rule-based detector. Rules live in `app/rules.py` and
are evaluated on every ingested telemetry record. Each triggered rule produces a
recommendation with a risk level and an explainable message.

## Default rules

| Metric | Threshold | Risk level | Suggested action |
| --- | --- | --- | --- |
| `temperature_c` | `> 80` | medium | Inspect cooling or load conditions. |
| `vibration_mm_s` | `> 12` | high | Inspect mechanical wear, mounting stability, or end-effector condition. |
| `cycle_time_s` | `> 75` | medium | Review cycle drift and upstream or downstream dependencies. |
| `axis_load_pct` | `> 90` | high | Inspect joint load, tooling, or program path. |

## How a rule is defined

```python
@dataclass(frozen=True)
class RecommendationRule:
    metric: str
    threshold: float
    risk_level: str
    message: str
```

A rule compares a single metric in the telemetry payload against a threshold. If
the metric exceeds the threshold, UpKeep emits a recommendation that includes the
metric, the observed value, the threshold, and the risk level.

## Tuning guidance

- Thresholds are initial operating values, not tuned limits. Calibrate them per
  robot model and work cell before production use.
- Keep messages actionable and specific to a maintenance action.
- Prefer adding a new rule over widening an existing one when the underlying
  cause differs.
- Record user feedback so thresholds can be tuned from real outcomes.

## Roadmap

Future versions will combine rules with state recognition and statistical or
model-based detection, while keeping every recommendation explainable.
