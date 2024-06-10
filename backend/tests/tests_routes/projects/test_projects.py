import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestProjects:
    """Тесты проектов."""

    async def test_get_multiple(self, api_client: AsyncClient):
        """Тест списка проекта."""
        result = await api_client.get("projects/get_multiple")
        assert result.status_code == 200
        res_json = result.json()
        assert res_json == []
