import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Define log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        RotatingFileHandler(
            "logs/app.log",
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3
        ),
        logging.StreamHandler()  # prints logs to console
    ]
)

logger = logging.getLogger("app")
