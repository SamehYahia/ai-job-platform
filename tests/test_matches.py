from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_match_is_deterministic_and_explainable() -> None:
    response = client.post(
        "/api/v1/matches/evaluate",
        json={
            "job": {
                "title": "Junior DevOps Engineer",
                "required_skills": ["AWS", "Docker", "Kubernetes", "Terraform"],
            },
            "candidate": {
                "profile_id": "candidate-001",
                "skills": ["docker", "AWS", "Python"],
            },
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "score_percent": 50.0,
        "matched_skills": ["aws", "docker"],
        "missing_skills": ["kubernetes", "terraform"],
        "explanation": "Matched 2 of 4 required skills.",
    }


def test_match_normalizes_duplicate_skills() -> None:
    response = client.post(
        "/api/v1/matches/evaluate",
        json={
            "job": {
                "title": "Cloud Engineer",
                "required_skills": [" AWS ", "aws", "Docker"],
            },
            "candidate": {
                "profile_id": "candidate-002",
                "skills": ["AWS"],
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["score_percent"] == 50.0


def test_match_rejects_empty_required_skills() -> None:
    response = client.post(
        "/api/v1/matches/evaluate",
        json={
            "job": {
                "title": "DevOps Engineer",
                "required_skills": [],
            },
            "candidate": {
                "profile_id": "candidate-003",
                "skills": ["Linux"],
            },
        },
    )

    assert response.status_code == 422
