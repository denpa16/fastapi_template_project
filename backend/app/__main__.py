from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from app.models import Song
from app.db import async_session

app = FastAPI()


@app.get("/users")
async def get_songs(session: AsyncSession = async_session):
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    return [songs]
