from datetime import datetime

import pytest

SAMPLE = {"title": "Book removalist", "due_date": "2026-12-01", "assigned_to": "Alex Example"}


def create(client, **overrides):
    payload = {**SAMPLE, **overrides}
    return client.post("/tasks", json=payload)


def test_create_task_with_title_only(client):
    response = client.post("/tasks", json={"title": "Book removalist"})

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Book removalist"
    assert body["status"] == "open"
    assert body["id"]
    assert body["due_date"] is None
    assert body["assigned_to"] is None
    assert body["notes"] is None


def test_create_task_returns_created_at(client):
    response = create(client)

    created_at = datetime.fromisoformat(response.json()["created_at"])
    assert created_at.tzinfo is not None


def test_created_at_cannot_be_set_by_the_client(client):
    response = create(client, created_at="2020-01-01T00:00:00Z")

    assert not response.json()["created_at"].startswith("2020-01-01")


def test_create_task_with_all_fields(client):
    payload = {
        "title": "Enrol in Medicare",
        "due_date": "2026-12-01",
        "assigned_to": "Alex Example",
        "notes": "Check the official Services Australia page first",
        "start_by": "2026-11-15",
        "case_id": "case-123",
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    body = response.json()
    for key, value in payload.items():
        assert body[key] == value


def test_surrounding_spaces_are_trimmed(client):
    response = create(client, title="  Book flights  ", assigned_to="  Alex Example ")

    assert response.json()["title"] == "Book flights"
    assert response.json()["assigned_to"] == "Alex Example"


def test_create_task_without_title_is_rejected(client):
    response = client.post("/tasks", json={"due_date": "2026-12-01"})

    assert response.status_code == 422


@pytest.mark.parametrize("field", ["title", "assigned_to"])
@pytest.mark.parametrize("blank", ["", "   "])
def test_create_task_with_blank_text_is_rejected(client, field, blank):
    response = create(client, **{field: blank})

    assert response.status_code == 422


def test_create_task_with_invalid_date_is_rejected(client):
    response = create(client, due_date="not-a-date")

    assert response.status_code == 422


def test_create_task_with_start_by_after_due_date_is_rejected(client):
    response = create(client, due_date="2026-12-01", start_by="2026-12-02")

    assert response.status_code == 422
    assert "Start by" in response.json()["detail"]


def test_list_tasks_is_empty_at_start(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_returns_created_tasks(client):
    create(client, title="First")
    create(client, title="Second")

    response = client.get("/tasks")

    titles = [task["title"] for task in response.json()]
    assert titles == ["First", "Second"]


def test_rejected_task_is_not_stored(client):
    create(client, start_by="2027-01-01")

    assert client.get("/tasks").json() == []


def test_complete_task(client):
    task_id = create(client, title="Close bank account").json()["id"]

    response = client.post(f"/tasks/{task_id}/complete")

    assert response.status_code == 200
    assert response.json()["status"] == "done"
    listed = client.get("/tasks").json()
    assert listed[0]["status"] == "done"


def test_complete_task_twice_is_allowed(client):
    task_id = create(client, title="Close bank account").json()["id"]
    client.post(f"/tasks/{task_id}/complete")

    response = client.post(f"/tasks/{task_id}/complete")

    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_complete_unknown_task_returns_404(client):
    response = client.post("/tasks/does-not-exist/complete")

    assert response.status_code == 404
