from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Candidate(Base):
    """Candidate profile with normalized skills for matching."""

    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    skills: Mapped[list[str]] = mapped_column(JSON, nullable=False)
