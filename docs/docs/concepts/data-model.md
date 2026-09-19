---
sidebar_position: 2
---

# Data Model

UpKeep keeps a small, vendor-neutral set of objects. The MVP implementation
lives in `app/models.py` and `app/schemas.py`.

## Core objects

| Object | Description |
| --- | --- |
| Robot | A fixed industrial robot identified by an external id, with name, cell, and vendor. |
| Cell | The work cell a robot belongs to. |
| Signal | A named measurement mapped from a vendor payload to an internal definition. |
| Telemetry Record | A single time-stamped observation pushed by an external system. |
| State Segment | A window of telemetry classified into an operating state or phase. |
| Health Score | A derived indicator of robot health over a period. |
| Anomaly Event | A detected abnormal pattern or degradation signal. |
| Recommendation | An explainable maintenance suggestion with supporting evidence. |
| Feedback Record | A user's confirm, reject, or comment on a recommendation. |

## Telemetry record

In the MVP, a telemetry record carries:

- `source` — the external provider that pushed the data
- `robot_id` / `robot_name` — the robot the data belongs to
- `cell_name` — the work cell context
- `ts` — the observation timestamp
- `payload` — a metric map such as `temperature_c`, `vibration_mm_s`,
  `cycle_time_s`, and `axis_load_pct`

The payload is stored as received and later normalized into internal signal
definitions.

## Relationships

- A robot belongs to a cell and has many telemetry records.
- A robot has many recommendations.
- A recommendation is derived from one or more telemetry records and carries the
  evidence needed to trace it back to the source data.

## Extending the model

When adding a new signal or vendor, prefer adding a mapping in the ingestion
layer rather than special-casing the internal model. This keeps rules and models
vendor-neutral and reusable.
