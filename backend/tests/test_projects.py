import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestProjects:
    async def test(self, api_client: AsyncClient):
        result = await api_client.get("projects/get_multiple")
        assert result.status_code == 200
