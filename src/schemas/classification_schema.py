from typing import List

import pandas as pd
from pydantic import BaseModel, Field


class ClassificationSchemaRequest(BaseModel):
    sepal_length_cm: float = Field(..., description="Comprimento da sépala em centímetros.")
    sepal_width_cm: float = Field(..., description="Largura da sépala em centímetros.")
    petal_length_cm: int = Field(..., description="Comprimento da pétala em centímetros.")
    petal_width_cm: float = Field(..., description="Largura da pétala em centímetros.")

    def to_dataframe(self) -> pd.DataFrame:
        """Converte o pedido de predição em um DataFrame do pandas."""
        return pd.DataFrame([{
            "SepalLengthCm": self.sepal_length_cm,
            "SepalWidthCm": self.sepal_width_cm,
            "PetalLengthCm": self.petal_length_cm,
            "PetalWidthCm": self.petal_width_cm,
        }])


class ClassificationSchemaResponse(BaseModel):
    category: str = Field(..., description="Categoria classificada da flor.")


class HistorySchema(BaseModel):
    petal_length_cm: int = Field(..., description="Comprimento da sépala em centímetros.")
    sepal_width_cm: float = Field(..., description="Largura da sépala em centímetros.")
    petal_length_cm: float = Field(..., description="Comprimento da pétala em centímetros.")
    petal_width_cm: float = Field(..., description="Largura da pétala em centímetros.")
    classify: str = Field(..., description="Label classificado pelo modelo")
    timestamp: str = Field(..., description="Horario da inferência")


class HistorySchemaResponse(BaseModel):
    history: List[HistorySchema] = Field(..., description="Histórico de inferencia do modelo.")
