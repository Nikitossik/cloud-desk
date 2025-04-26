from .conftest import client, user_token
from .utils import auth_headers
from httpx import Response


def test_unathorized_user(client):
    response: Response = client.get("/auth/me")
    assert response.status_code == 401


def test_register_user(client):
    response: Response = client.post(
        "/auth/signup",
        json={
            "name": "Test",
            "surname": "Test",
            "email": "testuser@gmail.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test"
    assert response.json()["surname"] == "Test"
    assert response.json()["email"] == "testuser@gmail.com"


def test_user_already_exists(client):
    response: Response = client.post(
        "/auth/signup",
        json={
            "name": "Test",
            "surname": "Test",
            "email": "testuser@gmail.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 422


def test_auth_me(client, user_token):
    response: Response = client.get("/auth/me", headers=auth_headers(user_token))
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@gmail.com"
