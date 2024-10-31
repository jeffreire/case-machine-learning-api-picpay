from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Health-check"])

@router.get("/health", response_class=JSONResponse)
def health_check():
    try:
        return JSONResponse(status_code=200, content={"status": "health", "message": "Connection successful!"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})