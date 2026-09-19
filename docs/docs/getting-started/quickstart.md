---
sidebar_position: 2
---

# Quickstart

This walkthrough takes you from a fresh install to a maintenance recommendation
in a few minutes.

## 1. Start the API

```bash
make api-run
```

The server listens on `http://127.0.0.1:8000`.

## 2. Seed demo data

In a second terminal:

```bash
make api-seed
```

Seeding creates a demo robot, telemetry records, and recommendations so the UI
has something to show.

## 3. Push telemetry

Send a telemetry record with `curl`:

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

The response reports the stored telemetry id and how many recommendations were
generated:

```json
{
  "telemetry_id": 42,
  "recommendation_count": 2
}
```

## 4. Inspect the results

List robots:

```bash
curl http://127.0.0.1:8000/api/v1/robots
```

List recommendations:

```bash
curl http://127.0.0.1:8000/api/v1/recommendations
```

## 5. Use the browser UI

Open `http://127.0.0.1:8000/` to view the fleet, robot details, and
recommendations in a single page.

## Next steps

- Understand the detection thresholds in
  [Recommendation Rules](../concepts/recommendation-rules.md).
- Read the [API Reference](../api/overview.md) before building an integration.
