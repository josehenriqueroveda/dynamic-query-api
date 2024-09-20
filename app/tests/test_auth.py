import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.getcwd())

from app.core.database.db import engine
from app.main import app

client = TestClient(app)


def test_login():
    response = client.post(
        "/api/v1/auth/login", data={"username": "testuser", "password": "TEST@door321"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_me():
    login_response = client.post(
        "/api/v1/auth/login", data={"username": "testuser", "password": "TEST@door321"}
    )
    token = login_response.json()["access_token"]
    response = client.get(
        "/api/v1/user/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "user": "testuser",
        "is_admin": False,
        "token": f"Bearer {token}",
    }


def test_logout():
    login_response = client.post(
        "/api/v1/auth/login", data={"username": "testuser", "password": "TEST@door321"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    print(token)

    logout_response = client.get(
        "/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"}
    )
    assert logout_response.status_code == 200
    assert logout_response.json() == {"message": "Logged out"}

    protected_route_response = client.get(
        "/api/v1/user/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert protected_route_response.status_code == 401
