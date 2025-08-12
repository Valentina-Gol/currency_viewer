from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI

from app.models.database import Base, engine
from app.routes.routes import router
from app.middleware.request_handler import RequestLogMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Currency Rates API",
    description="Service for working with currency rates of the CB RF",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
app.add_middleware(RequestLogMiddleware)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s  %(message)s")
