from datetime import datetime, timezone

import click
import typer

from app.database import SessionLocal, init_db
from app.models import Recommendation, Robot
from app.schemas import TelemetryIngestRequest
from app.services import ingest_telemetry, seed_demo_data

HELP_OPTION_NAMES = {"help_option_names": ["-h", "--help"]}


def _show_help_when_no_command(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        raise typer.Exit()


app = typer.Typer(
    help="UpKeep command line interface.",
    context_settings=HELP_OPTION_NAMES,
)
robots_app = typer.Typer(
    help="Inspect robots.",
    context_settings=HELP_OPTION_NAMES,
)
recommendations_app = typer.Typer(
    help="Inspect recommendations.",
    context_settings=HELP_OPTION_NAMES,
)
app.callback(invoke_without_command=True)(_show_help_when_no_command)
robots_app.callback(invoke_without_command=True)(_show_help_when_no_command)
recommendations_app.callback(invoke_without_command=True)(_show_help_when_no_command)
app.add_typer(robots_app, name="robots")
app.add_typer(recommendations_app, name="recommendations")


@app.command("help")
def help_command(ctx: typer.Context) -> None:
    """Show the command list and exit."""
    click.echo(ctx.find_root().get_help())


def _with_db():
    init_db()
    return SessionLocal()


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Bind address."),
    port: int = typer.Option(8000, help="Bind port."),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload for development."),
) -> None:
    """Run the FastAPI application with uvicorn."""
    import uvicorn

    uvicorn.run("app.main:app", host=host, port=port, reload=reload)


@app.command()
def seed() -> None:
    """Seed demo robots, telemetry, and recommendations."""
    db = _with_db()
    try:
        result = seed_demo_data(db)
        typer.echo(
            f"seeded robots={result['robots_created']} "
            f"telemetry={result['telemetry_created']} "
            f"recommendations={result['recommendations_created']}"
        )
    finally:
        db.close()


@app.command()
def ingest(
    robot_id: str = typer.Option(..., help="External robot identifier."),
    source: str = typer.Option("cli", help="Telemetry source name."),
    robot_name: str = typer.Option(None, help="Human readable robot name."),
    cell_name: str = typer.Option(None, help="Work cell name."),
    vendor: str = typer.Option(None, help="Robot vendor."),
    temperature_c: float = typer.Option(None, help="Temperature in Celsius."),
    vibration_mm_s: float = typer.Option(None, help="Vibration in mm/s."),
    cycle_time_s: float = typer.Option(None, help="Cycle time in seconds."),
    axis_load_pct: float = typer.Option(None, help="Axis load percentage."),
) -> None:
    """Ingest a single telemetry sample from the command line."""
    payload = {
        key: value
        for key, value in {
            "temperature_c": temperature_c,
            "vibration_mm_s": vibration_mm_s,
            "cycle_time_s": cycle_time_s,
            "axis_load_pct": axis_load_pct,
        }.items()
        if value is not None
    }
    telemetry = TelemetryIngestRequest(
        source=source,
        robot_id=robot_id,
        robot_name=robot_name,
        cell_name=cell_name,
        vendor=vendor,
        ts=datetime.now(timezone.utc),
        payload=payload,
    )

    db = _with_db()
    try:
        record, recommendations = ingest_telemetry(db, telemetry)
        typer.echo(f"telemetry_id={record.id} recommendations={len(recommendations)}")
        for recommendation in recommendations:
            typer.echo(f"  - [{recommendation.risk_level}] {recommendation.recommendation_type}: {recommendation.message}")
    finally:
        db.close()


@robots_app.command("list")
def list_robots() -> None:
    """List known robots."""
    db = _with_db()
    try:
        rows = db.query(Robot).order_by(Robot.external_id.asc()).all()
        if not rows:
            typer.echo("no robots found")
            return
        for row in rows:
            typer.echo(
                f"{row.external_id}\tstatus={row.status or 'n/a'}\tvendor={row.vendor or 'n/a'}\t"
                f"model={row.model or 'n/a'}\tcell={row.cell_name or 'n/a'}\t"
                f"telemetry={len(row.telemetry_records)}\trecommendations={len(row.recommendations)}"
            )
    finally:
        db.close()


@robots_app.command("show")
def show_robot(robot_id: str = typer.Argument(..., help="External robot identifier.")) -> None:
    """Show metadata for a single robot."""
    db = _with_db()
    try:
        robot = db.query(Robot).filter(Robot.external_id == robot_id).first()
        if robot is None:
            typer.echo(f"robot '{robot_id}' not found")
            raise typer.Exit(code=1)
        typer.echo(f"id:               {robot.external_id}")
        typer.echo(f"name:             {robot.name or 'n/a'}")
        typer.echo(f"vendor:           {robot.vendor or 'n/a'}")
        typer.echo(f"model:            {robot.model or 'n/a'}")
        typer.echo(f"serial_number:    {robot.serial_number or 'n/a'}")
        typer.echo(f"controller_type:  {robot.controller_type or 'n/a'}")
        typer.echo(f"firmware_version: {robot.firmware_version or 'n/a'}")
        typer.echo(f"site:             {robot.site or 'n/a'}")
        typer.echo(f"line:             {robot.line or 'n/a'}")
        typer.echo(f"cell:             {robot.cell_name or 'n/a'}")
        typer.echo(f"status:           {robot.status or 'n/a'}")
        typer.echo(f"installed_at:     {robot.installed_at or 'n/a'}")
        typer.echo(f"telemetry:        {len(robot.telemetry_records)}")
        typer.echo(f"recommendations:  {len(robot.recommendations)}")
    finally:
        db.close()


@recommendations_app.command("list")
def list_recommendations() -> None:
    """List maintenance recommendations."""
    db = _with_db()
    try:
        rows = db.query(Recommendation).order_by(Recommendation.created_at.desc()).all()
        if not rows:
            typer.echo("no recommendations found")
            return
        for row in rows:
            typer.echo(f"[{row.risk_level}] {row.robot.external_id}\t{row.recommendation_type}\t{row.message}")
    finally:
        db.close()


if __name__ == "__main__":
    app()
