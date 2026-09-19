---
sidebar_position: 2
---

# MVP PRD

## Product name

Robot Intelligence for Predictive Maintenance

## Goal

Deliver a first product version that turns industrial robot telemetry into
actionable maintenance insights for fixed robot cells.

## Target user

- Maintenance manager
- Reliability engineer
- Production engineer
- OEM or integrator service team

## Primary user problem

Robot data exists, but it is not converted into early warnings, clear diagnosis,
or practical maintenance actions.

## MVP outcome

Users can identify robot health risks earlier, understand why a risk was
triggered, and decide what maintenance action to take.

## Scope

- Robot asset and work cell modeling
- Ingestion of time-series data pushed from external systems
- Normalization of telemetry into a common internal model
- State recognition for robot operating phases
- Anomaly and degradation detection
- Maintenance recommendation generation
- Operator or engineer feedback capture

## Out of scope

- Edge data acquisition product
- Direct robot control
- Autonomous closed-loop maintenance actions
- Full CMMS or MES replacement
- Support for every industrial asset type

## Core use cases

1. A maintenance engineer views the health status of robots in a cell.
2. A reliability engineer reviews abnormal trends in cycle time, load, vibration,
   or temperature.
3. A service engineer receives a maintenance recommendation with supporting
   evidence.
4. A user confirms, dismisses, or annotates a recommendation for future learning.

## Functional modules

### 1. Asset modeling

- Define factory, line, cell, and robot
- Map robot to controller, tool, and key signals
- Define process or program context

### 2. Data ingestion

- Receive telemetry from external providers by API
- Validate payload structure and timestamps
- Map incoming signals to internal signal definitions

### 3. State recognition

- Classify robot activity into operating states
- Segment telemetry by process phase or cycle stage

### 4. Health and anomaly detection

- Calculate baseline and trend indicators
- Detect abnormal drift and repeated risk patterns
- Assign risk level and confidence

### 5. Recommendation engine

- Generate explainable maintenance recommendations
- Show likely cause, evidence, and suggested action

### 6. Feedback loop

- Allow users to confirm, reject, or comment on recommendations
- Store outcomes for later tuning and model improvement

## Key user flow

1. External system pushes robot telemetry into the platform.
2. The platform validates and normalizes the data.
3. The platform identifies the robot state or process phase.
4. The platform detects anomaly or degradation patterns.
5. The platform creates a recommendation with evidence.
6. The user reviews and records feedback.

## Core screens

- Robot fleet or cell overview
- Single robot detail page
- Anomaly and recommendation list
- Recommendation detail with evidence
- Feedback and review history

## Key data objects

Robot, Cell, Signal, Telemetry Record, State Segment, Health Score, Anomaly
Event, Recommendation, Feedback Record. See the
[Data Model](../concepts/data-model.md) for details.

## Success metrics

- Telemetry from target robots is ingested successfully
- Users can view robot health and abnormal events in one interface
- Each recommendation includes traceable evidence
- Users can provide structured feedback on recommendations
- Pilot users can identify maintenance issues earlier than their current workflow

## Assumptions

- Telemetry is available from an external provider
- The first deployment focuses on fixed industrial robots
- Users accept recommendation support without direct machine control

## Open questions

- Which robot use cases should be prioritized first
- What minimum signal set is guaranteed by the telemetry provider
- Whether the first deployment is single customer or multi-customer
- Whether work order integration is needed in the MVP or later
