---
sidebar_position: 4
---

# Recommendations

`GET /api/v1/recommendations`

Returns all maintenance recommendations, newest first.

## Response

```json
[
  {
    "id": 7,
    "robot_id": "robot-01",
    "recommendation_type": "temperature_c",
    "risk_level": "medium",
    "message": "Inspect cooling or load conditions. Temperature is above the initial operating threshold.",
    "evidence": {
      "metric": "temperature_c",
      "observed": 82,
      "threshold": 80,
      "telemetry_id": 42
    },
    "created_at": "2026-09-19T04:20:01Z"
  }
]
```

| Field | Type | Description |
| --- | --- | --- |
| `id` | integer | Recommendation identifier. |
| `robot_id` | string | External robot identifier. |
| `recommendation_type` | string | Metric that triggered the recommendation. |
| `risk_level` | string | `medium` or `high` in the MVP. |
| `message` | string | Explainable, actionable description. |
| `evidence` | object | Observed value, threshold, and source telemetry id. |
| `created_at` | string | Creation timestamp (ISO 8601). |

## Evidence and traceability

Every recommendation carries the evidence needed to reproduce it: the metric, the
observed value, the threshold, and the originating telemetry record. This keeps
recommendations auditable and lets users decide whether to act.

## Demo data

`POST /api/v1/demo/seed` creates demo robots, telemetry, and recommendations:

```json
{
  "robots_created": 3,
  "telemetry_created": 30,
  "recommendations_created": 6
}
```
