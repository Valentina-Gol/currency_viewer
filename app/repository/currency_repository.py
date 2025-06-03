from datetime import date

from models.models import Currency
from sqlalchemy.orm import Session


class CurrencyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_total_count(self) -> int:
        return self.db.query(Currency).count()

    def get_paginated(self, page: int, per_page: int) -> list[Currency]:
        return (
            self.db.query(Currency)
            .order_by(Currency.date)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    def get_codes(self) -> list[str]:
        codes_rows = (
            self.db.query(Currency.code).order_by(Currency.code).distinct().all()
        )
        return [code_row[0] for code_row in codes_rows]

    def exists_for_date(self, target_date: date) -> bool:
        return (
            self.db.query(Currency).filter(Currency.date == target_date).first()
            is not None
        )

    def add_multiple(self, currencies: list[Currency]) -> None:
        self.db.add_all(currencies)
        self.db.commit()

    def delete_by_code(self, code: str) -> int:
        deleted_count = self.db.query(Currency).filter(Currency.code == code).delete()
        self.db.commit()
        return deleted_count
