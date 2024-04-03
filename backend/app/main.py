import uvicorn
from fastapi import FastAPI


def get_fastapi_app() -> FastAPI:
    app_ = FastAPI(
        title="App title",
        description="App description",
        version="App version",
        docs_url="App docs url",
    )
    return app_


app: FastAPI = get_fastapi_app()


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
