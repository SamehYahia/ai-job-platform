from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Job(Base):
    """Job record with the required skills used by the matcher."""

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    required_skills: Mapped[list[str]] = mapped_column(JSON, nullable=False)
