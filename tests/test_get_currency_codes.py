import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_get_codes():
    # todo move AsyncClient to conftest
    async with AsyncClient(
        # todo move base_url to config
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        response = await client.get("/unique-currency-codes")
    assert response.status_code == 200
    assert response.json() == ["EUR", "GBP", "USD"]
