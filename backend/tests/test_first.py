import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestCreateToken:
    async def test(self, api_client_dm: AsyncClient):
        result = await api_client_dm.get("projects/get_multiple")
        assert result.status_code == 200
