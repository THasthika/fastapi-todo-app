from fastapi.testclient import TestClient
from fastapi import Response

from .main import app

client = TestClient(app)


def test_health_check():
    response: Response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_creation():

    response: Response = client.post("/todos",
                                     json={
                                         "title": "Hello",
                                         "description": "World"
                                         })
    assert response.status_code == 201
    # assert response.json() == {""}


def test_post_listing():

    response: Response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()["result"]) != 0


def test_put_update():
    response: Response = client.post("/todos",
                                     json={
                                         "title": "Hello",
                                         "description": "World"
                                     })
    todo_id = response.json()["result"]["id"]

    response: Response = client.put(f"/todos/{todo_id}",
                                    json={
                                        "title": "Updated Title",
                                        "description": "Updated Description",
                                        "completed": True
                                    })
    assert response.status_code == 200
    assert "result" in response.json()
    assert response.json()["result"]["id"] == todo_id
    assert response.json()["result"]["title"] == "Updated Title"
    assert response.json()["result"]["description"] == "Updated Description"
    assert response.json()["result"]["completed"] is True


def test_delete_todo():
    response: Response = client.post("/todos",
                                     json={
                                         "title": "Hello",
                                         "description": "World"
                                     })
    todo_id = response.json()["result"]["id"]

    response: Response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200

    response: Response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404
