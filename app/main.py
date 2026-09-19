from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, init_db
from app.models import Recommendation
from app.schemas import (
    HealthResponse,
    RecommendationResponse,
    RobotCreate,
    RobotDetailResponse,
    RobotResponse,
    RobotUpdate,
    SeedResponse,
    TelemetryIngestRequest,
    TelemetryIngestResponse,
    TelemetryRecordResponse,
)
from app.services import (
    create_robot,
    get_robot,
    ingest_telemetry as ingest_telemetry_record,
    list_robots as list_robots_service,
    recent_telemetry,
    robot_detail,
    robot_summary,
    seed_demo_data,
    update_robot,
)


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
    return TelemetryIngestResponse(telemetry_id=record.id, recommendation_count=len(recommendations))


@app.get("/api/v1/robots", response_model=list[RobotResponse])
def list_robots(db: Session = Depends(get_db)) -> list[RobotResponse]:
    return [RobotResponse(**robot_summary(row)) for row in list_robots_service(db)]


@app.post("/api/v1/robots", response_model=RobotDetailResponse, status_code=status.HTTP_201_CREATED)
def register_robot(payload: RobotCreate, db: Session = Depends(get_db)) -> RobotDetailResponse:
    try:
        robot = create_robot(db, payload)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return RobotDetailResponse(**robot_detail(robot))


@app.get("/api/v1/robots/{robot_id}", response_model=RobotDetailResponse)
def read_robot(robot_id: str, db: Session = Depends(get_db)) -> RobotDetailResponse:
    robot = get_robot(db, robot_id)
    if robot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="robot not found")
    return RobotDetailResponse(**robot_detail(robot))


@app.patch("/api/v1/robots/{robot_id}", response_model=RobotDetailResponse)
def edit_robot(robot_id: str, payload: RobotUpdate, db: Session = Depends(get_db)) -> RobotDetailResponse:
    robot = get_robot(db, robot_id)
    if robot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="robot not found")
    robot = update_robot(db, robot, payload)
    return RobotDetailResponse(**robot_detail(robot))


@app.get("/api/v1/robots/{robot_id}/telemetry", response_model=list[TelemetryRecordResponse])
def read_robot_telemetry(
    robot_id: str,
    limit: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[TelemetryRecordResponse]:
    robot = get_robot(db, robot_id)
    if robot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="robot not found")
    return [
        TelemetryRecordResponse(
            id=record.id,
            source=record.source,
            observed_at=record.observed_at,
            payload=record.payload,
            created_at=record.created_at,
        )
        for record in recent_telemetry(db, robot, limit)
    ]


@app.get("/api/v1/recommendations", response_model=list[RecommendationResponse])
def list_recommendations(
    robot_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[RecommendationResponse]:
    query = db.query(Recommendation).order_by(Recommendation.created_at.desc())
    if robot_id is not None:
        robot = get_robot(db, robot_id)
        if robot is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="robot not found")
        query = query.filter(Recommendation.robot_id == robot.id)
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
        for row in query.all()
    ]


@app.post("/api/v1/demo/seed", response_model=SeedResponse)
def seed_demo(db: Session = Depends(get_db)) -> SeedResponse:
    return SeedResponse(**seed_demo_data(db))
