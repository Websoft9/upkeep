from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, init_db
from app.models import Recommendation, Robot
from app.schemas import HealthResponse, RecommendationResponse, RobotResponse, SeedResponse, TelemetryIngestRequest, TelemetryIngestResponse
from app.services import ingest_telemetry as ingest_telemetry_record, seed_demo_data


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title=settings.app_title, version=settings.app_version)
init_db()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/v1/telemetry/ingest", response_model=TelemetryIngestResponse)
def ingest_telemetry(telemetry: TelemetryIngestRequest, db: Session = Depends(get_db)) -> TelemetryIngestResponse:
    record, recommendations = ingest_telemetry_record(db, telemetry)
    return TelemetryIngestResponse(
        telemetry_id=record.id,
        recommendation_count=len(recommendations),
    )


@app.get("/api/v1/robots", response_model=list[RobotResponse])
def list_robots(db: Session = Depends(get_db)) -> list[RobotResponse]:
    rows = db.query(Robot).order_by(Robot.external_id.asc()).all()
    return [
        RobotResponse(
            robot_id=row.external_id,
            robot_name=row.name,
            cell_name=row.cell_name,
            vendor=row.vendor,
            telemetry_count=len(row.telemetry_records),
            recommendation_count=len(row.recommendations),
            latest_observed_at=max((record.observed_at for record in row.telemetry_records), default=None),
        )
        for row in rows
    ]


@app.get("/api/v1/recommendations", response_model=list[RecommendationResponse])
def list_recommendations(db: Session = Depends(get_db)) -> list[RecommendationResponse]:
    rows = db.query(Recommendation).order_by(Recommendation.created_at.desc()).all()
    return [
        RecommendationResponse(
            id=row.id,
            robot_id=row.robot.external_id,
            recommendation_type=row.recommendation_type,
            risk_level=row.risk_level,
            message=row.message,
            evidence=row.evidence,
            created_at=row.created_at,
        )
        for row in rows
    ]


@app.post("/api/v1/demo/seed", response_model=SeedResponse)
def seed_demo(db: Session = Depends(get_db)) -> SeedResponse:
    result = seed_demo_data(db)
    return SeedResponse(**result)
