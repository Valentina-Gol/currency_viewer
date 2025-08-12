from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.settings import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, pool_size=100, echo=False
)
session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
