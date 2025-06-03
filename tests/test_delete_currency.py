from datetime import date

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from models.database import Currency
from .conftest_data import db_session

DATA = [
    Currency(id=4, code="GBP", rate=90.0, date=date(2025, 7, 1)),
    Currency(id=1, code="USD", rate=65.0, date=date(2025, 7, 1)),
    Currency(id=2, code="USD", rate=65.0, date=date(2025, 7, 2)),
]


@pytest.mark.asyncio
async def test_delete_currency_by_code(db_session):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        currency_code = "EUR"
        response = await client.delete(f"/delete-by-code/{currency_code}")
    assert response.status_code == 204

    items: list[Currency] = db_session.query(Currency).order_by(Currency.code).all()
    assert items == DATA


@pytest.mark.asyncio
async def test_pass_invalid_currency_code():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        currency_code = "BLABLA"
        response = await client.delete(f"/delete-by-code/{currency_code}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid currency code format"


@pytest.mark.asyncio
async def test_pass_not_exist_currency_code():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        currency_code = "NON"
        response = await client.delete(f"/delete-by-code/{currency_code}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Currency code not found"
