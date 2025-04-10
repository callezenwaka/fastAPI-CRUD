# src/database/__init__.py
# from .database import database

# __all__ = ['database']

# src/database/__init__.py
from .database import Base, get_db, database

# Export these items so they can be imported directly from src.database
__all__ = ['Base', 'get_db', 'database']