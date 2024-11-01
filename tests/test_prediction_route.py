from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_predict_model_no_model_loaded():
    prediction_request = {
        "sepalLengthCm": 1.0,
        "sepalWidthCm": 2.57,
        "petalLengthCm": 4.0,
        "petalWidthCm": 1.0
    }
    
    response = client.post("/model/predict/", json=prediction_request)

    assert response.status_code == 503
    assert response.json() == {
        "detail": "O modelo de predição não está carregado. Carregue o modelo antes de fazer previsões."
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
    
    prediction_request = {
        "sepalLengthCm": 1.0,
        "sepalWidthCm": 2.57,
        "petalLengthCm": 4.0,
        "petalWidthCm": 1.0
    }
    
    response = client.post("/model/predict/", json=prediction_request)

    assert response.status_code == 200
    assert "category" in response.text
    assert '{"category":"Iris-versicolor"}' == response.text

def test_predict_model_internal_server_error():
    prediction_request = {
        "sepalLengthCm": 1.0,
        "sepalWidthCm": 2.57,
        "petalLengthCm": 4.0,
        "petalWidthCm": 1.0
    }
    with patch("src.services.prediction_model_service.PredictModelService.predict", side_effect=Exception("Erro simulado")):
        response = client.post("/model/predict/", json=prediction_request)
        
        assert response.status_code == 500
        assert response.json() == {
            "detail": "Erro ao realizar a previsão: Erro simulado"
        }