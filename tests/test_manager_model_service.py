import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock

from src.schemas.classification_schema import (
    ClassificationSchemaRequest,
    ClassificationSchemaResponse,
)
from src.services.classification_model_service import (
    ClassificationModelService,  # Update with your actual import path
)


class TestClassificationModelService(unittest.TestCase):
    
    def setUp(self):
        self.mock_model = Mock()
        self.mock_db = Mock()
        
        self.service = ClassificationModelService(self.mock_model, self.mock_db)

    def test_classify_success(self):
        request = ClassificationSchemaRequest(sepal_length_cm=5.1, sepal_width_cm=3.5, 
                                               petal_length_cm=1, petal_width_cm=0.2)
        expected_label = "Iris-setosa"
        
        self.mock_model.predict.return_value = [0]

        response = self.service.classify(request)

        self.assertIsInstance(response, ClassificationSchemaResponse)
        self.assertEqual(response.category, expected_label)

        self.mock_db.classifications.insert_one.assert_called_once()
        inserted_data = self.mock_db.classifications.insert_one.call_args[0][0]
        self.assertEqual(inserted_data['sepal_length_cm'], request.sepal_length_cm)
        self.assertEqual(inserted_data['sepal_width_cm'], request.sepal_width_cm)
        self.assertEqual(inserted_data['petal_length_cm'], request.petal_length_cm)
        self.assertEqual(inserted_data['petal_width_cm'], request.petal_width_cm)
        self.assertEqual(inserted_data['classify'], expected_label)
        self.assertTrue('timestamp' in inserted_data)

    def test_save_classification(self):
        request = ClassificationSchemaRequest(sepal_length_cm=5.1, sepal_width_cm=3.5, 
                                               petal_length_cm=1, petal_width_cm=0.2)
        expected_classify = "Iris-setosa"

        self.service._ClassificationModelService__save_classification(request, expected_classify)

        self.mock_db.classifications.insert_one.assert_called_once()
        inserted_data = self.mock_db.classifications.insert_one.call_args[0][0]
        self.assertEqual(inserted_data['sepal_length_cm'], request.sepal_length_cm)
        self.assertEqual(inserted_data['sepal_width_cm'], request.sepal_width_cm)
        self.assertEqual(inserted_data['petal_length_cm'], request.petal_length_cm)
        self.assertEqual(inserted_data['petal_width_cm'], request.petal_width_cm)
        self.assertEqual(inserted_data['classify'], expected_classify)
        self.assertTrue('timestamp' in inserted_data)

