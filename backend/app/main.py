from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def start_page() -> str:
    """Тестовый апи."""
    return f"Start Page"
