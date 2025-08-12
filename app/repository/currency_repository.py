from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select as select_sa, delete as delete_sa

from app.models.models import Currency


class CurrencyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_total_count(self) -> int:
        query = select_sa(func.count(Currency.id))
        result = await self._session.execute(query)
        return result.scalar()

    async def get_paginated(self, page: int, per_page: int) -> list[Currency]:
        query = select_sa(Currency).offset((page - 1) * per_page).limit(per_page).order_by(Currency.date)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_codes(self) -> list[str]:
        return (
            (
                await self._session.execute(
                    select_sa(Currency.code).order_by(Currency.code).distinct()
                )
            )
            .scalars()
            .all()
        )

    async def exists_for_date(self, target_date: date) -> bool:
        return (await self._session.execute(select_sa(Currency.date).where(Currency.date == target_date))).scalars().all() != []

    async def add_multiple(self, currencies: list[Currency]) -> None:
        self._session.add_all(currencies)
        await self._session.commit()

    async def delete_by_code(self, code: str) -> int:
        result = await self._session.execute(delete_sa(Currency).filter_by(code=code))
        await self._session.commit()
        return result.rowcount

