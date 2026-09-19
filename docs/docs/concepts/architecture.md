---
sidebar_position: 1
---

# Architecture

UpKeep is organized into layers that keep ingestion, storage, intelligence, and
presentation concerns separate. The platform never controls robots; it is a
read-only intelligence layer over telemetry supplied by external systems.

## Design principles

- Telemetry is pushed in from external providers.
- The platform does not control robots.
- The internal model stays vendor-neutral.
- Rules, skills, and models remain separate and versioned.
- Every recommendation is traceable to its source data.
- The design supports future expansion to more robot types and vendors.

## Layers

### Ingestion layer

Receives telemetry and event payloads, validates timestamps, schema, and source
identity, and maps vendor-specific payloads into a common structure.

### Data layer

Stores raw telemetry, normalized telemetry and state segments, anomaly events,
recommendations, and feedback. It preserves traceability between raw data and
derived outputs.

### Intelligence layer

Recognizes robot operating states, computes baseline and trend features, detects
anomalies and degradation patterns, triggers diagnostic skills, and generates
explainable recommendations.

### Application layer

Presents fleet and robot-level views, lists anomalies and recommendations, and
lets users review and submit feedback.

### Governance layer

Enforces read-only operational behavior, tracks rule, skill, and model versions,
and maintains auditability for recommendations and feedback.

## Data flow

1. An external system pushes telemetry into the ingestion layer.
2. The platform validates and normalizes the payload.
3. Normalized telemetry is stored and linked to the robot and cell model.
4. State recognition assigns operating context to the data.
5. Detection logic identifies abnormal patterns or degradation signals.
6. The recommendation engine creates a maintenance suggestion with evidence.
7. The application layer presents results to the user.
8. User feedback is captured and stored for later tuning.

## Core services

- Ingestion API
- Signal Mapping Service
- Asset Modeling Service
- State Recognition Service
- Health and Anomaly Service
- Recommendation Service
- Feedback Service
- Audit Service

## MVP boundary

The architecture targets one focused use case: fixed industrial robot cells with
externally supplied telemetry. It is modular enough to expand later and simple
enough to deliver quickly.
