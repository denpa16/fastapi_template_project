import pytest

import factory
from app.models import Project


class ProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Фабрика проектов."""

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f"name_{n}")
    alias = factory.Sequence(lambda n: f"alias_{n}")

    class Meta:
        model = Project


@pytest.fixture()
async def project_db_factory(override_get_db_session):
    async def factory(project_data: dict):
        async for s in override_get_db_session():
            project = Project(**project_data)
            s.add(project)
            await s.flush()
            await s.commit()
        return project

    return factory
