from fastapi import FastAPI

from routes.routes import router

app = FastAPI(
    title="Currency Rates API",
    description="RESTful-service for working with currency rates of the CB RF",
    version="1.0.0",
)

app.include_router(router)
