from .conftest import client, user_token, test_applications
from .utils import auth_headers
from httpx import Response


def test_create_session(client, user_token):
    response: Response = client.post(
        "/session",
        headers=auth_headers(user_token),
        json={
            "name": "working session",
            "description": "my first session",
            "enable_tracking": False,
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "working session"
    assert response.json()["slugname"] == "working-session"
    assert response.json()["is_active"] is True
    assert response.json()["is_tracking"] is False


def test_get_session_by_slug(client, user_token):
    response: Response = client.get(
        "/session/working-session",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 200
    assert response.json()["name"] == "working session"
    assert response.json()["slugname"] == "working-session"
    assert response.json()["is_active"] is True
    assert response.json()["is_tracking"] is False


def test_clone_active_session(client, user_token, test_applications):
    response: Response = client.post(
        "/active-session/clone",
        headers=auth_headers(user_token),
        json={
            "name": "working session clone",
            "description": "the new active session clone",
            "enable_tracking": False,
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "working session clone"
    assert response.json()["slugname"] == "working-session-clone"
    assert response.json()["is_active"] is True
    assert response.json()["is_tracking"] is False


def test_get_active_session(client, user_token):
    response: Response = client.get("/active-session", headers=auth_headers(user_token))
    assert response.status_code == 200
    assert response.json()["name"] == "working session clone"
    assert response.json()["slugname"] == "working-session-clone"
    assert response.json()["is_active"] is True
    assert response.json()["is_tracking"] is False


def test_get_all_sessions(client, user_token):
    response: Response = client.get(
        "/session",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_deactivate_active_session(client, user_token):
    response: Response = client.post(
        "/active-session/deactivate",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 201
    assert response.json()["name"] == "working session clone"
    assert response.json()["slugname"] == "working-session-clone"
    assert response.json()["is_active"] is False
    assert response.json()["is_tracking"] is False


def test_not_found_active_session(client, user_token):
    response: Response = client.get(
        "/active-session",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 404


def test_activate_session_by_slug(client, user_token):
    response: Response = client.post(
        "/session/working-session/activate",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 200
    assert response.json()["name"] == "working session"
    assert response.json()["slugname"] == "working-session"
    assert response.json()["is_active"] is True
    assert response.json()["is_tracking"] is False


def test_delete_active_session(client, user_token):
    response: Response = client.delete(
        "/active-session",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 204


def test_delete_session_by_slug(client, user_token):
    response: Response = client.delete(
        "/session/working-session-clone",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 204


def test_get_all_sessions_empty(client, user_token):
    response: Response = client.get(
        "/session",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 200
    assert len(response.json()) == 0
