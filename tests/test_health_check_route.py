from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_health_check_sucess():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "health", "message": "Connection successful!"}