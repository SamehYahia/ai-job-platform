from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Provide one database session for each API request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        # Always release the connection, including failed requests.
        db.close()
