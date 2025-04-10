# # src/database.py
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# from src.utils.logger import logger

# # Load environment variables from .env file
# load_dotenv()

# # Get database connection parameters from environment variables
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_PORT = os.getenv("DB_PORT", "5432")
# DB_USERNAME = os.getenv("DB_USERNAME", "app_user")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "app_password")
# DB_NAME = os.getenv("DB_NAME", "app_db")

# # Construct the database URL
# DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# # DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# logger.info(f"Connecting to database at {DB_HOST}:{DB_PORT}/{DB_NAME}")

# try:
#     # Create SQLAlchemy engine
#     engine = create_engine(DATABASE_URL)
#     logger.debug("Database engine created successfully")
    
#     # Create SessionLocal class
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     logger.debug("Database session factory created")
    
#     # Create Base class for models
#     Base = declarative_base()
    
# except Exception as e:
#     logger.error(f"Failed to connect to database: {str(e)}")
#     raise

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     logger.debug("Database session created")
#     try:
#         yield db
#     finally:
#         db.close()
#         logger.debug("Database session closed")

# src/database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # from src.config.settings import settings
# from src.config import settings
# from src.utils.logger import logger

# # Log connection info
# logger.info(f"Connecting to database at {settings.db_host}:{settings.db_port}/{settings.db_name}")

# try:
#     # Create SQLAlchemy engine using the database URL from settings
#     engine = create_engine(settings.database_url)
#     logger.debug("Database engine created successfully")
    
#     # Create SessionLocal class
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     logger.debug("Database session factory created")
    
#     # Create Base class for models
#     Base = declarative_base()
    
# except Exception as e:
#     logger.error(f"Failed to connect to database: {str(e)}")
#     raise

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     logger.debug("Database session created")
#     try:
#         yield db
#     finally:
#         db.close()
#         logger.debug("Database session closed")

# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from src.config.settings import settings
from src.utils.logger import logger

# Create Base class for models
Base = declarative_base()

class Database:
    def __init__(self, db_url: str = None):
        self.db_url = db_url or settings.database_url
        self.engine = None
        self.SessionLocal = None
        
    def connect(self):
        """Initialize database connection"""
        logger.info(f"Connecting to database at {settings.db_host}:{settings.db_port}/{settings.db_name}")
        
        try:
            # Create SQLAlchemy engine
            # self.engine = create_engine(self.db_url)
            self.engine = create_async_engine(self.db_url)
            logger.debug("Database engine created successfully")
            
            # Create SessionLocal class
            # self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.debug("Database session factory created")
            
            return self
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    def create_tables(self):
        """Create all tables defined in the models"""
        if not self.engine:
            self.connect()
        
        Base.metadata.create_all(bind=self.engine)
        logger.debug("Database tables created")
        
    def get_db(self) -> Generator[Session, None, None]:
        """Dependency for getting a database session"""
        if not self.SessionLocal:
            self.connect()
            
        db = self.SessionLocal()
        logger.debug("Database session created")
        
        try:
            yield db
        finally:
            db.close()
            logger.debug("Database session closed")


# Create and initialize the database
database = Database().connect()

# For dependency injection
get_db = database.get_db