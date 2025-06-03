from datetime import date

import pytest
from httpx import AsyncClient
from models.models import Currency
from sqlalchemy.orm import Session

DATA = [
    Currency(id=4, code="GBP", rate=90.0, date=date(2025, 7, 1)),
    Currency(id=1, code="USD", rate=65.0, date=date(2025, 7, 1)),
    Currency(id=2, code="USD", rate=65.0, date=date(2025, 7, 2)),
]


@pytest.mark.asyncio
async def test_delete_currency_by_code(db_session: Session, async_client: AsyncClient):
    async with async_client:
        currency_code = "EUR"
        response = await async_client.delete(f"/delete-by-code/{currency_code}")
    assert response.status_code == 204

    items: list[Currency] = db_session.query(Currency).order_by(Currency.code).all()
    assert items == DATA


@pytest.mark.asyncio
async def test_pass_invalid_currency_code(async_client: AsyncClient):
    async with async_client:
        currency_code = "BLABLA"
        response = await async_client.delete(f"/delete-by-code/{currency_code}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid currency code format"


@pytest.mark.asyncio
async def test_pass_not_exist_currency_code(async_client: AsyncClient):
    async with async_client:
        currency_code = "NON"
        response = await async_client.delete(f"/delete-by-code/{currency_code}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Currency code not found"
