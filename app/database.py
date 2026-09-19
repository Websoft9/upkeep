from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


DATABASE_URL = settings.database_url


class Base(DeclarativeBase):
    pass


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


def _apply_lightweight_migrations() -> None:
    inspector = inspect(engine)
    if "robots" not in inspector.get_table_names():
        return

    robot_columns = {column["name"] for column in inspector.get_columns("robots")}
    if "vendor" not in robot_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE robots ADD COLUMN vendor VARCHAR(100)"))
