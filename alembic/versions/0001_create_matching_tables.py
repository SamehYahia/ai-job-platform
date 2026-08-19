"""Create matching tables.

Revision ID: 0001_create_matching_tables
Revises:
Create Date: 2026-08-19 00:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001_create_matching_tables"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("required_skills", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_jobs_id"), "jobs", ["id"], unique=False)

    op.create_table(
        "candidates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.String(length=100), nullable=False),
        sa.Column("skills", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_candidates_id"), "candidates", ["id"], unique=False)
    op.create_index(op.f("ix_candidates_profile_id"), "candidates", ["profile_id"], unique=True)

    op.create_table(
        "match_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.Integer(), nullable=False),
        sa.Column("candidate_id", sa.Integer(), nullable=False),
        sa.Column("score_percent", sa.Float(), nullable=False),
        sa.Column("matched_skills", sa.JSON(), nullable=False),
        sa.Column("missing_skills", sa.JSON(), nullable=False),
        sa.Column("explanation", sa.String(length=300), nullable=False),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidates.id"]),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_match_results_id"), "match_results", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_match_results_id"), table_name="match_results")
    op.drop_table("match_results")
    op.drop_index(op.f("ix_candidates_profile_id"), table_name="candidates")
    op.drop_index(op.f("ix_candidates_id"), table_name="candidates")
    op.drop_table("candidates")
    op.drop_index(op.f("ix_jobs_id"), table_name="jobs")
    op.drop_table("jobs")
