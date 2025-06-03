import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from models.database import Currency, Base
from app.dependencies import get_db
from app.main import app
from unittest.mock import AsyncMock


engine = create_engine("sqlite:///memory.db")
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_initialization():
    Base.metadata.create_all(engine)
    session = Session()
    session.add_all(
        [
            Currency(code="USD", rate=65.0, date=date(2025, 7, 1)),
            Currency(code="USD", rate=65.0, date=date(2025, 7, 2)),
            Currency(code="EUR", rate=75.0, date=date(2025, 7, 2)),
            Currency(code="GBP", rate=90.0, date=date(2025, 7, 1)),
        ]
    )
    session.commit()
    session.close()


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


# todo может получитсься от дублирования избавиться?
@pytest.fixture
def db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def override_db_dependency(db_initialization):
    app.dependency_overrides[get_db] = get_session
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


@pytest.fixture
def mock_fetch_currency_rates_basic(monkeypatch):
    data = (
        '<?xml version="1.0" encoding="windows-1251"?>'
        '<ValCurs Date="01.01.2020" name="Foreign Currency Market"><Valute ID="R01010">'
        "<NumCode>036</NumCode><CharCode>AUD</CharCode><Nominal>1</Nominal><Name>Австралийский доллар</Name>"
        "<Value>14,6800</Value><VunitRate>14,68</VunitRate></Valute>"
        '<Valute ID="R01035"><NumCode>826</NumCode><CharCode>GBP</CharCode><Nominal>1</Nominal>'
        "<Name>Фунт стерлингов</Name><Value>43,4800</Value><VunitRate>43,48</VunitRate></Valute>"
        "</ValCurs>"
    )
    async_mock = AsyncMock(return_value=data)
    monkeypatch.setattr("app.routes.utils.fetch_currency_rates", async_mock)
    return async_mock
