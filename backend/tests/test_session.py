from .conftest import client, user_token
from .utils import auth_headers
from httpx import Response


def create_session(client, user_token, *, name="working session", start=True):
    return client.post(
        "/session/",
        headers=auth_headers(user_token),
        json={
            "name": name,
            "description": "my first session",
            "start": start,
        },
    )


def test_create_session(client, user_token):
    response: Response = create_session(client, user_token)
    assert response.status_code == 201
    assert response.json()["name"] == "working session"
    assert response.json()["slugname"] == "working-session"
    assert response.json()["is_active"] is True


def test_get_session_by_slug(client, user_token):
    create_session(client, user_token)

    response: Response = client.get(
        "/session/by-slug/working-session",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 200
    assert response.json()["name"] == "working session"
    assert response.json()["slugname"] == "working-session"
    assert response.json()["is_active"] is True


def test_get_active_session(client, user_token):
    create_session(client, user_token)

    response: Response = client.get("/session/active", headers=auth_headers(user_token))
    assert response.status_code == 200
    assert response.json()["name"] == "working session"
    assert response.json()["slugname"] == "working-session"
    assert response.json()["is_active"] is True


def test_get_all_sessions(client, user_token):
    create_session(client, user_token)

    response: Response = client.get(
        "/session/",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_deactivate_active_session(client, user_token):
    create_session(client, user_token)

    response: Response = client.post(
        "/session/active/stop",
        headers=auth_headers(user_token),
    )
    assert response.status_code in (200, 201)
    assert response.json()["name"] == "working session"
    assert response.json()["slugname"] == "working-session"
    assert response.json()["is_active"] is False


def test_not_found_active_session(client, user_token):
    create_session(client, user_token, start=False)

    response: Response = client.get(
        "/session/active",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 404


def test_activate_session_by_slug(client, user_token):
    create_session(client, user_token, start=False)

    response: Response = client.post(
        "/session/by-slug/working-session/start",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 200
    assert response.json()["name"] == "working session"
    assert response.json()["slugname"] == "working-session"
    assert response.json()["is_active"] is True


def test_delete_active_session(client, user_token):
    create_session(client, user_token)

    response: Response = client.delete(
        "/session/active",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 204


def test_delete_session_by_slug(client, user_token):
    create_session(client, user_token)

    response: Response = client.delete(
        "/session/by-slug/working-session",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 204


def test_get_all_sessions_empty(client, user_token):
    response: Response = client.get(
        "/session/",
        headers=auth_headers(user_token),
    )
    assert response.status_code == 200
    assert len(response.json()) == 0
