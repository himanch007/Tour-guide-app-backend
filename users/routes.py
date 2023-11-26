from fastapi import APIRouter

from .controllers.user_details import router as user_details_router


api_router = APIRouter()

api_router.include_router(user_details_router, prefix='/user-details', tags=['user-details'])
