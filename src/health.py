from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

# from src.database.database import get_db
from src.database import get_db

healthRouter = APIRouter()

@healthRouter.get("/health")
def check_health(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to check the database connection
        result = db.execute(text("SELECT 1")).fetchone()
        if result:
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}