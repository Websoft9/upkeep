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


class RobotResponse(BaseModel):
    robot_id: str
    robot_name: str | None
    cell_name: str | None
    vendor: str | None
    telemetry_count: int
    recommendation_count: int
    latest_observed_at: datetime | None


class SeedResponse(BaseModel):
    robots_created: int
    telemetry_created: int
    recommendations_created: int


class HealthResponse(BaseModel):
    status: str
