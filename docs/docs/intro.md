---
sidebar_position: 1
slug: /intro
---

# Introduction

**UpKeep** is an AI-driven predictive maintenance platform for industrial robots.
It turns robot telemetry pushed from external systems into health insights, early
warnings, and explainable maintenance recommendations.

This documentation is the single home for the UpKeep product documentation. It is
written in English by default; additional locales can be enabled later through
Docusaurus internationalization.

## What UpKeep does

- Ingests time-series telemetry from external providers over a simple HTTP API.
- Normalizes vendor-specific payloads into a vendor-neutral internal model.
- Recognizes robot operating states and process phases.
- Detects anomalies and degradation patterns against configurable rules.
- Produces maintenance recommendations with traceable evidence.
- Captures operator and engineer feedback for future tuning.

## Where to go next

- New to the project? Start with the [Quickstart](./getting-started/quickstart.md).
- Want the big picture? Read the [Architecture](./concepts/architecture.md).
- Integrating a system? See the [API Reference](./api/overview.md).
- Looking for product context? Read the [Business Brief](./product/business-brief.md).

## Documentation conventions

- All pages are authored in Markdown or MDX under `docs/docs/`.
- Sidebar order comes from `sidebar_position` front matter and `_category_.json`.
- Code samples use fenced blocks with a language hint for syntax highlighting.
- Every recommendation shown in the docs must be traceable to source telemetry.
