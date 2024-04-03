from fastapi import APIRouter


router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])


@router.get("/", status_code=200)
def healthcheck() -> dict[str, str | int]:
    """Healthcheck."""
    return {"status": 200, "message": "OK"}
