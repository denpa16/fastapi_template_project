from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session
from app.domains import (
    FacetFilterSet,
    IntegerFilter,
)
from app.models import Building

router = APIRouter(prefix="/buildings", tags=["Buildings"])


class BuildingFilter(FacetFilterSet):
    number = IntegerFilter()
    project = IntegerFilter()


@router.get("/")
async def list(
    filter: BuildingFilter = Depends(BuildingFilter),
    session: AsyncSession = async_session,
):
    result = await session.execute(select(Building))
    buildings = result.scalars().all()
    return buildings
