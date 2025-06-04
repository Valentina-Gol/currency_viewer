from sqlalchemy import Column, Date, Float, Integer, String

from app.models.database import Base


class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), index=True)
    rate = Column(Float)
    date = Column(Date)

    def __eq__(self, other) -> bool:
        if isinstance(other, Currency):
            return (
                other.code == self.code
                and other.rate == self.rate
                and other.date == self.date
                and other.id == self.id
            )
        return False

    def __repr__(self) -> str:
        if self.id:
            return f"Currency(id={self.id}, code={self.code}, rate={self.rate}, date={self.date})"
        return f"Currency(code={self.code}, rate={self.rate}, date={self.date})"
