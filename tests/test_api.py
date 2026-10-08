from conftest import make_user


def test_register_success(client):
    res = client.post(
        "/auth/register",
        json={"name": "Merga", "email": "m@example.com", "password": "password123"},
    )
    assert res.status_code == 201
    assert res.json()["email"] == "m@example.com"
    assert "password" not in res.json()
    assert "password_hash" not in res.json()


def test_register_duplicate_email(client):
    body = {"name": "A", "email": "dup@example.com", "password": "password123"}
    client.post("/auth/register", json=body)
    res = client.post("/auth/register", json=body)
    assert res.status_code == 409


def test_login_wrong_password(client):
    make_user(client, "A", "a@example.com")
    res = client.post("/auth/login", data={"username": "a@example.com", "password": "wrongpass"})
    assert res.status_code == 401


def test_tasks_require_auth(client):
    assert client.get("/tasks").status_code == 401


def test_create_and_list_tasks(client):
    headers = make_user(client, "A", "a@example.com")
    res = client.post("/tasks", json={"title": "Learn pytest"}, headers=headers)
    assert res.status_code == 201
    assert res.json()["title"] == "Learn pytest"

    res = client.get("/tasks", headers=headers)
    assert res.json()["total"] == 1
    assert len(res.json()["items"]) == 1


def test_update_task(client):
    headers = make_user(client, "A", "a@example.com")
    task_id = client.post("/tasks", json={"title": "Old"}, headers=headers).json()["id"]

    res = client.put(
        f"/tasks/{task_id}",
        json={"title": "New", "completed": True},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["title"] == "New"
    assert res.json()["completed"] is True


def test_delete_task(client):
    headers = make_user(client, "A", "a@example.com")
    task_id = client.post("/tasks", json={"title": "Temp"}, headers=headers).json()["id"]

    assert client.delete(f"/tasks/{task_id}", headers=headers).status_code == 204
    assert client.get(f"/tasks/{task_id}", headers=headers).status_code == 404


def test_cannot_access_other_users_task(client):
    alice = make_user(client, "Alice", "alice@example.com")
    bob = make_user(client, "Bob", "bob@example.com")

    task_id = client.post("/tasks", json={"title": "Private"}, headers=alice).json()["id"]

    assert client.get(f"/tasks/{task_id}", headers=bob).status_code == 404
    assert client.put(
        f"/tasks/{task_id}", json={"title": "hacked", "completed": True}, headers=bob
    ).status_code == 404
    assert client.delete(f"/tasks/{task_id}", headers=bob).status_code == 404

    # Alice's task is untouched
    res = client.get(f"/tasks/{task_id}", headers=alice)
    assert res.json()["title"] == "Private"


def test_pagination(client):
    headers = make_user(client, "A", "a@example.com")
    for i in range(5):
        client.post("/tasks", json={"title": f"Task {i}"}, headers=headers)

    res = client.get("/tasks?limit=2&offset=0", headers=headers).json()
    assert res["total"] == 5
    assert len(res["items"]) == 2

    res = client.get("/tasks?limit=2&offset=4", headers=headers).json()
    assert len(res["items"]) == 1  # last page is partial

    assert client.get("/tasks?limit=1000", headers=headers).status_code == 422


def test_filter_by_completed(client):
    headers = make_user(client, "A", "a@example.com")
    client.post("/tasks", json={"title": "Done", "completed": True}, headers=headers)
    client.post("/tasks", json={"title": "Open", "completed": False}, headers=headers)

    res = client.get("/tasks?completed=true", headers=headers).json()
    assert res["total"] == 1
    assert res["items"][0]["title"] == "Done"