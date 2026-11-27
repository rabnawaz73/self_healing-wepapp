"""Health and application information endpoint tests."""

from fastapi.testclient import TestClient

from app import config
from app.main import app


client = TestClient(app)


def test_root_returns_the_storefront():
    response = client.get("/")

    assert response.status_code == 200
    assert "CloudRescue" in response.text
    assert "text/html" in response.headers["content-type"]


def test_health_returns_healthy():
    config.FORCE_UNHEALTHY = False

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "version": "1.0",
        "service": "CloudRescue",
    }


def test_health_returns_unhealthy_when_failure_is_forced(monkeypatch):
    monkeypatch.setattr(config, "FORCE_UNHEALTHY", True)

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["detail"] == {
        "status": "unhealthy",
        "version": "1.0",
        "service": "CloudRescue",
    }


def test_version_returns_deployed_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "version": "1.0",
        "environment": "production",
    }
