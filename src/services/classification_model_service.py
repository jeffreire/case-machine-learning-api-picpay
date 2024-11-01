from datetime import datetime

from src.schemas.classification_schema import (
    ClassificationSchemaRequest,
    ClassificationSchemaResponse,
)


class ClassificationModelService:
    def __init__(self, model, db) -> None:
        self.model = model
        self.db = db
        self.labels = {
            0: "Iris-setosa",
            1: "Iris-versicolor",
            2: "Iris-virginica"
        }
    
    def classify(self, request : ClassificationSchemaRequest):
        input_data = request.to_dataframe()
        index_category_classify = self.model.predict(input_data)[0]
        category_classify = self.labels[index_category_classify]
        self.__save_classification(request, category_classify)
        return ClassificationSchemaResponse(category=category_classify)
    

    def __save_classification(self, request: ClassificationSchemaRequest, classify: float):
        self.db.classifications.insert_one({
            'sepal_length_cm': request.sepal_length_cm,
            'sepal_width_cm': request.sepal_width_cm,
            'petal_length_cm': request.petal_length_cm,
            'petal_width_cm': request.petal_width_cm,
            'classify': classify,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })