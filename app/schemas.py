from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TelemetryIngestRequest(BaseModel):
    source: str = Field(min_length=1, max_length=100)
    robot_id: str = Field(min_length=1, max_length=100)
    robot_name: str | None = Field(default=None, max_length=200)
    cell_name: str | None = Field(default=None, max_length=200)
    vendor: str | None = Field(default=None, max_length=100)
    ts: datetime
    payload: dict[str, Any]


class TelemetryIngestResponse(BaseModel):
    telemetry_id: int
    recommendation_count: int


class RecommendationResponse(BaseModel):
    id: int
    robot_id: str
    recommendation_type: str
    risk_level: str
    message: str
    evidence: dict[str, Any]
    created_at: datetime


class TelemetryRecordResponse(BaseModel):
    id: int
    source: str
    observed_at: datetime
    payload: dict[str, Any]
    created_at: datetime


class RobotCreate(BaseModel):
    external_id: str = Field(min_length=1, max_length=100)
    robot_name: str | None = Field(default=None, max_length=200)
    vendor: str | None = Field(default=None, max_length=100)
    model: str | None = Field(default=None, max_length=100)
    serial_number: str | None = Field(default=None, max_length=100)
    controller_type: str | None = Field(default=None, max_length=100)
    firmware_version: str | None = Field(default=None, max_length=100)
    site: str | None = Field(default=None, max_length=200)
    line: str | None = Field(default=None, max_length=200)
    cell_name: str | None = Field(default=None, max_length=200)
    status: str = Field(default="active", max_length=50)
    description: str | None = Field(default=None, max_length=2000)
    metadata_json: dict[str, Any] | None = None
    installed_at: datetime | None = None


class RobotUpdate(BaseModel):
    robot_name: str | None = Field(default=None, max_length=200)
    vendor: str | None = Field(default=None, max_length=100)
    model: str | None = Field(default=None, max_length=100)
    serial_number: str | None = Field(default=None, max_length=100)
    controller_type: str | None = Field(default=None, max_length=100)
    firmware_version: str | None = Field(default=None, max_length=100)
    site: str | None = Field(default=None, max_length=200)
    line: str | None = Field(default=None, max_length=200)
    cell_name: str | None = Field(default=None, max_length=200)
    status: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=2000)
    metadata_json: dict[str, Any] | None = None
    installed_at: datetime | None = None


class RobotResponse(BaseModel):
    robot_id: str
    robot_name: str | None
    vendor: str | None
    model: str | None
    site: str | None
    line: str | None
    cell_name: str | None
    status: str
    telemetry_count: int
    recommendation_count: int
    latest_observed_at: datetime | None


class RobotDetailResponse(RobotResponse):
    serial_number: str | None
    controller_type: str | None
    firmware_version: str | None
    description: str | None
    metadata_json: dict[str, Any] | None
    installed_at: datetime | None
    created_at: datetime
    updated_at: datetime | None


class SeedResponse(BaseModel):
    robots_created: int
    telemetry_created: int
    recommendations_created: int


class HealthResponse(BaseModel):
    status: str
