from random import random, randrange
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi import Path, Depends
from sqlalchemy import delete, exc, insert, select, update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session
from app.domains import (
    FacetFilterSet,
    CharInFilter,
    BooleanFilter,
    RelationshipFilter,
)
from app.models import Project

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/")
async def get_multiple(
    session: AsyncSession = async_session,
):
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects


class ProjectFilter(FacetFilterSet):
    name_s = CharInFilter(field_name="name", method="name_s_filter")
    alias = BooleanFilter()
    alias.facets = "get_alias_facets"
    buildings = RelationshipFilter(field_name="number")

    class Meta:
        model = Project

    def name_s_filter(self, query, name, value):
        return query

    def get_alias_facets(self, session):
        return ["sss", "eee"]


@router.get("/test")
async def get_test_multiple(
    _: Request,
    project_filter: ProjectFilter = Depends(ProjectFilter),
    session: AsyncSession = async_session,
):
    filter_query = project_filter(_)
    result = await session.execute(filter_query)
    projects = result.scalars().all()
    return projects


@router.get("/specs")
async def get_specs(
    _: Request,
    project_filter: ProjectFilter = Depends(ProjectFilter),
    session: AsyncSession = async_session,
):
    specs = await project_filter.specs(session)
    return specs


@router.get("/facets")
async def get_facets(
    _: Request,
    project_filter: ProjectFilter = Depends(ProjectFilter),
    session: AsyncSession = async_session,
):
    specs = await project_filter.facets(_, session)
    return specs


@router.get("/{id}")
async def get_one(id: UUID = Path(alias="id"), session: AsyncSession = async_session):
    result = await session.execute(select(Project).where(Project.id == id))
    project = result.scalars().one()
    return project


@router.get("/delete_multiple")
async def delete_multiple(session: AsyncSession = async_session):
    await session.execute(delete(Project))
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects


@router.get("/{id}/delete_one")
async def delete_one(
    id: UUID = Path(alias="id"), session: AsyncSession = async_session
):
    result = await session.execute(delete(Project).where(Project.id == id))
    try:
        project = result.scalars().one()
    except exc.NoResultFound:
        project = None
    return project


@router.get("/{id}/update_one")
async def update_one(
    id: UUID = Path(alias="id"),
    session: AsyncSession = async_session,
):
    update_data = {"name": f"name_{random()}"}
    await session.execute(update(Project).where(Project.id == id).values(**update_data))
    result = await session.execute(select(Project).where(Project.id == id))
    projects = result.scalars().one
    return projects


@router.get("/update_multiple_by_pk")
async def update_multiple_by_pk(session: AsyncSession = async_session):
    update_data = [
        {
            "id": "cebc78f1-3b69-4a48-b0c5-e95bec82f1d9",
            "name": f"name_m_upd_{randrange(1000, 10000)}",
            "alias": "som_alies",
        },
        {
            "id": "1ed6c6c5-63c0-4e3b-8f67-81758e73f0db",
            "name": f"name_m_upd_{randrange(1000, 10000)}",
            "alias": "som_alies",
        },
    ]
    await session.execute(update(Project), update_data)
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects


@router.get("/update_multiple_by_field")
async def update_multiple_by_field(session: AsyncSession = async_session):
    """TODO: надо выяснить, почему не работает."""
    update_data = [
        {"u_name": "project_2", "alias": f"its_new_alias_{randrange(1000, 10000)}"},
        {"u_name": "project_3", "alias": f"its_new_alias_{randrange(1000, 10000)}"},
    ]
    await session.execute(
        update(Project).where(Project.name == bindparam("u_name")), update_data
    )
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects


@router.get("/create_one")
async def create_one(session: AsyncSession = async_session):
    session.add(Project(name=f"name_{random()}"))
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects


@router.get("/create_multiple")
async def create_multiple(session: AsyncSession = async_session):
    create_data = [{"name": "project_1"}, {"name": "project_2"}, {"name": "project_3"}]
    await session.execute(insert(Project).values(create_data))
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects
