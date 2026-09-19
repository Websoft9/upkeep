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
uk seed
```

Open `http://127.0.0.1:8000/` for the UI and `http://127.0.0.1:8000/docs` for the Swagger UI.

## CLI

The backend ships a [Typer](https://typer.tiangolo.com/) CLI, installed as the
`upkeep` command with `uk` as a short alias. It covers local ops and inspection
tasks:

```bash
upkeep serve --reload        # run the FastAPI app
upkeep seed                  # seed demo data
upkeep ingest --robot-id robot-01 --temperature-c 84 --vibration-mm-s 9
upkeep robots list           # list known robots
upkeep recommendations list  # list maintenance recommendations

uk seed                      # the same CLI through the short alias
```

Show the command list with `upkeep`, `upkeep help`, `upkeep -h`, or `upkeep --help`.
Run `upkeep <command> --help` for command details.

The commands only resolve on `PATH` after the virtual environment is activated:

```bash
source .venv/bin/activate
```

To make them available everywhere without activating the venv, link them onto
your `PATH`:

```bash
make link-cli      # symlink upkeep and uk into /usr/local/bin
make unlink-cli    # remove the symlinks
```

Override the target directory with `BIN_DIR`, for example
`make link-cli BIN_DIR=$$HOME/.local/bin`.

To run the CLI through Make instead, pass arguments with `ARGS`:

```bash
make cli                     # show the command list
make cli ARGS="robots list"  # run any CLI command
make cli ARGS="seed"
```

`make cli` and `make link-cli` bootstrap the virtual environment on first use.

### Database location

By default the SQLite database lives at `<repo>/upkeep.db` regardless of the
current directory, so the CLI and API always share the same data. Override it
with `UPKEEP_DATABASE_URL`:

```bash
UPKEEP_DATABASE_URL="sqlite:////tmp/upkeep.db" upkeep robots list
```

## Next.js Frontend

The repository also includes a product-oriented frontend in `web/`.

Create a frontend env file:

```bash
cp web/.env.example web/.env.local
```

Install and run:

```bash
make web-install
make web-run
```

Open `http://127.0.0.1:3000/` for the Next.js UI.

The frontend expects the FastAPI backend to be running on `http://127.0.0.1:8000` by default.

### Run with Make

```bash
make api-install
make api-run
make web-install
make web-run
```

Override the port of any run target with `PORT` (or a per-service variable such as
`API_PORT`, `WEB_PORT`, `DOCS_PORT`):

```bash
make api-run PORT=8001
make web-run WEB_PORT=4000
```

Stop one service or all of them (kills whatever listens on the port):

```bash
make stop            # stop api, docs, and web
make stop api        # or: make stop web / make stop docs
make stop api PORT=8001
```

### Run with Docker

Container build files live in [`docker/`](./docker).

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

## Documentation

Product documentation lives in [`docs/`](./docs) and is built with
[Docusaurus](https://docusaurus.io/). It is authored in English by default.

```bash
make docs-install
make docs-run     # http://localhost:3000/upkeep/
make docs-build
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
