"""Logging configuration utilities."""
import logging
import os
from datetime import datetime
from ..config.settings import settings

# Ensure logs directory exists
if not os.path.exists(settings.LOGS_DIR):
    os.makedirs(settings.LOGS_DIR)

log_filename = os.path.join(
    settings.LOGS_DIR, 
    f"rag_chatbot_{datetime.now().strftime('%Y-%m-%d')}.log"
)


class DetailedFormatter(logging.Formatter):
    """Custom formatter that adds stage information."""
    
    def format(self, record):
        if hasattr(record, 'stage'):
            record.msg = f"\n{'='*60}\n[STAGE: {record.stage}]\n{'='*60}\n{record.msg}"
        return super().format(record)


def setup_logger(name: str) -> logging.Logger:
    """Setup and return a logger with file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = DetailedFormatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d\n%(message)s\n'
    )
    file_handler.setFormatter(file_format)
    
    # Optional: uncomment to enable console logging
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_format = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
    # console_handler.setFormatter(console_format)
    # logger.addHandler(console_handler)
    
    logger.addHandler(file_handler)
    
    return logger
