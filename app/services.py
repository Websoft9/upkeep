from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models import RawTelemetryRecord, Recommendation, Robot
from app.rules import DEFAULT_RULES
from app.schemas import TelemetryIngestRequest


def get_or_create_robot(db: Session, telemetry: TelemetryIngestRequest) -> Robot:
    robot = db.query(Robot).filter(Robot.external_id == telemetry.robot_id).first()
    if robot is None:
        robot = Robot(
            external_id=telemetry.robot_id,
            name=telemetry.robot_name,
            cell_name=telemetry.cell_name,
            vendor=telemetry.vendor,
        )
        db.add(robot)
        db.flush()
        return robot

    if telemetry.robot_name and robot.name != telemetry.robot_name:
        robot.name = telemetry.robot_name
    if telemetry.cell_name and robot.cell_name != telemetry.cell_name:
        robot.cell_name = telemetry.cell_name
    if telemetry.vendor and robot.vendor != telemetry.vendor:
        robot.vendor = telemetry.vendor
    return robot


def store_raw_telemetry(db: Session, robot: Robot, telemetry: TelemetryIngestRequest) -> RawTelemetryRecord:
    record = RawTelemetryRecord(
        source=telemetry.source,
        observed_at=telemetry.ts,
        payload=telemetry.payload,
        robot_id=robot.id,
    )
    db.add(record)
    db.flush()
    return record


def build_recommendations(record: RawTelemetryRecord) -> list[Recommendation]:
    payload = record.payload
    recommendations: list[Recommendation] = []

    for rule in DEFAULT_RULES:
        observed = payload.get(rule.metric)
        if observed is None or observed <= rule.threshold:
            continue
        recommendations.append(
            Recommendation(
                recommendation_type=rule.metric,
                risk_level=rule.risk_level,
                message=rule.message,
                evidence={
                    "metric": rule.metric,
                    "observed": observed,
                    "threshold": rule.threshold,
                    "telemetry_record_id": record.id,
                },
                robot_id=record.robot_id,
                telemetry_record_id=record.id,
            )
        )

    return recommendations


def ingest_telemetry(db: Session, telemetry: TelemetryIngestRequest) -> tuple[RawTelemetryRecord, list[Recommendation]]:
    robot = get_or_create_robot(db, telemetry)
    record = store_raw_telemetry(db, robot, telemetry)
    recommendations = build_recommendations(record)
    for recommendation in recommendations:
        db.add(recommendation)
    db.commit()
    db.refresh(record)
    return record, recommendations


def seed_demo_data(db: Session) -> dict[str, int]:
    samples = [
        TelemetryIngestRequest(
            source="demo-seed",
            robot_id="robot-01",
            robot_name="Welding Robot 01",
            cell_name="Cell A",
            vendor="DemoVendor",
            ts=datetime.now(timezone.utc) - timedelta(minutes=6),
            payload={"temperature_c": 82, "vibration_mm_s": 7, "cycle_time_s": 79, "axis_load_pct": 72},
        ),
        TelemetryIngestRequest(
            source="demo-seed",
            robot_id="robot-02",
            robot_name="Handling Robot 02",
            cell_name="Cell B",
            vendor="DemoVendor",
            ts=datetime.now(timezone.utc) - timedelta(minutes=4),
            payload={"temperature_c": 61, "vibration_mm_s": 14, "cycle_time_s": 68, "axis_load_pct": 94},
        ),
        TelemetryIngestRequest(
            source="demo-seed",
            robot_id="robot-03",
            robot_name="Assembly Robot 03",
            cell_name="Cell C",
            vendor="DemoVendor",
            ts=datetime.now(timezone.utc) - timedelta(minutes=2),
            payload={"temperature_c": 58, "vibration_mm_s": 6, "cycle_time_s": 57, "axis_load_pct": 63},
        ),
    ]

    telemetry_created = 0
    recommendations_created = 0
    robot_ids_before = {row.external_id for row in db.query(Robot).all()}

    for sample in samples:
        _, recommendations = ingest_telemetry(db, sample)
        telemetry_created += 1
        recommendations_created += len(recommendations)

    robot_ids_after = {row.external_id for row in db.query(Robot).all()}
    return {
        "robots_created": len(robot_ids_after - robot_ids_before),
        "telemetry_created": telemetry_created,
        "recommendations_created": recommendations_created,
    }
