from sqlalchemy import select


class BaseFilter:
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        method: str | None = None,
        **kwargs,
    ):
        if lookup_expr is None:
            lookup_expr = "__eq__"
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.method = method
        self.extra = kwargs
        self.extra.setdefault("required", False)


class BaseInFilter:
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        method: str | None = None,
        **kwargs,
    ):
        if lookup_expr is None:
            lookup_expr = "in_"
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.method = method
        self.extra = kwargs
        self.extra.setdefault("required", False)


class BaseRangeFilter:
    """TODO: _max и _min надо сделать."""

    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        method: str | None = None,
        **kwargs,
    ):
        if lookup_expr is None:
            lookup_expr = "range_"
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.method = method
        self.extra = kwargs
        self.extra.setdefault("required", False)


class IntegerFilter(BaseFilter): ...


class IntegerInFilter(BaseFilter): ...


class RangeFilter(BaseRangeFilter): ...


class CharFilter(BaseFilter): ...


class CharInFilter(BaseInFilter): ...


class BooleanFilter(BaseFilter): ...


class RelationshipFilter:
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        method: str | None = None,
        **kwargs,
    ):
        if lookup_expr is None:
            lookup_expr = "range_"
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.method = method
        self.extra = kwargs
        self.extra.setdefault("required", False)


class BaseFilterSet:
    def filter(self):
        query = select(self.Meta.model)
        _filters = self.get_filters()
        for key, value in self.query_params:
            if _filter := _filters.get(key):
                key = _filter.field_name if _filter.field_name else key
                try:
                    model_field = getattr(self.Meta.model, key)
                except AttributeError:
                    continue
                if _filter.method:
                    try:
                        query = getattr(self, _filter.method)(query, key, value)
                    except AttributeError:
                        raise AttributeError
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
    def filter_list(cls):
        return cls.__dict__.keys()

    def get_filters(self):
        filters = {}
        for key in self.filter_list():
            attr = getattr(self, key)
            if isinstance(attr, BaseFilter | BaseInFilter):
                filters[key] = attr
        return filters

    def __call__(self, request, *args, **kwargs):
        self.query_params = request.query_params.items()
        return self.filter()

    class Meta:
        model = None


class FacetFilterSet(BaseFilterSet):
    async def get_spec_choices(self, field_name, session):
        result = await session.execute(
            select(
                getattr(self.Meta.model, "id"),
                getattr(self.Meta.model, field_name),
            )
        )
        return [{"label": item[0], "value": item[1]} for item in result.fetchall()]

    async def specs(self, session):
        specs = []
        for filter_name, _filter in self.get_filters().items():
            name = _filter.field_name if _filter.field_name else filter_name
            _filter_spec_skip = (
                _filter.spec_skip if hasattr(_filter, "spec_skip") else False
            )
            if _filter_spec_skip:
                continue
            if hasattr(_filter, "specs"):
                method = _filter.specs
                specs.append(
                    {"name": filter_name, "choices": getattr(self, method)(session)}
                )
                continue
            specs.append(
                {
                    "name": name,
                    "choices": await self.get_spec_choices(name, session),
                }
            )
        return specs

    async def get_facet_choices(self, field_name, result):
        choices = []
        for item in result:
            if attr := getattr(item[0], field_name):
                choices.append(attr)
        return choices

    async def facets(self, request, session):
        self.query_params = request.query_params.items()
        query = self.filter()
        result = await session.execute(query)
        result = result.fetchall()
        facets = []
        count = len(result)
        for filter_name, _filter in self.get_filters().items():
            name = _filter.field_name if _filter.field_name else filter_name
            _filter_facets_skip = (
                _filter.facets_skip if hasattr(_filter, "facets_skip") else False
            )
            if _filter_facets_skip:
                continue
            if hasattr(_filter, "facets"):
                method = _filter.facets
                facets.append(
                    {"name": filter_name, "choices": getattr(self, method)(session)}
                )
                continue
            facets.append(
                {
                    "name": name,
                    "choices": await self.get_facet_choices(name, result),
                }
            )
        return {"facets": facets, "count": count}
