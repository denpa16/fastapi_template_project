import pytest

from app.models import Project


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
