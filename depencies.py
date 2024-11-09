from sqlalchemy.orm import Session

from db.engine import SessionLocal


def get_db() -> Session:
    with SessionLocal() as db:
        yield db
