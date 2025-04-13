# src/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database import get_db
from src.utils import logger

healthRouter = APIRouter()

@healthRouter.get("/health")
async def check_health(db: AsyncSession = Depends(get_db)):
    try:
        logger.debug("Executing health check query")
        result = await db.execute(text("SELECT 1"))
        row = result.fetchone()
        if row:
            logger.debug("Database health check successful")
            return {"status": "healthy", "database": "connected"}
        else:
            logger.warn("Database health check query returned no results")
            return {"status": "unhealthy", "database": "no results"}
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}