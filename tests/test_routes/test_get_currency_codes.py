import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from httpx import AsyncClient, ASGITransport

from models.database import Currency, Base
from app.dependencies import get_db
from app.main import app


@pytest.fixture
def db_initialization():
    engine = create_engine("sqlite:///memory")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
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
    engine = create_engine("sqlite:///memory")
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def override_db_dependency(db_initialization):
    app.dependency_overrides[get_db] = get_session
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_codes():
    async with AsyncClient(
        # todo move base_url to config
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        response = await client.get("/unique-currency-codes")
    assert response.status_code == 200
    assert response.json() == ["EUR", "GBP", "USD"]
