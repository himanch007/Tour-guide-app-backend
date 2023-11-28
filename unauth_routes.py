from fastapi import APIRouter

from tour_guide.controllers.shortest_path import router as shortest_path_router


api_router = APIRouter()

api_router.include_router(shortest_path_router, prefix='/tour_guide/shortest-path', tags=['shortest-path'])
