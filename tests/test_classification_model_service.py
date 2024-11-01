import unittest
from unittest.mock import MagicMock, patch

import joblib

from src.services.manager_model_service import (
    ManagerModelService,  # Update with your actual import path
)


class TestManagerModelService(unittest.TestCase):
    
    def setUp(self):
        self.service = ManagerModelService()

    @patch('joblib.load')
    def test_load_model_success(self, mock_load):
        mock_model = MagicMock()
        mock_model.filename = 'model.pkl'
        mock_model.file = 'dummy_path/model.pkl'
        
        mock_load.return_value = "Mocked Model"
        
        result = self.service.load_model(mock_model)

        self.assertTrue(result)
        self.assertEqual(self.service.get_model(), "Mocked Model")
        mock_load.assert_called_once_with(mock_model.file)

    def test_load_model_invalid_filetype(self):
        mock_model = MagicMock()
        mock_model.filename = 'model.txt'
        mock_model.file = 'dummy_path/model.txt'
        
        result = self.service.load_model(mock_model)

        self.assertFalse(result)
        self.assertIsNone(self.service.get_model())

    def test_get_model_no_model_loaded(self):
        self.assertIsNone(self.service.get_model())
