from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_predict_model_no_model_loaded():
    classification_request = {
        "sepal_length_cm": 1.0,
        "sepal_width_cm": 2.57,
        "petal_length_cm": 4.0,
        "petal_width_cm": 1.0
    }
    
    response = client.post("/model/classify/", json=classification_request)

    assert response.status_code == 503
    assert response.json() == {
        "detail": "O modelo de classificação não está carregado. Carregue o modelo antes de fazer as classificações."
    }

def test_load_model_success():
    model_path = "./tests/models/Iris.pkl"
    with open(model_path, "rb") as model_file:
        response = client.post("/model/load/", files={"model": model_file})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Modelo carregado com sucesso!"}

def test_load_model_invalid_file():
    invalid_file_path = "./tests/models/model_test_error.txt"

    with open(invalid_file_path, "rb") as model_file:
        response = client.post("/model/load/", files={"model": model_file})

    assert response.status_code == 500
    assert response.json() == {
        'detail': 'Erro ao carregar o modelo: 400: O arquivo de modelo é inválido. Por favor, verifique e tente novamente.'
    }

def test_predict_model_success():
    with open("./tests/models/Iris.pkl", "rb") as model_file:
        client.post("/model/load/", files={"model": model_file})
    
    classification_request = {
        "sepal_length_cm": 1.0,
        "sepal_width_cm": 2.57,
        "petal_length_cm": 4.0,
        "petal_width_cm": 1.0
    }
    
    response = client.post("/model/classify/", json=classification_request)

    assert response.status_code == 200
    assert "category" in response.text
    assert '{"category":"Iris-versicolor"}' == response.text

def test_predict_model_internal_server_error():
    classification_request = {
        "sepal_length_cm": 1.0,
        "sepal_width_cm": 2.57,
        "petal_length_cm": 4.0,
        "petal_width_cm": 1.0
    }
    
    with patch("src.services.classification_model_service.ClassificationModelService.classify", side_effect=Exception("Erro simulado")):
        response = client.post("/model/classify/", json=classification_request)
        
        assert response.status_code == 500
        assert response.json() == {
            "detail": "Erro ao realizar a classificação: Erro simulado"
        }
