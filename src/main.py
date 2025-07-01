import os
import uvicorn
from fastapi import FastAPI
from routes import (
    accounts_router,
    profiles_router,
    movies_router,
    carts_router,
    orders_router,
    payment_router,
)

if "ENVIRONMENT" not in os.environ:
    os.environ["ENVIRONMENT"] = "local"

app = FastAPI(
    title="Online cinema",
    description="Online Cinema project based on FastAPI and SQLAlchemy",
)

app.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
app.include_router(profiles_router, prefix="/profiles", tags=["profiles"])
app.include_router(movies_router, prefix="/movies", tags=["movies"])
app.include_router(carts_router, prefix="/carts", tags=["carts"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(payment_router, prefix="/payments", tags=["payments"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
