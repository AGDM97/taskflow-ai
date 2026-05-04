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


def test_should_get_task_by_id():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Read documentation",
            "description": "Study FastAPI docs",
        },
    )

    created_task = create_response.json()
    task_id = created_task["id"]

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["id"] == task_id
    assert data["title"] == "Read documentation"
    assert data["status"] == "TODO"


def test_should_return_404_when_task_does_not_exist():
    response = client.get("/tasks/non-existing-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_should_update_task_status():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Implement status update",
            "description": "Add PATCH endpoint",
        },
    )

    created_task = create_response.json()
    task_id = created_task["id"]

    update_response = client.patch(
        f"/tasks/{task_id}/status",
        json={
            "status": "IN_PROGRESS",
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == task_id
    assert data["status"] == "IN_PROGRESS"


def test_should_return_404_when_updating_non_existing_task():
    response = client.patch(
        "/tasks/non-existing-id/status",
        json={
            "status": "DONE",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_should_reject_invalid_status():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Validate status",
        },
    )

    created_task = create_response.json()
    task_id = created_task["id"]

    response = client.patch(
        f"/tasks/{task_id}/status",
        json={
            "status": "INVALID_STATUS",
        },
    )

    assert response.status_code == 422


def test_should_summarize_task_with_description():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Build AI feature",
            "description": "Create the summarize task endpoint",
            "priority": "HIGH",
        },
    )

    created_task = create_response.json()
    task_id = created_task["id"]

    response = client.post(f"/tasks/{task_id}/summarize")

    assert response.status_code == 200

    data = response.json()

    assert data["task_id"] == task_id
    assert "Build AI feature" in data["summary"]
    assert "Create the summarize task endpoint" in data["summary"]
    assert "TODO" in data["summary"]
    assert "HIGH" in data["summary"]


def test_should_summarize_task_without_description():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Review code",
        },
    )

    created_task = create_response.json()
    task_id = created_task["id"]

    response = client.post(f"/tasks/{task_id}/summarize")

    assert response.status_code == 200

    data = response.json()

    assert data["task_id"] == task_id
    assert "Review code" in data["summary"]
    assert "No description was provided" in data["summary"]


def test_should_return_404_when_summarizing_non_existing_task():
    response = client.post("/tasks/non-existing-id/summarize")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
