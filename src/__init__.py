# src/__init__.py
from fastapi import FastAPI
from src.books.routes import bookRouter
from src.health import healthRouter

version = "v1"

app = FastAPI(
    title="Book store",
    description="This is a book store service.",
    version=version
)

app.include_router(bookRouter, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(healthRouter, prefix=f"/api/{version}", tags=["health"])