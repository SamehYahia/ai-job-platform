import os
from collections.abc import Generator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from app.models import Candidate, Job, MatchResult
from app.repositories.matches import save_match_evaluation
from app.schemas.match import MatchRequest
from app.services.matcher import calculate_match

TRUNCATE_TEST_TABLES = text("TRUNCATE TABLE match_results, candidates, jobs RESTART IDENTITY")


@pytest.fixture
def postgres_database() -> Generator[sessionmaker[Session], None, None]:
    """Provide an isolated PostgreSQL session factory for integration testing."""
    database_url = os.getenv("TEST_DATABASE_URL")

    if database_url is None:
        pytest.skip("TEST_DATABASE_URL is required for PostgreSQL integration tests")

    parsed_url = make_url(database_url)

    if parsed_url.get_backend_name() != "postgresql":
        pytest.fail("TEST_DATABASE_URL must use PostgreSQL")

    database_name = parsed_url.database or ""
    if not database_name.endswith("_test"):
        pytest.fail("Integration database name must end with '_test'")

    engine = create_engine(database_url, pool_pre_ping=True)
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    # The schema must already exist through Alembic migrations.
    with engine.begin() as connection:
        connection.execute(TRUNCATE_TEST_TABLES)

    try:
        yield testing_session_local
    finally:
        try:
            with engine.begin() as connection:
                connection.execute(TRUNCATE_TEST_TABLES)
        finally:
            engine.dispose()


@pytest.mark.integration
def test_match_evaluation_persists_with_postgresql(
    postgres_database: sessionmaker[Session],
) -> None:
    """Verify the repository persists a complete evaluation in PostgreSQL."""
    request = MatchRequest.model_validate(
        {
            "job": {
                "title": "Platform Engineer",
                "required_skills": ["AWS", "Terraform", "Kubernetes"],
            },
            "candidate": {
                "profile_id": "postgres-integration-001",
                "skills": ["AWS", "Terraform"],
            },
        }
    )
    result = calculate_match(request)

    with postgres_database() as db:
        assert db.get_bind().dialect.name == "postgresql"

        saved_result = save_match_evaluation(db, request, result)
        job_id = saved_result.job_id
        candidate_id = saved_result.candidate_id
        result_id = saved_result.id

    with postgres_database() as db:
        job = db.get(Job, job_id)
        candidate = db.get(Candidate, candidate_id)
        match_result = db.get(MatchResult, result_id)

        assert job is not None
        assert job.required_skills == ["aws", "terraform", "kubernetes"]

        assert candidate is not None
        assert candidate.profile_id == "postgres-integration-001"
        assert candidate.skills == ["aws", "terraform"]

        assert match_result is not None
        assert match_result.score_percent == 66.67
        assert match_result.matched_skills == ["aws", "terraform"]
        assert match_result.missing_skills == ["kubernetes"]
