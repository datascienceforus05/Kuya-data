"""
Database Utility - MongoDB connection and operations
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from typing import Optional

# MongoDB connection settings
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "kuya_cloud")

# Global client instances
_async_client: Optional[AsyncIOMotorClient] = None
_sync_client: Optional[MongoClient] = None


def get_database():
    """
    Get async MongoDB database instance.
    Uses Motor for async operations.
    """
    global _async_client
    
    if _async_client is None:
        _async_client = AsyncIOMotorClient(MONGODB_URI)
    
    return _async_client[DATABASE_NAME]


def get_sync_database():
    """
    Get synchronous MongoDB database instance.
    Used for operations that don't support async.
    """
    global _sync_client
    
    if _sync_client is None:
        _sync_client = MongoClient(MONGODB_URI)
    
    return _sync_client[DATABASE_NAME]


async def init_database():
    """
    Initialize database with indexes.
    Call this on application startup.
    """
    db = get_database()
    
    # Create indexes for users collection
    users = db.users
    await users.create_index("email", unique=True)
    
    # Create indexes for reports collection
    reports = db.reports
    await reports.create_index("reportId", unique=True)
    await reports.create_index("userEmail")
    await reports.create_index("createdAt")
    
    print("Database indexes created successfully")


async def close_database():
    """
    Close database connections.
    Call this on application shutdown.
    """
    global _async_client, _sync_client
    
    if _async_client:
        _async_client.close()
        _async_client = None
    
    if _sync_client:
        _sync_client.close()
        _sync_client = None
    
    print("Database connections closed")
