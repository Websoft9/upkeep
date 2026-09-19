---
sidebar_position: 1
---

# Installation

UpKeep ships as a FastAPI backend with a static browser UI. It stores data in a
local SQLite database by default, so no external services are required for a
first run.

## Requirements

- Python 3.11 or newer
- `pip` and `venv` (bundled with Python)
- Optional: Docker, for the container workflow

## Install from source

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Then open:

- `http://127.0.0.1:8000/` for the browser UI
- `http://127.0.0.1:8000/docs` for the interactive Swagger UI
- `http://127.0.0.1:8000/health` for the health check

## Use the Make targets

The repository provides convenience targets:

```bash
make api-install   # create the venv and install dependencies
make api-run       # run the FastAPI development server
make api-seed      # seed demo telemetry and recommendations
```

## Run with Docker

```bash
make docker-build  # build the upkeep:dev image
make docker-run    # run the container on port 8000
```

## Configuration

Settings are loaded from the environment via `pydantic-settings`. See
`app/config.py` for the available options. The SQLite file defaults to
`upkeep.db` in the working directory.
