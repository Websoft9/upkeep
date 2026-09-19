# High-Level Architecture

## Purpose

Define the minimum architecture needed to support the MVP for industrial robot predictive maintenance.

## Architecture Goal

Receive robot telemetry from external systems, turn it into normalized machine context, detect health risks, generate maintenance recommendations, and capture user feedback.

## Core Principles

- telemetry is pushed in from external providers
- the platform does not control robots
- the internal model stays vendor-neutral
- rules, skills, and models remain separate
- every recommendation must be traceable to source data
- the design must support future expansion to more robot types and vendors

## System Layers

### 1. Ingestion Layer

Responsibilities:

- receive telemetry and event payloads
- validate timestamps, schema, and source identity
- map vendor-specific payloads into a common structure

### 2. Data Layer

Responsibilities:

- store raw telemetry
- store normalized telemetry and state segments
- store anomaly events, recommendations, and feedback
- preserve traceability between raw data and derived outputs

### 3. Intelligence Layer

Responsibilities:

- recognize robot operating states
- calculate baseline and trend features
- detect anomalies and degradation patterns
- trigger diagnostic skills
- generate explainable recommendations

### 4. Application Layer

Responsibilities:

- present fleet and robot-level views
- present anomalies and recommendations
- allow users to review and submit feedback

### 5. Governance Layer

Responsibilities:

- enforce read-only operational behavior
- track rule, skill, and model versions
- maintain auditability for recommendations and feedback

## High-Level Data Flow

1. An external system pushes telemetry into the ingestion layer.
2. The platform validates and normalizes the incoming payload.
3. Normalized telemetry is stored and linked to the robot and cell model.
4. State recognition assigns operating context to the data.
5. Detection logic identifies abnormal patterns or degradation signals.
6. The recommendation engine creates a maintenance suggestion with evidence.
7. The application layer presents results to the user.
8. User feedback is captured and stored for later tuning.

## Core Services

- Ingestion API
- Signal Mapping Service
- Asset Modeling Service
- State Recognition Service
- Health and Anomaly Service
- Recommendation Service
- Feedback Service
- Audit Service

## Core Data Domains

- Assets
- Signals
- Raw Telemetry
- Normalized Telemetry
- State Segments
- Health Scores
- Anomaly Events
- Recommendations
- Feedback Records

## External Interfaces

The MVP should expose or support:

- telemetry ingest API
- asset configuration interface
- recommendation review interface
- feedback capture interface

Future integrations may include:

- CMMS or work order systems
- MES or production systems
- additional robot vendors or telemetry providers

## MVP Boundary

The architecture is designed for one focused use case: fixed industrial robot cells with externally supplied telemetry. It should be modular enough to expand later, but simple enough to deliver quickly.
