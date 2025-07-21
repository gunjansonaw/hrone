from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

client = AsyncIOMotorClient(MONGODB_URL)
db = client.ecommerce

def ping_db():
    """Test database connection"""
    try:
        MongoClient(MONGODB_URL).admin.command('ping')
        return True
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return False