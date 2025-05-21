from api_back.db.mongo import collection
from bson import ObjectId
from typing import List, Optional

async def find_all(limit: int, skip: int, sort_order: int) -> List[dict]:
    cursor = collection.find().sort("time", sort_order).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

async def find_by_id(id: str) -> Optional[dict]:
    try:
        return await collection.find_one({"_id": ObjectId(id)})
    except:
        return None
