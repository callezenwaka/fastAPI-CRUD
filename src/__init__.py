# src/__init__.py
from fastapi import FastAPI
from src.books.routes import bookRouter
from src.config import settings
from src.database import database
from src.health import healthRouter
from contextlib import asynccontextmanager
from src.utils.logger import logger

@asynccontextmanager
async def life_span(app: FastAPI):
    # Startup logic
    logger.info("Server is starting...")
    await database.connect()
    logger.debug("Database connected")
    
    yield  # This is where FastAPI serves requests
    
    # Shutdown logic
    logger.info("Server is shutting down...")
    if database.engine:
        await database.engine.dispose()
        logger.debug("Database connection closed")
    logger.info("Server has been stopped!")

app = FastAPI(
    title="Book store",
    description="This is a book store service.",
    version=settings.api_version,
    lifespan=life_span
)
        
app.include_router(bookRouter, prefix=f"/api/{settings.api_version}/books", tags=["books"])
app.include_router(healthRouter, prefix=f"/api/{settings.api_version}", tags=["health"])