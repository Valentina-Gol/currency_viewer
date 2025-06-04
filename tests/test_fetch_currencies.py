from datetime import date
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.models.models import Currency

DATA = [
    Currency(id=5, code="AUD", rate=14.68, date=date(2020, 1, 1)),
    Currency(id=6, code="GBP", rate=43.48, date=date(2020, 1, 1)),
]


@pytest.mark.asyncio
async def test_post_currency(
    db_session: Session,
    mock_fetch_currency_rates_basic: AsyncMock,
    async_client: AsyncClient,
):
    test_date = date(2020, 1, 1)
    async with async_client:
        response = await async_client.post(
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
async def test_pass_already_existing_date(async_client: AsyncClient):
    test_date = date(2025, 7, 1)
    async with async_client:
        response = await async_client.post(
            "/currencies", json={"date": test_date.strftime("%Y-%m-%d")}
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Data for the specified dates already exists"


@pytest.mark.asyncio
async def test_cbr_fetching_error(
    mock_fetch_errors_values: AsyncMock, async_client: AsyncClient
):
    test_date = date(2025, 7, 10)
    async with async_client:
        response = await async_client.post(
            "/currencies", json={"date": test_date.strftime("%Y-%m-%d")}
        )
    assert response.status_code == 502
    mock_fetch_errors_values.assert_called_once()


@pytest.mark.asyncio
async def test_invalid_body_format(async_client: AsyncClient):
    async with async_client:
        response = await async_client.post("/currencies", json={"date": "2025/07/10"})
    assert response.status_code == 422
