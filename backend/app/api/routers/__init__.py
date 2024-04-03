from fastapi import APIRouter

from .healthcheck import router as healtcheck_router

router = APIRouter()
router.include_router(healtcheck_router)
