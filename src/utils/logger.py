# src/utils/logger.py
# import os
# import logging
# # import datetime
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Set up basic configuration
# LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
# ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
# ENABLED = ENVIRONMENT != "test"

# # Configure logger with appropriate level
# logging.basicConfig(
#     level=getattr(logging, LOG_LEVEL),
#     format='[%(levelname)s] %(asctime)s %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

import logging
# from src.config.settings import settings
from src.config import settings

# Set up basic configuration
LOG_LEVEL = settings.log_level.upper()
ENVIRONMENT = settings.environment
ENABLED = ENVIRONMENT != "test"

# Configure logger with appropriate level
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='[%(levelname)s]    %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Logger:
    def __init__(self):
        self.enabled = ENABLED
        self.is_dev = ENVIRONMENT == 'development'

    def info(self, message, *args):
        if self.enabled:
            logging.info(f"{message}", *args)

    def error(self, message, *args):
        if self.enabled:
            logging.error(f"{message}", *args)

    def warn(self, message, *args):
        if self.enabled:
            logging.warning(f"{message}", *args)

    def debug(self, message, *args):
        if self.enabled and self.is_dev:  # Only log debug in development mode
            logging.debug(f"{message}", *args)

    # def debug(self, message, *args):
    #     if self.enabled:
    #         logging.debug(f"{message}", *args)

# Create logger instance
logger = Logger()