from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.models.database import Base, engine
from app.routes.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Currency Rates API",
    description="Service for working with currency rates of the CB RF",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
