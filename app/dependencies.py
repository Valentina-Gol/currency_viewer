from typing import Generator

from fastapi import Depends
from models.database import SessionLocal
from repository.currency_repository import CurrencyRepository
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_currency_repository(db: Session = Depends(get_db)) -> CurrencyRepository:
    return CurrencyRepository(db)
