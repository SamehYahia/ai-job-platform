from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_demo_ui_is_served() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "AI Job Platform" in response.text
    assert "/api/v1/matches/evaluate" in response.text


def test_liveness_returns_ok() -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness() -> None:
    """Readiness succeeds when the database accepts queries."""
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
