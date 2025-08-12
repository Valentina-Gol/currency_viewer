from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import session_maker
from app.repository.currency_repository import CurrencyRepository


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = session_maker()
    try:
        yield session
    finally:
        await session.close()


def get_currency_repository(
    session: AsyncSession = Depends(get_session),
) -> CurrencyRepository:
    return CurrencyRepository(session)
