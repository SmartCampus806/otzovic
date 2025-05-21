from pydantic import BaseModel, Extra, Field
from typing import Optional
from datetime import datetime

class OtzivListDTO(BaseModel):
    _id: str = Field(..., alias="_id")
    source_id: str
    text: str
    time: datetime

class OtzivDetailDTO(BaseModel, extra=Extra.allow):
    _id: str = Field(..., alias="_id")
