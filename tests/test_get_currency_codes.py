import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_codes(async_client: AsyncClient):
    async with async_client:
        response = await async_client.get("/unique-currency-codes")
    assert response.status_code == 200
    assert response.json() == ["EUR", "GBP", "USD"]
