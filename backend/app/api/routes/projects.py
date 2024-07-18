from typing import Any

from random import random, randrange
from uuid import UUID

from fastapi import APIRouter
from fastapi import Path
from pydantic import Field
from sqlalchemy import delete, exc, insert, select, update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter

from app.db import async_session
from app.models import Project

router = APIRouter(prefix="/projects", tags=["Projects"])


class FacetFilterSet(Filter):
    """Класс фильтра с фасетами."""

    class Constants(Filter.Constants):
        model: Any
        specs_methods: dict = {}
        specs_skip: list = []

    async def get_choices(self, field_name, session):
        result = await session.execute(
            select(
                getattr(self.Constants.model, "id"),
                getattr(self.Constants.model, field_name),
            )
        )
        return [{"label": item[0], "value": item[1]} for item in result.fetchall()]

    async def specs(self, session):
        specs = []
        for field_name, _ in self.model_dump().items():
            if field_name in self.Constants.specs_skip:
                continue
            if method := self.Constants.specs_methods.get(field_name):
                specs.append(
                    {
                        "name": field_name,
                        "choices": await getattr(self, method)(session),
                    }
                )
                continue
            specs.append(
                {
                    "name": field_name,
                    "choices": await self.get_choices(field_name, session),
                }
            )

        return specs


class ProjectFilter(FacetFilterSet):
    name: str | None = Field(alias="names", default=None)

    class Constants(FacetFilterSet.Constants):
        model = Project

    class Config:
        populate_by_name = True
        specs_methods: dict = {}
        specs_skip: list = []

    async def get_name_specs(self, session):
        result = await session.execute(
            select(
                getattr(self.Constants.model, "alias"),
                getattr(self.Constants.model, "name"),
            )
        )
        return [{"label": item[0], "value": item[1]} for item in result.fetchall()]


@router.get("/")
async def get_multiple(
    project_filter: ProjectFilter = FilterDepends(ProjectFilter),
    session: AsyncSession = async_session,
):
    query = project_filter.filter(select(Project))
    result = await session.execute(query)
    projects = result.scalars().all()
    return projects


@router.get("/specs")
async def get_specs(
    project_filter: ProjectFilter = FilterDepends(ProjectFilter),
    session: AsyncSession = async_session,
):
    specs = await project_filter.specs(session)
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
