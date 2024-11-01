from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def add_custom_openapi(app: FastAPI) -> None:
    openapi_schema = get_openapi(
        title="Iris Species Prediction API",
        version="1.0.0",
        description="Iris Species Prediction API",
        routes=app.routes,
        servers=[{"url": "http://localhost:8000"}],
    )
    
    app.openapi_schema = openapi_schema