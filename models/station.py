from pydantic import BaseModel, Field
from typing import List
from models.tag import Tag
import datetime

class Station(BaseModel):
    id: int = Field(...) 
    name: str = Field(...)
    tags: List[Tag] = Field(...)
    datetime: datetime.datetime