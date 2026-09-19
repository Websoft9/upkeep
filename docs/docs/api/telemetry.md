---
sidebar_position: 2
---

# Telemetry Ingest

`POST /api/v1/telemetry/ingest`

Accepts a telemetry record from an external provider, stores it, and evaluates
the [recommendation rules](../concepts/recommendation-rules.md) against the
payload.

## Request body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `source` | string | yes | External provider that pushed the data. Max 100 chars. |
| `robot_id` | string | yes | External robot identifier. Max 100 chars. |
| `robot_name` | string | no | Human-readable robot name. Max 200 chars. |
| `cell_name` | string | no | Work cell name. Max 200 chars. |
| `vendor` | string | no | Robot vendor. Max 100 chars. |
| `ts` | string | yes | Observation timestamp (ISO 8601). |
| `payload` | object | yes | Metric map evaluated by the rules. |

## Example request

```bash
curl -X POST http://127.0.0.1:8000/api/v1/telemetry/ingest \
  -H 'Content-Type: application/json' \
  -d '{
    "source": "demo-simulator",
    "robot_id": "robot-01",
    "robot_name": "Robot 01",
    "cell_name": "Cell A",
    "ts": "2026-09-19T04:20:00Z",
    "payload": {
      "temperature_c": 82,
      "vibration_mm_s": 8,
      "cycle_time_s": 79,
      "axis_load_pct": 72
    }
  }'
```

## Example response

```json
{
  "telemetry_id": 42,
  "recommendation_count": 2
}
```

`recommendation_count` is the number of rules that fired for this record. Query
`GET /api/v1/recommendations` to read them.

## Notes

- Each call creates a new telemetry record; the endpoint is not idempotent.
- Unknown payload keys are stored but do not trigger rules unless a matching rule
  exists.
- The payload is preserved as received to keep recommendations traceable.
