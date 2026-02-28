from .conftest import client, user_token
from .utils import auth_headers
from httpx import Response


def test_get_device(client, user_token):
    response: Response = client.get("/device", headers=auth_headers(user_token))
    assert response.status_code == 200


def test_delete_device(client, user_token):
    response: Response = client.delete("/device", headers=auth_headers(user_token))
    assert response.status_code == 204
