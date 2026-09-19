from app.database import SessionLocal, init_db
from app.services import seed_demo_data


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        result = seed_demo_data(db)
        print(result)
    finally:
        db.close()


if __name__ == "__main__":
    main()
