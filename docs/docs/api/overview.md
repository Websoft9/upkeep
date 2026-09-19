---
sidebar_position: 1
---

# API Overview

The UpKeep backend is a FastAPI application. The interactive OpenAPI
documentation is served at `/docs`, and the raw schema at `/openapi.json`.

## Base URL

```
http://127.0.0.1:8000
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check. |
| `GET` | `/` | Browser UI. |
| `POST` | `/api/v1/telemetry/ingest` | Ingest a telemetry record and evaluate rules. |
| `GET` | `/api/v1/robots` | List robots with telemetry and recommendation counts. |
| `GET` | `/api/v1/recommendations` | List recommendations, newest first. |
| `POST` | `/api/v1/demo/seed` | Seed demo robots, telemetry, and recommendations. |

## Conventions

- All request and response bodies are JSON.
- Timestamps are ISO 8601 strings in UTC, for example `2026-09-19T04:20:00Z`.
- Identifiers such as `robot_id` are external, vendor-facing ids chosen by the
  telemetry provider.
- The API is read-only with respect to robots; it never issues control commands.

## Error handling

FastAPI returns standard validation errors with HTTP `422` for malformed bodies.
Unknown routes return HTTP `404`.

## Try it

- [Telemetry Ingest](./telemetry.md)
- [Robots](./robots.md)
- [Recommendations](./recommendations.md)
