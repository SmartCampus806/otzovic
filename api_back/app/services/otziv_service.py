from api_back.repositories.otziv_repository import find_all, find_by_id
from api_back.models.dto import OtzivListDTO, OtzivDetailDTO
from typing import List
from fastapi import HTTPException

async def get_all_otzivs(limit: int, skip: int, sort: str) -> List[OtzivListDTO]:
    sort_order = 1 if sort == "asc" else -1
    raw_docs = await find_all(limit, skip, sort_order)
    return [OtzivListDTO(**doc) for doc in raw_docs]

async def get_otziv_by_id(id: str) -> OtzivDetailDTO:
    doc = await find_by_id(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Otziv not found")
    return OtzivDetailDTO(**doc)
