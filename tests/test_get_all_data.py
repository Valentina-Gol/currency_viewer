import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_first_page(async_client: AsyncClient):
    async with async_client:
        response = await async_client.get(
            "/all-data", params={"page": 1, "per_page": 2}
        )
    assert response.status_code == 200
    assert response.json() == {
        "page": 1,
        "per_page": 2,
        "total": 4,
        "items": [
            {"code": "USD", "date": "2025-07-01", "id": 1, "rate": 65.0},
            {"code": "GBP", "date": "2025-07-01", "id": 4, "rate": 90.0},
        ],
    }


@pytest.mark.asyncio
async def test_get_last_page(async_client: AsyncClient):
    async with async_client:
        response = await async_client.get(
            "/all-data", params={"page": 2, "per_page": 3}
        )
    assert response.status_code == 200
    assert response.json() == {
        "page": 2,
        "per_page": 3,
        "total": 4,
        "items": [{"code": "EUR", "date": "2025-07-02", "id": 3, "rate": 75.0}],
    }


@pytest.mark.asyncio
async def test_get_extra_page(async_client: AsyncClient):
    async with async_client:
        response = await async_client.get(
            "/all-data", params={"page": 50, "per_page": 3}
        )
    assert response.status_code == 200
    assert response.json() == {"page": 50, "per_page": 3, "total": 4, "items": []}


@pytest.mark.asyncio
async def test_pass_wrong_params(async_client: AsyncClient):
    async with async_client:
        response = await async_client.get(
            "/all-data", params={"page": -1, "per_page": 3}
        )
    assert response.status_code == 422
