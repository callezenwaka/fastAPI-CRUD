# src/__init__.py
from fastapi import FastAPI
from src.books.routes import bookRouter
from src.users.routes import userRouter
from src.reviews.routes import reviewRouter
from src.health import healthRouter
from src.config import Config
from src.database import database
from contextlib import asynccontextmanager
from src.utils.logger import logger
from src.errors.error import register_all_errors
from src.middleware.middleware import register_middleware

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
    title=Config.title,
    description=Config.description,
    version=Config.api_version,
    docs_url=f"/api/{Config.api_version}/docs",
    contact={
        "name": "Wise Owl",
        "email": "info@mail.com",
    }
    # lifespan=life_span
)

register_all_errors(app)

register_middleware(app)
        
app.include_router(bookRouter, prefix=f"/api/{Config.api_version}/books", tags=["books"])
app.include_router(userRouter, prefix=f"/api/{Config.api_version}/users", tags=["users"])
app.include_router(reviewRouter, prefix=f"/api/{Config.api_version}/reviews", tags=["reviews"])
app.include_router(healthRouter, prefix=f"/api/{Config.api_version}", tags=["health"])