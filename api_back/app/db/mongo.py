from motor.motor_asyncio import AsyncIOMotorClient
from api_back.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
collection = db[settings.COLLECTION_NAME]
