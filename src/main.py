from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.core.openapi import add_custom_openapi
from src.routes import health_check_route, prediction_route

app = FastAPI()


app.include_router(health_check_route.router)
app.include_router(prediction_route.router)
add_custom_openapi(app)

@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse("/docs")