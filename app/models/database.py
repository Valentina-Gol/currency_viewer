from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import DATABASE_URL

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, pool_size=100
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
