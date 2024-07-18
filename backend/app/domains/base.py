from typing import Any

from sqlalchemy import select
from fastapi_filter.contrib.sqlalchemy import Filter


class FacetFilterSet(Filter):
    """Класс фильтра с фасетами."""

    class Constants(Filter.Constants):
        model: Any
        specs_methods: dict = {}
        specs_skip: list = []
        facets_methods: dict = {}
        facets_skip: list = []

    async def get_spec_choices(self, field_name, session):
        result = await session.execute(
            select(
                getattr(self.Constants.model, "id"),
                getattr(self.Constants.model, field_name),
            )
        )
        return [{"label": item[0], "value": item[1]} for item in result.fetchall()]

    async def get_facet_choices(self, field_name, result):
        return [getattr(item, field_name) for item in result]

    async def specs(self, session):
        specs = []
        for field_name, _ in self.model_dump().items():
            if field_name in self.Constants.specs_skip:
                continue
            elif method := self.Constants.specs_methods.get(field_name):
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
                    "choices": await self.get_spec_choices(field_name, session),
                }
            )

        return specs

    async def facets(self, session, query):
        query_res = await session.execute(query)
        result = query_res.scalars().all()
        facets = []
        for field_name, _ in self.model_dump().items():
            if field_name in self.Constants.facets_skip:
                continue
            elif method := self.Constants.facets_methods.get(field_name):
                facets.append(
                    {
                        "name": field_name,
                        "choices": await getattr(self, method)(result),
                    }
                )
                continue
            facets.append(
                {
                    "name": field_name,
                    "choices": await self.get_facet_choices(field_name, result),
                }
            )
        count = len(result)
        return {"facets": facets, "count": count}
