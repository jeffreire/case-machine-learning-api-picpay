from datetime import datetime

from src.schemas.prediction_schema import PredictSchemaRequest, PredictSchemaResponse


class PredictModelService:
    def __init__(self, model) -> None:
        self.model = model
        self.labels = {
            0: "Iris-setosa",
            1: "Iris-versicolor",
            2: "Iris-virginica"
        }
    
    def predict(self, request : PredictSchemaRequest):
        input_data = request.to_array2d()
        category_predict = self.model.predict(input_data)[0]
        return PredictSchemaResponse(category=self.labels[category_predict])