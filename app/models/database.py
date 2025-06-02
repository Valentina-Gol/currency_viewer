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


Base.metadata.create_all(bind=engine)
