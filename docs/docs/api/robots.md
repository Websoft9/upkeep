---
sidebar_position: 3
---

# Robots

`GET /api/v1/robots`

Returns the known robots with aggregate counts and the latest observation time.

## Response

```json
[
  {
    "robot_id": "robot-01",
    "robot_name": "Robot 01",
    "cell_name": "Cell A",
    "vendor": "Acme Robotics",
    "telemetry_count": 128,
    "recommendation_count": 4,
    "latest_observed_at": "2026-09-19T04:20:00Z"
  }
]
```

| Field | Type | Description |
| --- | --- | --- |
| `robot_id` | string | External robot identifier. |
| `robot_name` | string \| null | Human-readable name. |
| `cell_name` | string \| null | Work cell name. |
| `vendor` | string \| null | Robot vendor. |
| `telemetry_count` | integer | Number of stored telemetry records. |
| `recommendation_count` | integer | Number of recommendations for the robot. |
| `latest_observed_at` | string \| null | Timestamp of the newest telemetry record. |

Results are ordered by `robot_id` ascending.
