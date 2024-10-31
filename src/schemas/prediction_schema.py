import pandas as pd
from pydantic import BaseModel, Field


class PredictSchemaRequest(BaseModel):
    sepalLengthCm : float = Field(..., description="Comprimento da sépala em centímetros.")
    sepalWidthCm : float = Field(..., description="Largura da sépala em centímetros.")
    petalLengthCm : int = Field(..., description="Comprimento da pétala em centímetros.")
    petalWidthCm : float = Field(..., description="Comprimento da pétala em centímetros.")
    
    def to_array2d(self):
        request_dataframe = [[
            self.sepalLengthCm,
            self.sepalWidthCm,
            self.petalLengthCm,
            self.petalWidthCm,
        ]]
        return request_dataframe


class PredictSchemaResponse(BaseModel):
    category : str = Field(..., description="Categoria classificada da Flor")
    