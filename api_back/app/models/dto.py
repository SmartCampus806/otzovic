from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OtzivBaseDTO(BaseModel):
    date: datetime
    text: str
    title: str
    rating: int
    city: str
    author: str
    comments: int
    source_id: str

class OtzivListDTO(BaseModel):
    id: str = Field(..., alias="id")
    date: datetime
    title: str
    source_id: str

class OtzivDetailDTO(OtzivBaseDTO):
    id: str = Field(..., alias="id")