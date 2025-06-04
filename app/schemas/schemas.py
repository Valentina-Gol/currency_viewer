from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CurrencyCreate(BaseModel):
    date: str = Field(description="Date in format YYY-MM-DD", default="2025-07-03")

    @field_validator("date")
    def valid_date_format(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date have to be in format YYYY-MM-DD")
        return v


class Currency(BaseModel):
    id: int
    date: date
    code: str = "USD"
    rate: float = 1.0

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel):
    page: int = 1
    per_page: int = 1
    total: int = 1
    items: list[Currency]
