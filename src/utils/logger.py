# src/utils/logger.py
import logging
from src.config import Config

# Set up basic configuration
LOG_LEVEL = Config.log_level.upper()
ENVIRONMENT = Config.environment
ENABLED = ENVIRONMENT != "test"

# Configure logger with appropriate level
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='[%(levelname)s] %(asctime)s %(message)s',
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

# Create logger instance
logger = Logger()