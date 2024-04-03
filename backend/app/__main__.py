import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api import routers
from app.config import settings


app: FastAPI = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.app.secret_key)
app.include_router(routers.router)


if __name__ == "__main__":
    uvicorn.run("app.__main__:app", reload=True)
