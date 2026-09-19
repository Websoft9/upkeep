from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Robot(Base):
    __tablename__ = "robots"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    cell_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    vendor: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    telemetry_records: Mapped[list["RawTelemetryRecord"]] = relationship(back_populates="robot")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="robot")


class RawTelemetryRecord(Base):
    __tablename__ = "raw_telemetry_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(100))
    observed_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    robot_id: Mapped[int] = mapped_column(ForeignKey("robots.id"), index=True)

    robot: Mapped[Robot] = relationship(back_populates="telemetry_records")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="telemetry_record")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    recommendation_type: Mapped[str] = mapped_column(String(100))
    risk_level: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
    evidence: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    robot_id: Mapped[int] = mapped_column(ForeignKey("robots.id"), index=True)
    telemetry_record_id: Mapped[int] = mapped_column(ForeignKey("raw_telemetry_records.id"), index=True)

    robot: Mapped[Robot] = relationship(back_populates="recommendations")
    telemetry_record: Mapped[RawTelemetryRecord] = relationship(back_populates="recommendations")
