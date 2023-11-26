from urllib.request import Request
from fastapi.responses import JSONResponse

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        return JSONResponse(
            {"message": "Internal server error"},
        status_code=500)