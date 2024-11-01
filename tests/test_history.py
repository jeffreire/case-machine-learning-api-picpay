import unittest

from fastapi.testclient import TestClient

from src.main import app
from src.routes.classification_route import get_db


class MockInMemoryDatabase:
    def __init__(self, classifications=None):
        self.classifications = classifications or []

    def find(self):
        return self.classifications

def override_get_db():
    return MockInMemoryDatabase()

class TestHistoryModel(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
        app.dependency_overrides[get_db] = override_get_db

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_history_model_exception(self):
        class FaultyDatabase:
            def find(self):
                raise Exception("Database error")

        app.dependency_overrides[get_db] = lambda: FaultyDatabase()
        
        response = self.client.get("/model/history/")
        self.assertEqual(response.status_code, 500)
        self.assertIn("Erro ao obter o histórico:", response.json()['detail'])
