# UpKeep

AI-driven predictive maintenance.

## API Skeleton

The repository now includes a minimal FastAPI backend and static frontend that support:

- health check
- telemetry ingest
- robot listing
- recommendation listing
- demo data seeding
- browser-based UI

### Run locally

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Seed demo data:

```bash
python -m app.seed
```

Open `http://127.0.0.1:8000/` for the UI and `http://127.0.0.1:8000/docs` for the Swagger UI.

### Run with Make

```bash
make api-install
make api-run
```

### Run with Docker

```bash
make docker-build
make docker-run
```

### Example ingest payload

```json
{
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
}
```

## Development

Run `make help` to list the available targets.

### opencode

```bash
make opencode
```

Launches the [opencode](https://opencode.ai) TUI with every proxy environment
variable (`http_proxy`, `https_proxy`, `all_proxy`, `NO_PROXY`, ...) stripped, so
the session talks to the model providers directly instead of through the shell's
proxy. Extra CLI flags can be forwarded:

```bash
make opencode ARGS="--model anthropic/claude-sonnet-4-5"
```
