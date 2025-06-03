from datetime import date
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from models.database import Currency


DATA = [
    Currency(id=5, code="AUD", rate=14.68, date=date(2020, 1, 1)),
    Currency(id=6, code="GBP", rate=43.48, date=date(2020, 1, 1)),
]


@pytest.fixture
def mock_fetch_errors_values(monkeypatch):
    data = (
        '<?xml version="1.0" encoding="windows-1251"?>'
        '<ValCurs Date="01.01.2020" name="Foreign Currency Market"><Valute ID="R01010">'
        "<NumCode>036</NumCode><CharCode>AUD</CharCode><Nominal>1</Nominal><Name>Австралийский доллар</Name>"
        "</ValCurs>"
    )
    async_mock = AsyncMock(return_value=data)
    monkeypatch.setattr("app.routes.utils.fetch_currency_rates", async_mock)
    return async_mock


@pytest.mark.asyncio
async def test_post_currency(db_session, mock_fetch_currency_rates_basic):
    test_date = date(2020, 1, 1)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        response = await client.post(
            "/currencies", json={"date": test_date.strftime("%Y-%m-%d")}
        )
    assert response.status_code == 201
    mock_fetch_currency_rates_basic.assert_called_once()

    items: list[Currency] = (
        db_session.query(Currency)
        .filter(Currency.date == test_date)
        .order_by(Currency.code)
        .all()
    )
    assert items == DATA


@pytest.mark.asyncio
async def test_pass_already_existing_date(db_session):
    test_date = date(2025, 7, 1)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        response = await client.post(
            "/currencies", json={"date": test_date.strftime("%Y-%m-%d")}
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Data for the specified dates already exists"


@pytest.mark.asyncio
async def test_cbr_fetching_error(db_session, mock_fetch_errors_values):
    test_date = date(2025, 7, 10)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        response = await client.post(
            "/currencies", json={"date": test_date.strftime("%Y-%m-%d")}
        )
    assert response.status_code == 502
    mock_fetch_errors_values.assert_called_once()


@pytest.mark.asyncio
async def test_invalid_body_format(db_session):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        response = await client.post("/currencies", json={"date": "2025/07/10"})
    assert response.status_code == 422
