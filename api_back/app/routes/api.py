from fastapi import APIRouter, Query, Path, Body
from typing import List
from app.models.dto import OtzivListDTO, OtzivDetailDTO, OtzivBaseDTO
from app.services.otziv_service import get_all_otzivs, get_otziv_by_id, create_new_otziv

router = APIRouter()

@router.get("/otziv", response_model=List[OtzivListDTO], summary="Пагинированный список отзывов")
async def get_otziv_list(
    limit: int = Query(10, gt=0),
    skip: int = Query(0, ge=0),
    sort: str = Query("desc", pattern="^(asc|desc)$")
):
    """
    Получить список отзывов с пагинацией и сортировкой.
    """
    return await get_all_otzivs(limit, skip, sort)

@router.get("/otziv/{id}", response_model=OtzivDetailDTO, summary="Получить отзыв по _id")
async def get_otziv_by_id_route(id: str = Path(..., description="MongoDB ObjectId")):
    """
    Получить подробную информацию об отзыве по его идентификатору.
    """
    return await get_otziv_by_id(id)

@router.post("/otziv", response_model=str, summary="Создать новый отзыв")
async def create_otziv_route(otziv: OtzivBaseDTO = Body(...)):
    """
    Создать новый отзыв.
    """
    return await create_new_otziv(otziv)