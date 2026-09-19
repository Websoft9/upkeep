from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models import RawTelemetryRecord, Recommendation, Robot
from app.rules import DEFAULT_RULES
from app.schemas import RobotCreate, RobotUpdate, TelemetryIngestRequest


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


def list_robots(db: Session) -> list[Robot]:
    return db.query(Robot).order_by(Robot.external_id.asc()).all()


def get_robot(db: Session, external_id: str) -> Robot | None:
    return db.query(Robot).filter(Robot.external_id == external_id).first()


def create_robot(db: Session, data: RobotCreate) -> Robot:
    if get_robot(db, data.external_id) is not None:
        raise ValueError(f"robot '{data.external_id}' already exists")
    robot = Robot(
        external_id=data.external_id,
        name=data.robot_name,
        vendor=data.vendor,
        model=data.model,
        serial_number=data.serial_number,
        controller_type=data.controller_type,
        firmware_version=data.firmware_version,
        site=data.site,
        line=data.line,
        cell_name=data.cell_name,
        status=data.status,
        description=data.description,
        metadata_json=data.metadata_json,
        installed_at=data.installed_at,
    )
    db.add(robot)
    db.commit()
    db.refresh(robot)
    return robot


def update_robot(db: Session, robot: Robot, data: RobotUpdate) -> Robot:
    updates = data.model_dump(exclude_unset=True)
    if "robot_name" in updates:
        updates["name"] = updates.pop("robot_name")
    for key, value in updates.items():
        setattr(robot, key, value)
    db.commit()
    db.refresh(robot)
    return robot


def recent_telemetry(db: Session, robot: Robot, limit: int = 20) -> list[RawTelemetryRecord]:
    return (
        db.query(RawTelemetryRecord)
        .filter(RawTelemetryRecord.robot_id == robot.id)
        .order_by(RawTelemetryRecord.observed_at.desc())
        .limit(limit)
        .all()
    )


def robot_summary(robot: Robot) -> dict:
    return {
        "robot_id": robot.external_id,
        "robot_name": robot.name,
        "vendor": robot.vendor,
        "model": robot.model,
        "site": robot.site,
        "line": robot.line,
        "cell_name": robot.cell_name,
        "status": robot.status,
        "telemetry_count": len(robot.telemetry_records),
        "recommendation_count": len(robot.recommendations),
        "latest_observed_at": max((record.observed_at for record in robot.telemetry_records), default=None),
    }


def robot_detail(robot: Robot) -> dict:
    data = robot_summary(robot)
    data.update(
        {
            "serial_number": robot.serial_number,
            "controller_type": robot.controller_type,
            "firmware_version": robot.firmware_version,
            "description": robot.description,
            "metadata_json": robot.metadata_json,
            "installed_at": robot.installed_at,
            "created_at": robot.created_at,
            "updated_at": robot.updated_at,
        }
    )
    return data


SEED_ROBOTS = [
    RobotCreate(
        external_id="robot-01",
        robot_name="Welding Robot 01",
        vendor="KUKA",
        model="KR 10 R1100",
        serial_number="KUKA-0001",
        controller_type="KR C5",
        firmware_version="8.6",
        site="Plant A",
        line="Line 1",
        cell_name="Cell A",
        status="active",
        description="Arc welding cell",
        metadata_json={"payload_kg": 10, "reach_mm": 1100},
    ),
    RobotCreate(
        external_id="robot-02",
        robot_name="Handling Robot 02",
        vendor="FANUC",
        model="M-20iD/25",
        serial_number="FANUC-0021",
        controller_type="R-30iB",
        firmware_version="V9.30",
        site="Plant A",
        line="Line 1",
        cell_name="Cell B",
        status="maintenance",
        description="Material handling and machine tending",
        metadata_json={"payload_kg": 25, "reach_mm": 1831},
    ),
    RobotCreate(
        external_id="robot-03",
        robot_name="Assembly Robot 03",
        vendor="ABB",
        model="IRB 2600",
        serial_number="ABB-0007",
        controller_type="IRC5",
        firmware_version="6.15",
        site="Plant A",
        line="Line 2",
        cell_name="Cell C",
        status="active",
        description="Assembly and pick-place",
        metadata_json={"payload_kg": 12, "reach_mm": 1650},
    ),
]

SEED_TELEMETRY = [
    TelemetryIngestRequest(
        source="demo-seed",
        robot_id="robot-01",
        robot_name="Welding Robot 01",
        cell_name="Cell A",
        vendor="KUKA",
        ts=datetime.now(timezone.utc) - timedelta(minutes=6),
        payload={"temperature_c": 82, "vibration_mm_s": 7, "cycle_time_s": 79, "axis_load_pct": 72},
    ),
    TelemetryIngestRequest(
        source="demo-seed",
        robot_id="robot-02",
        robot_name="Handling Robot 02",
        cell_name="Cell B",
        vendor="FANUC",
        ts=datetime.now(timezone.utc) - timedelta(minutes=4),
        payload={"temperature_c": 61, "vibration_mm_s": 14, "cycle_time_s": 68, "axis_load_pct": 94},
    ),
    TelemetryIngestRequest(
        source="demo-seed",
        robot_id="robot-03",
        robot_name="Assembly Robot 03",
        cell_name="Cell C",
        vendor="ABB",
        ts=datetime.now(timezone.utc) - timedelta(minutes=2),
        payload={"temperature_c": 58, "vibration_mm_s": 6, "cycle_time_s": 57, "axis_load_pct": 63},
    ),
]


def seed_demo_data(db: Session) -> dict[str, int]:
    robot_ids_before = {row.external_id for row in db.query(Robot).all()}

    for robot_data in SEED_ROBOTS:
        existing = get_robot(db, robot_data.external_id)
        if existing is None:
            create_robot(db, robot_data)
        else:
            update_robot(
                db,
                existing,
                RobotUpdate(**robot_data.model_dump(exclude={"external_id"})),
            )

    telemetry_created = 0
    recommendations_created = 0
    for sample in SEED_TELEMETRY:
        _, recommendations = ingest_telemetry(db, sample)
        telemetry_created += 1
        recommendations_created += len(recommendations)

    robot_ids_after = {row.external_id for row in db.query(Robot).all()}
    return {
        "robots_created": len(robot_ids_after - robot_ids_before),
        "telemetry_created": telemetry_created,
        "recommendations_created": recommendations_created,
    }
