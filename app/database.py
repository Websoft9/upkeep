from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


DATABASE_URL = settings.database_url


def _ensure_sqlite_directory(url: str) -> None:
    prefix = "sqlite:///"
    if not url.startswith(prefix):
        return
    path = url[len(prefix) :]
    if not path or path == ":memory:":
        return
    Path(path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


class Base(DeclarativeBase):
    pass


_ensure_sqlite_directory(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.models import Recommendation, Robot, RawTelemetryRecord  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _apply_lightweight_migrations()


ROBOT_COLUMN_MIGRATIONS = {
    "vendor": "VARCHAR(100)",
    "model": "VARCHAR(100)",
    "serial_number": "VARCHAR(100)",
    "controller_type": "VARCHAR(100)",
    "firmware_version": "VARCHAR(100)",
    "site": "VARCHAR(200)",
    "line": "VARCHAR(200)",
    "status": "VARCHAR(50) DEFAULT 'active'",
    "description": "TEXT",
    "metadata": "JSON",
    "installed_at": "DATETIME",
    "updated_at": "DATETIME",
}


def _apply_lightweight_migrations() -> None:
    inspector = inspect(engine)
    if "robots" not in inspector.get_table_names():
        return

    robot_columns = {column["name"] for column in inspector.get_columns("robots")}
    with engine.begin() as connection:
        for column, definition in ROBOT_COLUMN_MIGRATIONS.items():
            if column in robot_columns:
                continue
            connection.execute(text(f"ALTER TABLE robots ADD COLUMN {column} {definition}"))
