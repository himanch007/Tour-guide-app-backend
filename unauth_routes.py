from fastapi import APIRouter

from users.controllers.register import router as registration_router
from users.controllers.login import router as login_router
from tour_guide.controllers.shortest_path import router as shortest_path_router


api_router = APIRouter()

api_router.include_router(
    registration_router, prefix='/users/register', tags=['register'])
api_router.include_router(login_router, prefix='/users/login', tags=['login'])
api_router.include_router(shortest_path_router, prefix='/tour_guide/shortest-path', tags=['shortest-path'])
