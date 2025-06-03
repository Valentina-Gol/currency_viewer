from fastapi import FastAPI
from models.database import Base, engine
from routes.routes import router

app = FastAPI(
    title="Currency Rates API",
    description="Service for working with currency rates of the CB RF",
    version="1.0.0",
)

app.include_router(router)


Base.metadata.create_all(bind=engine)
