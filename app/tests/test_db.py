import os
import sys

from fastapi.testclient import TestClient
from sqlalchemy import text

sys.path.append(os.getcwd())

from app.core.database.db import engine
from app.main import app

client = TestClient(app)


def test_db():
    try:
        connection = engine.connect()
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1
        connection.close()
        print("Connection successful")
    except Exception as exc:
        print(exc)


def test_health():
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
