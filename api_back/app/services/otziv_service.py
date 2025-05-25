from app.db.mongo import collection
from app.models.dto import OtzivListDTO, OtzivDetailDTO, OtzivBaseDTO
from typing import List
from fastapi import HTTPException
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

async def get_all_otzivs(limit: int, skip: int, sort: str) -> List[OtzivListDTO]:
    sort_order = 1 if sort == "asc" else -1
    cursor = collection.find().sort("date", sort_order).skip(skip).limit(limit)
    raw_docs = await cursor.to_list(length=limit)
    result = []
    for doc in raw_docs:
        item = {
            "id": str(doc["_id"]),
            "date": doc["date"],
            "title": doc["title"],
            "source_id": doc["source_id"]
        }
        result.append(OtzivListDTO(**item))
    return result

async def get_otziv_by_id(id: str) -> OtzivDetailDTO:
    try:
        doc = await collection.find_one({"_id": ObjectId(id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Otziv not found")
        doc["id"] = str(doc["_id"])
        return OtzivDetailDTO(**doc)
    except Exception:
        raise HTTPException(status_code=404, detail="Otziv not found")

async def create_new_otziv(otziv: OtzivBaseDTO) -> str:
    doc = otziv.dict()
    result = await collection.insert_one(doc)
    return str(result.inserted_id)