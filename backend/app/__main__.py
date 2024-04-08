from random import random, randrange
from uuid import UUID

from fastapi import FastAPI, Path
from sqlalchemy import delete, exc, insert, select, update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session
from app.models import Project

app = FastAPI()


@app.get("/projects/get_multiple")
async def get_multiple(session: AsyncSession = async_session):
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects


@app.get("/projects/{id}/get_one")
async def get_one(id: UUID = Path(alias="id"), session: AsyncSession = async_session):
    result = await session.execute(select(Project).where(Project.id == id))
    project = result.scalars().one()
    return project


@app.get("/projects/delete_multiple")
async def delete_multiple(session: AsyncSession = async_session):
    await session.execute(delete(Project))
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects


@app.get("/projects/{id}/delete_one")
async def delete_one(
    id: UUID = Path(alias="id"), session: AsyncSession = async_session
):
    result = await session.execute(delete(Project).where(Project.id == id))
    try:
        project = result.scalars().one()
    except exc.NoResultFound:
        project = None
    return project


@app.get("/projects/{id}/update_one")
async def update_one(
    id: UUID = Path(alias="id"),
    session: AsyncSession = async_session,
):
    update_data = {"name": f"name_{random()}"}
    await session.execute(update(Project).where(Project.id == id).values(**update_data))
    result = await session.execute(select(Project).where(Project.id == id))
    projects = result.scalars().one
    return projects


@app.get("/projects/update_multiple_by_pk")
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


@app.get("/projects/update_multiple_by_field")
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


@app.get("/projects/create_one")
async def create_one(session: AsyncSession = async_session):
    session.add(Project(name=f"name_{random()}"))
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects


@app.get("/projects/create_multiple")
async def create_multiple(session: AsyncSession = async_session):
    create_data = [{"name": "project_1"}, {"name": "project_2"}, {"name": "project_3"}]
    await session.execute(insert(Project).values(create_data))
    result = await session.execute(select(Project))
    projects = result.scalars().all()
    return projects
