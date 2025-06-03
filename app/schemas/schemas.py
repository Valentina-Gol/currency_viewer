from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date


class CurrencyCreate(BaseModel):
    date: str = Field(..., description="Date in format YYY-MM-DD")

    @field_validator("date")
    def valid_date_format(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date have to be in format YYYY-MM-DD")
        return v


class Currency(BaseModel):
    id: int
    code: str
    rate: float
    date: date

    class Config:
        orm_mode = True


class PaginatedResponse(BaseModel):
    page: int
    per_page: int
    total: int
    items: list[Currency]
