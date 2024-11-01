from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from src.db.database import InMemoryDatabase
from src.schemas.classification_schema import (
    ClassificationSchemaRequest,
    ClassificationSchemaResponse,
    HistorySchema,
    HistorySchemaResponse,
)
from src.services.classification_model_service import ClassificationModelService
from src.services.manager_model_service import ManagerModelService

router = APIRouter(tags=["Classification Model"])

db = InMemoryDatabase()
manager_model_service = ManagerModelService()
prediction_schema_service = None

def get_db():
    return db

def get_manager_model():
    return manager_model_service

def get_classification_model_service():
    return prediction_schema_service


@router.post("/model/load/", status_code=status.HTTP_200_OK)
def load_model(
    model: UploadFile = File(...),
    manager_model: ManagerModelService = Depends(get_manager_model),
    db: InMemoryDatabase = Depends(get_db)
) -> dict:
    global prediction_schema_service
    try:
        if manager_model.load_model(model):
            prediction_schema_service = ClassificationModelService(manager_model.get_model(), db)
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

@router.post("/model/classify/", response_model=ClassificationSchemaResponse)
def predict_model(
    predict_model_request: ClassificationSchemaRequest,
    prediction_model_service: ClassificationModelService = Depends(get_classification_model_service)
) -> ClassificationSchemaResponse:
    if prediction_model_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="O modelo de classificação não está carregado. Carregue o modelo antes de fazer as classificações."
        )
    
    try:
        predict_response = prediction_model_service.classify(predict_model_request)
        return predict_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao realizar a classificação: {str(e)}"
        )

@router.get("/model/history/", response_model=HistorySchemaResponse)
def history_model(db: InMemoryDatabase = Depends(get_db)) -> HistorySchemaResponse:
    try:
        classifications = list(db.classifications.find())
        if not classifications:
            raise HTTPException(status_code=404, detail="Nenhuma classificação!")

        history = [HistorySchema(**classification) for classification in classifications]
        history_response_model = HistorySchemaResponse(history=history)
        return history_response_model
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter o histórico: {e}")