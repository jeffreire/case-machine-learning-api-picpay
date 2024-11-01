import pandas as pd
from pydantic import BaseModel, Field


class PredictSchemaRequest(BaseModel):
    sepalLengthCm : float = Field(..., description="Comprimento da sépala em centímetros.")
    sepalWidthCm : float = Field(..., description="Largura da sépala em centímetros.")
    petalLengthCm : int = Field(..., description="Comprimento da pétala em centímetros.")
    petalWidthCm : float = Field(..., description="Comprimento da pétala em centímetros.")
    
    def to_dataframe(self):
        request_dataframe = {
            "SepalLengthCm": self.sepalLengthCm,
            "SepalWidthCm": self.sepalWidthCm,
            "PetalLengthCm": self.petalLengthCm,
            "PetalWidthCm": self.petalWidthCm,
        }
        prediction_df = pd.DataFrame([request_dataframe])
        return prediction_df


class PredictSchemaResponse(BaseModel):
    category : str = Field(..., description="Categoria classificada da Flor")
    