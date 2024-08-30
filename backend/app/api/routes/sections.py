from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session
from app.models import Section, Building

router = APIRouter(prefix="/sections", tags=["Sections"])


@router.get("/")
async def list(
    session: AsyncSession = async_session,
):
    result = await session.execute(
        select(Section)
        .where(
            Building.number == 1,
            Building.project_id == "cebc78f1-3b69-4a48-b0c5-e95bec82f1d9",
        )
        .distinct()
    )
    sections = result.scalars().all()
    return sections


@router.get("/create_multiple")
async def create_multiple(session: AsyncSession = async_session):
    create_data = []
    buildings = await session.execute(select(Building))
    buildings = buildings.scalars().all()
    for b in buildings:
        for i in range(5):
            create_data.append({"number": i, "building_id": b.id})
    result = await session.execute(select(Section))
    sections = result.scalars().all()
    return sections
