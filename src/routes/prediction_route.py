from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from src.schemas.prediction_schema import PredictSchemaRequest, PredictSchemaResponse
from src.services.manager_model_service import ManagerModelService
from src.services.prediction_model_service import PredictModelService

router = APIRouter(tags=["Prediction Model"])

manager_model_service = ManagerModelService()
prediction_schema_service = None

def get_manager_model():
    return manager_model_service

def get_prediction_model_service():
    return prediction_schema_service


@router.post("/model/load/", status_code=status.HTTP_200_OK)
def load_model(
    model: UploadFile = File(...),
    manager_model: ManagerModelService = Depends(get_manager_model)
) -> dict:
    global prediction_schema_service
    try:
        if manager_model.load_model(model):
            prediction_schema_service = PredictModelService(manager_model.get_model())
            return {"message": "Modelo carregado com sucesso!"}

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo de modelo é inválido. Por favor, verifique e tente novamente."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar o modelo: {str(e)}"
        )

@router.post("/model/predict/", response_model=PredictSchemaResponse)
def predict_model(
    predict_model_request: PredictSchemaRequest,
    prediction_model_service: PredictModelService = Depends(get_prediction_model_service)
) -> PredictSchemaResponse:
    if prediction_model_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="O modelo de predição não está carregado. Carregue o modelo antes de fazer previsões."
        )
    
    try:
        predict_response = prediction_model_service.predict(predict_model_request)
        return predict_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao realizar a previsão: {str(e)}"
        )
