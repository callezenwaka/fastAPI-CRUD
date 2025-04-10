# src/database/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
from typing import AsyncGenerator
from src.config.settings import settings
from src.utils.logger import logger

# Create Base class for models
Base = declarative_base()

class Database:
    def __init__(self, db_url: str = None):
        self.db_url = db_url or settings.database_url
        self.engine: AsyncEngine = None
        self.SessionLocal = None
        
    async def connect(self):
        """Initialize database connection"""
        logger.info(f"Connecting to database at {settings.db_host}:{settings.db_port}/{settings.db_name}")
        
        try:
            # Create async SQLAlchemy engine
            self.engine = create_async_engine(self.db_url, echo=True)
            async with self.engine.begin() as connection:
                statement = text("SELECT 'hello';")
                result = await connection.execute(statement)
                logger.debug(f"Database connection established {result.all()}")
            logger.debug("Database engine created successfully")
            
            # Create async session maker
            self.SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.debug("Database session factory created")
            
            return self
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    async def create_tables(self):
        """Create all tables defined in the models"""
        if not self.engine:
            self.connect()
        
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.debug("Database tables created")
        
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Dependency for getting a database session"""
        if not self.SessionLocal:
            self.connect()
            
        async with self.SessionLocal() as session:
            logger.debug("Database session created")
            try:
                yield session
            finally:
                await session.close()
                logger.debug("Database session closed")


# # Create and initialize the database
# database = Database().connect()

# # For dependency injection
# get_db = database.get_db

# Create database instance without connecting
database = Database()

# For dependency injection - this is a function, not an awaited coroutine
get_db = database.get_db