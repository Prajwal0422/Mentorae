"""
MongoDB database configuration and connection management.
Uses Motor for async MongoDB operations.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .settings import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    """MongoDB database connection manager."""
    
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None


db = Database()


async def connect_to_mongo():
    """
    Establish connection to MongoDB.
    Called on application startup.
    """
    try:
        logger.info("Connecting to MongoDB...")
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.database = db.client[settings.DATABASE_NAME]
        
        # Test connection
        await db.client.admin.command('ping')
        logger.info(f"Successfully connected to MongoDB: {settings.DATABASE_NAME}")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection.
    Called on application shutdown.
    """
    try:
        logger.info("Closing MongoDB connection...")
        if db.client:
            db.client.close()
        logger.info("MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")


def get_database() -> AsyncIOMotorDatabase:
    """
    Get database instance.
    Used as a dependency in route handlers.
    """
    return db.database
