from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_register_success() -> None:
    response = client.post("/auth/register", json={"username": "minda"})
    assert response.status_code == 200
    assert response.json()["message"] == "register success"


def test_register_duplicate_user() -> None:
    client.post("/auth/register", json={"username": "repeat_user"})
    response = client.post("/auth/register", json={"username": "repeat_user"})
    assert response.status_code == 400


def test_login_success() -> None:
    response = client.post("/auth/login")
    assert response.status_code == 200
    assert response.json()["data"]["access_token"] == "demo-token"


def test_list_users() -> None:
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)


def test_create_article() -> None:
    response = client.post("/articles", json={"title": "FastAPI 测试文章"})
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "FastAPI 测试文章"
