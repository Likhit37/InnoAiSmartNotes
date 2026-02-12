"""
MongoDB connection management.
"""

from pymongo import MongoClient
from backend.shared.core.config import settings


class MongoDB:
    client: MongoClient = None
    db = None


mongodb = MongoDB()


def connect_to_mongo():
    """
    Establish MongoDB connection and ensure required indexes.
    """

    mongodb.client = MongoClient(settings.MONGO_URI)

    # Explicit database selection (safer than get_default_database)
    mongodb.db = mongodb.client.get_default_database()

    # Ensure unique index on email
    mongodb.db.users.create_index("email", unique=True)

    print("MongoDB connected")


def close_mongo_connection():
    """
    Close MongoDB connection gracefully.
    """
    if mongodb.client:
        mongodb.client.close()
        print("MongoDB connection closed")
