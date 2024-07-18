from fastapi import APIRouter
from pydantic import Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends

from app.db import async_session
from app.domains import FacetFilterSet
from app.models import Building

router = APIRouter(prefix="/buildings", tags=["Buildings"])


class BuildingFilter(FacetFilterSet):
    number: str | None = Field(alias="number", default=None)
    project: str | None = Field(alis="project", default=None)

    class Constants(FacetFilterSet.Constants):
        model = Building

    class Config:
        populate_by_name = True


@router.get("/")
async def list(
    filter: BuildingFilter = FilterDepends(BuildingFilter),
    session: AsyncSession = async_session,
):
    query = filter.filter(select(Building))
    result = await session.execute(query)
    buildings = result.scalars().all()
    return buildings


@router.get("/specs")
async def specs(
    filter: BuildingFilter = FilterDepends(BuildingFilter),
    session: AsyncSession = async_session,
):
    specs = await filter.specs(session)
    return specs


@router.get("/facets")
async def facets(
    filter: Building = FilterDepends(BuildingFilter),
    session: AsyncSession = async_session,
):
    query = filter.filter(select(Building))
    facets = await filter.facets(session, query)
    return facets
