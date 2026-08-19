from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.main import app
from app.models import Candidate, Job, MatchResult


def test_match_evaluation_is_persisted(
    test_database: sessionmaker[Session],
) -> None:
    """Verify that an API evaluation persists all related records."""
    client = TestClient(app)

    response = client.post(
        "/api/v1/matches/evaluate",
        json={
            "job": {
                "title": "Junior DevOps Engineer",
                "required_skills": ["AWS", "Docker", "Kubernetes"],
            },
            "candidate": {
                "profile_id": "candidate-persistence-001",
                "skills": ["AWS", "Docker"],
            },
        },
    )

    assert response.status_code == 200

    with test_database() as db:
        job = db.scalar(select(Job))
        candidate = db.scalar(select(Candidate))
        match_result = db.scalar(select(MatchResult))

        assert job is not None
        assert job.title == "Junior DevOps Engineer"
        assert job.required_skills == ["aws", "docker", "kubernetes"]

        assert candidate is not None
        assert candidate.profile_id == "candidate-persistence-001"
        assert candidate.skills == ["aws", "docker"]

        assert match_result is not None
        assert match_result.job_id == job.id
        assert match_result.candidate_id == candidate.id
        assert match_result.score_percent == 66.67
        assert match_result.matched_skills == ["aws", "docker"]
        assert match_result.missing_skills == ["kubernetes"]
