from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from app.models import Project
from app.db import async_session

app = FastAPI()


@app.get("/projects")
async def get_list(session: AsyncSession = async_session):
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects
