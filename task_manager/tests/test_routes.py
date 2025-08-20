import pytest
from app import create_app
from app.db import db

@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    with app.app_context():
        db.drop_all()

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}

def test_create_task_valid(client):
    res = client.post("/api/tasks", json={"title": "Test task", "description": "desc"})
    assert res.status_code == 201
    body = res.get_json()
    assert body["title"] == "Test task"
    assert body["description"] == "desc"
    assert body["status"] == "pending"

def test_create_task_requires_title(client):
    res = client.post("/api/tasks", json={"description": "no title"})
    assert res.status_code == 400

def test_get_task(client):
    created = client.post("/api/tasks", json={"title": "Task 1"}).get_json()
    res = client.get(f"/api/tasks/{created['id']}")
    assert res.status_code == 200
    assert res.get_json()["id"] == created["id"]

def test_get_tasks_list(client):
    client.post("/api/tasks", json={"title": "Task 1"})
    client.post("/api/tasks", json={"title": "Task 2"})
    res = client.get("/api/tasks")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_update_task(client):
    created = client.post("/api/tasks", json={"title": "Old"}).get_json()
    res = client.put(f"/api/tasks/{created['id']}", json={"title": "New", "status": "done"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["title"] == "New"
    assert data["status"] == "done"

def test_delete_task(client):
    created = client.post("/api/tasks", json={"title": "To delete"}).get_json()
    res = client.delete(f"/api/tasks/{created['id']}")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Task deleted successfully"
    # ensure 404 after delete
    res2 = client.get(f"/api/tasks/{created['id']}")
    assert res2.status_code == 404
