# MVP PRD

## Product Name

Robot Intelligence for Predictive Maintenance

## Goal

Deliver a first product version that turns industrial robot telemetry into actionable maintenance insights for fixed robot cells.

## Target User

- Maintenance manager
- Reliability engineer
- Production engineer
- OEM or integrator service team

## Primary User Problem

Robot data exists, but it is not converted into early warnings, clear diagnosis, or practical maintenance actions.

## MVP Outcome

Users can identify robot health risks earlier, understand why a risk was triggered, and decide what maintenance action to take.

## Scope

The MVP includes:

- robot asset and work cell modeling
- ingestion of time-series data pushed from external systems
- normalization of telemetry into a common internal model
- state recognition for robot operating phases
- anomaly and degradation detection
- maintenance recommendation generation
- operator or engineer feedback capture

## Out of Scope

- edge data acquisition product
- direct robot control
- autonomous closed-loop maintenance actions
- full CMMS or MES replacement
- support for every industrial asset type

## Core Use Cases

1. A maintenance engineer views the health status of robots in a cell.
2. A reliability engineer reviews abnormal trends in cycle time, load, vibration, or temperature.
3. A service engineer receives a maintenance recommendation with supporting evidence.
4. A user confirms, dismisses, or annotates a recommendation for future learning.

## Functional Modules

### 1. Asset Modeling

- define factory, line, cell, and robot
- map robot to controller, tool, and key signals
- define process or program context

### 2. Data Ingestion

- receive telemetry from external providers by API
- validate payload structure and timestamps
- map incoming signals to internal signal definitions

### 3. State Recognition

- classify robot activity into operating states
- segment telemetry by process phase or cycle stage

### 4. Health and Anomaly Detection

- calculate baseline and trend indicators
- detect abnormal drift and repeated risk patterns
- assign risk level and confidence

### 5. Recommendation Engine

- generate explainable maintenance recommendations
- show likely cause, evidence, and suggested action

### 6. Feedback Loop

- allow users to confirm, reject, or comment on recommendations
- store outcomes for later tuning and model improvement

## Key User Flow

1. External system pushes robot telemetry into the platform.
2. The platform validates and normalizes the data.
3. The platform identifies the robot state or process phase.
4. The platform detects anomaly or degradation patterns.
5. The platform creates a recommendation with evidence.
6. The user reviews and records feedback.

## Core Screens

- robot fleet or cell overview
- single robot detail page
- anomaly and recommendation list
- recommendation detail with evidence
- feedback and review history

## Key Data Objects

- Robot
- Cell
- Signal
- Telemetry Record
- State Segment
- Health Score
- Anomaly Event
- Recommendation
- Feedback Record

## Success Metrics

- telemetry from target robots is ingested successfully
- users can view robot health and abnormal events in one interface
- each recommendation includes traceable evidence
- users can provide structured feedback on recommendations
- pilot users can identify maintenance issues earlier than their current workflow

## Assumptions

- telemetry is available from an external provider
- the first deployment focuses on fixed industrial robots
- users accept recommendation support without direct machine control

## Open Questions

- which robot use cases should be prioritized first
- what minimum signal set is guaranteed by the telemetry provider
- whether first deployment is single customer or multi-customer
- whether work order integration is needed in the MVP or later
