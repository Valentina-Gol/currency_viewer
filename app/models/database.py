from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./currency.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), index=True)
    rate = Column(Float)
    date = Column(Date)

    def __eq__(self, other):
        if isinstance(other, Currency):
            return (
                other.code == self.code
                and other.rate == self.rate
                and other.date == self.date
                and other.id == self.id
            )
        return False

    def __repr__(self):
        if self.id:
            return f"Currency(id={self.id}, code={self.code}, rate={self.rate}, date={self.date})"
        return f"Currency(code={self.code}, rate={self.rate}, date={self.date})"


Base.metadata.create_all(bind=engine)
