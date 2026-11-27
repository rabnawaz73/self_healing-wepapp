"""Application entry point.

Endpoints are implemented in the application development task.
"""
"""CloudRescue FastAPI application."""

from fastapi import FastAPI
from mangum import Mangum

from app.routes import router


app = FastAPI(
    title="CloudRescue",
    description="A self-healing sample e-commerce application.",
    version="1.0",
)
app.include_router(router)

handler = Mangum(app)
