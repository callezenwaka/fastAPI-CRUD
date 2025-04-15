# src/database/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
# from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from src.config import Config
from src.utils.logger import logger
# from src.database.models import Book

# No need for Base = declarative_base() since SQLModel serves as your base class

class Database:
    def __init__(self, db_url: str = None):
        self.db_url = db_url or Config.database_url
        self.engine: AsyncEngine = None
        self.SessionLocal = None
        
    async def connect(self):
        """Initialize database connection"""
        logger.info(f"Connecting to database at {Config.db_host}:{Config.db_port}/{Config.db_name}")
        
        try:
            # Create async SQLAlchemy engine
            # self.engine = create_async_engine(self.db_url, echo=True)
            self.engine = create_async_engine(self.db_url)
            async with self.engine.begin() as connection:
                await connection.run_sync(SQLModel.metadata.create_all)

            logger.debug("Database engine created successfully")
            
            # Create async session maker
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, class_=AsyncSession, bind=self.engine, expire_on_commit=False)
            logger.debug("Database session factory created")
            
            return self
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    async def create_tables(self):
        """Create all tables defined in the models"""
        if not self.engine:
            await self.connect()
        
        async with self.engine.begin() as connection:
            # Use SQLModel.metadata instead of Base.metadata
            await connection.run_sync(SQLModel.metadata.create_all)
        logger.debug("Database tables created")
        
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Dependency for getting a database session"""
        if not self.SessionLocal:
            await self.connect()
            
        async with self.SessionLocal() as session:
            logger.debug("Database session created")
            try:
                yield session
            finally:
                await session.close()
                logger.debug("Database session closed")


# Create database instance without connecting
init_database = Database()

# For dependency injection - this is a function, not an awaited coroutine
get_session = init_database.get_session