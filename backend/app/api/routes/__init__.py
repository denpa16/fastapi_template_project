from fastapi import APIRouter

from .projects import router as projects_router

api_router = APIRouter(prefix="/api")
api_router.include_router(projects_router)
