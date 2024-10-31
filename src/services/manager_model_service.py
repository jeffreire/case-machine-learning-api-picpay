from typing import Any

import joblib


class ManagerModelService:

    def load_model(self, model) -> bool:
        if model.filename.endswith('.pkl'):
            self.pickle_model = joblib.load(model.file)
            return True
        return False
    
    def get_model(self) -> Any:
        return self.pickle_model