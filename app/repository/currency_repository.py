from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, func

from app.models.models import Currency


class CurrencyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_total_count(self) -> int:
        return 0
        # return (await self._session.execute(Select(func.count(Currency)))).scalar()
        # return self._session.query(Currency).count()

    async def get_paginated(self, page: int, per_page: int) -> list[Currency]:
        return []
        # return (
        #     self._session.query(Currency)
        #     .order_by(Currency.date)
        #     .offset((page - 1) * per_page)
        #     .limit(per_page)
        #     .all()
        # )

    async def get_codes(self) -> list[str]:
        return (
            (
                await self._session.execute(
                    Select(Currency.code).order_by(Currency.code).distinct()
                )
            )
            .scalars()
            .all()
        )

    async def exists_for_date(self, target_date: date) -> bool:
        return False
        # return (
        #     self._session.query(Currency).filter(Currency.date == target_date).first()
        #     is not None
        # )

    async def add_multiple(self, currencies: list[Currency]) -> None:
        pass
        # self._session.add_all(currencies)
        # self._session.commit()

    async def delete_by_code(self, code: str) -> int:
        return 0
        # deleted_count = (
        #     self._session.query(Currency).filter(Currency.code == code).delete()
        # )
        # self._session.commit()
        # return deleted_count
