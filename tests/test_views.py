from starlette.testclient import TestClient

from examples.main import app


def create(client):
    return client.post(
        "/user",
        json={"name": "test", "password": "test", "age": 25},
    )


def test_create():
    with TestClient(app) as client:
        response = create(client)
        assert response.status_code == 200
        assert response.json() == {"name": "test", "age": 25}


def test_list():
    with TestClient(app) as client:
        create(client)
        response = client.get(
            "/user",
        )
        assert response.status_code == 200
        assert response.json() == [{"age": 25, "name": "test"}]


def test_detail():
    with TestClient(app) as client:
        create(client)
        response = client.get(
            "/user/1",
        )
        assert response.status_code == 200
        assert response.json() == {"age": 25, "name": "test"}


def test_delete():
    with TestClient(app) as client:
        create(client)
        response = client.delete(
            "/user/1",
        )
        assert response.status_code == 200
        assert response.json() is None


def test_update():
    with TestClient(app) as client:
        create(client)
        response = client.put("/user/1", json={"name": "test2"})
        assert response.status_code == 200
        assert response.json() is None
