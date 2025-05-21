from fastapi import APIRouter, Query, Path
from typing import List
from app.models.dto import OtzivListDTO, OtzivDetailDTO
from app.services.otziv_service import get_all_otzivs, get_otziv_by_id

router = APIRouter()

@router.get("/otziv", response_model=List[OtzivListDTO], summary="Пагинированный список отзывов")
async def get_otziv_list(
    limit: int = Query(10, gt=0),
    skip: int = Query(0, ge=0),
    sort: str = Query("desc", regex="^(asc|desc)$")
):
    return await get_all_otzivs(limit, skip, sort)

@router.get("/otziv/{id}", response_model=OtzivDetailDTO, summary="Получить отзыв по _id")
async def get_otziv_by_id_route(id: str = Path(..., description="MongoDB ObjectId")):
    return await get_otziv_by_id(id)
