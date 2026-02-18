"""Database connection management."""
import psycopg2
from ..config.settings import settings
from ..utils.logging import setup_logger

logger = setup_logger("database")


def get_db_connection():
    """Create and return a PostgreSQL database connection."""
    logger.debug("Creating database connection...")
    conn = psycopg2.connect(**settings.db_config)
    logger.debug("Database connection established")
    return conn
