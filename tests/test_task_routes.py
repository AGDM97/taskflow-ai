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


def test_should_summarize_task_with_description(monkeypatch):
   def fake_generate_task_breakdown(title, description, status, priority):
    return 
    [
        {
            "title": "Define API contract",
            "description": "Create the endpoint contract for task breakdown.",
            "priority": "HIGH"
        },
        {
            "title": "Implement service",
            "description": "Create the service that calls the LLM client.",
            "priority": "HIGH"
        },
        {
            "title": "Add tests",
            "description": "Validate successful and error scenarios.",
            "priority": "MEDIUM"
        }
    ]
    

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


def test_should_summarize_task_without_description(monkeypatch):
    def fake_generate_task_summary(title, description, status, priority):
        return (
            f"Summary generated for title={title}, "
            f"description={description}, status={status}, priority={priority}"
        )

    monkeypatch.setattr(
        "app.services.task_summary_service.llm_client.generate_task_summary",
        fake_generate_task_summary,
    )

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
    assert "None" in data["summary"]
    assert "TODO" in data["summary"]
    assert "MEDIUM" in data["summary"]


def test_should_return_404_when_summarizing_non_existing_task():
    response = client.post("/tasks/non-existing-id/summarize")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_should_break_task_into_subtasks(monkeypatch):
    def fake_generate_task_breakdown(title, description, status, priority):
        return [
            {
                "title": "Define API contract",
                "description": "Create the endpoint contract for task breakdown.",
                "priority": "HIGH",
            },
            {
                "title": "Implement service",
                "description": "Create the service that calls the LLM client.",
                "priority": "HIGH",
            },
            {
                "title": "Add tests",
                "description": "Validate successful and error scenarios.",
                "priority": "MEDIUM",
            },
        ]

    monkeypatch.setattr(
        "app.services.task_breakdown_service.llm_client.generate_task_breakdown",
        fake_generate_task_breakdown,
    )

    create_response = client.post(
        "/tasks",
        json={
            "title": "Build breakdown feature",
            "description": "Use LLM to generate subtasks",
            "priority": "HIGH",
        },
    )

    task_id = create_response.json()["id"]

    response = client.post(f"/tasks/{task_id}/breakdown")

    assert response.status_code == 200

    data = response.json()

    assert data["task_id"] == task_id
    assert len(data["subtasks"]) == 3
    assert data["subtasks"][0]["title"] == "Define API contract"
    assert data["subtasks"][0]["priority"] == "HIGH"


def test_should_return_404_when_breaking_down_non_existing_task():
    response = client.post("/tasks/non-existing-id/breakdown")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_should_return_502_when_llm_breakdown_output_is_invalid(monkeypatch):
    def fake_generate_invalid_task_breakdown(title, description, status, priority):return "This is not valid JSON"

    monkeypatch.setattr(
        "app.services.task_breakdown_service.llm_client.generate_task_breakdown",
        fake_generate_invalid_task_breakdown,
    )

    create_response = client.post(
        "/tasks",
        json={
            "title": "Build invalid output test",
            "description": "Validate bad LLM response",
        },
    )

    task_id = create_response.json()["id"]

    response = client.post(f"/tasks/{task_id}/breakdown")

    assert response.status_code == 502
    assert response.json()["detail"] == "Invalid LLM output"
