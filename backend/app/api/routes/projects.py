from random import random, randrange
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi import Path, Depends
from pydantic import Field
from sqlalchemy import delete, exc, insert, select, update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends

from app.db import async_session
from app.domains import FacetFilterSet
from app.models import Project

router = APIRouter(prefix="/projects", tags=["Projects"])


class ProjectFilter(FacetFilterSet):
    name: str | None = Field(alias="names", default=None)

    class Constants(FacetFilterSet.Constants):
        model = Project
        specs_methods: dict = {
            "name": "get_name_specs",
        }
        specs_skip: list = []
        facets_methods: dict = {
            "name": "get_name_facets",
        }
        facets_skip: list = []

    class Config:
        populate_by_name = True

    async def get_name_specs(self, session):
        result = await session.execute(
            select(
                getattr(self.Constants.model, "alias"),
                getattr(self.Constants.model, "name"),
            )
        )
        return [{"label": item[0], "value": item[1]} for item in result.fetchall()]

    async def get_name_facets(self, result):
        return [item.name for item in result]


@router.get("/")
async def get_multiple(
    filter: ProjectFilter = FilterDepends(ProjectFilter),
    session: AsyncSession = async_session,
):
    query = filter.filter(select(Project))
    result = await session.execute(query)
    projects = result.scalars().all()
    return projects


class BaseFilter:
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
    ):
        if lookup_expr is None:
            lookup_expr = "__eq__"
        self.field_name = field_name
        self.lookup_expr = lookup_expr


class BaseInFilter:
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
    ):
        if lookup_expr is None:
            lookup_expr = "in_"
        self.field_name = field_name
        self.lookup_expr = lookup_expr


class BaseRangeFilter:
    """TODO: _max и _min надо сделать."""

    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
    ):
        if lookup_expr is None:
            lookup_expr = "range_"
        self.field_name = field_name
        self.lookup_expr = lookup_expr


class IntegerFilter(BaseFilter): ...


class IntegerInFilter(BaseFilter): ...


class RangeFilter(BaseRangeFilter): ...


class CharFilter(BaseFilter): ...


class CharInFilter(BaseInFilter): ...


class FilterSet:
    def __filter(self):
        query = select(self.Meta.model)
        _filters = self.__get_filters()
        for key, value in self.__query_params:
            if _filter := _filters.get(key):
                try:
                    model_field = getattr(self.Meta.model, key)
                except AttributeError:
                    continue
                if isinstance(_filter, BaseFilter):
                    query = query.filter(
                        getattr(model_field, _filter.lookup_expr)(value)
                    )
                if isinstance(_filter, BaseInFilter):
                    query = query.filter(
                        getattr(model_field, _filter.lookup_expr)(value.split(","))
                    )
        return query

    @classmethod
    def __filter_list(cls):
        return cls.__dict__.keys()

    def __get_filters(self):
        filters = {}
        for key in self.__filter_list():
            attr = getattr(self, key)
            if isinstance(attr, BaseFilter | BaseInFilter):
                filters[key] = attr
        return filters

    def __call__(self, request, *args, **kwargs):
        self.__query_params = request.query_params.items()
        return self.__filter()

    class Meta:
        model = None


class TProjectFilter(FilterSet):
    name = CharInFilter()
    alias = CharInFilter()

    class Meta:
        model = Project


@router.get("/test")
async def get_test_multiple(
    _: Request,
    project_filter: TProjectFilter = Depends(TProjectFilter),
    session: AsyncSession = async_session,
):
    sm = project_filter(_)
    result = await session.execute(sm)
    projects = result.scalars().all()
    return projects


@router.get("/specs")
async def get_specs(
    project_filter: ProjectFilter = FilterDepends(ProjectFilter),
    session: AsyncSession = async_session,
):
    specs = await project_filter.specs(session)
    return specs


@router.get("/facets")
async def get_facets(
    project_filter: ProjectFilter = FilterDepends(ProjectFilter),
    session: AsyncSession = async_session,
):
    query = project_filter.filter(select(Project))
    facets = await project_filter.facets(session, query)
    return facets


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
