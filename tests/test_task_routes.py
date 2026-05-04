from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_should_create_task_successfully():
    response = client.post(
        "/tasks",
        json={
            "title": "Study FastAPI",
            "description": "Create first endpoint",
            "priority": "HIGH",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "Study FastAPI"
    assert data["description"] == "Create first endpoint"
    assert data["status"] == "TODO"
    assert data["priority"] == "HIGH"


def test_should_create_task_with_default_priority():
    response = client.post(
        "/tasks",
        json={
            "title": "Study Python",
            "description": "Practice backend development",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["priority"] == "MEDIUM"
    assert data["status"] == "TODO"


def test_should_reject_short_title():
    response = client.post(
        "/tasks",
        json={
            "title": "AI",
        },
    )

    assert response.status_code == 422
