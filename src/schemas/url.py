from typing import Optional, Union
from pydantic import BaseModel, validator
from dateutil.parser import parse as parse_date
from src.models import Visit
from datetime import datetime


class URL(BaseModel):
    short_url: str
    url: str
    created_date: datetime

    class Config:
        orm_mode = True


class URLAuthenticated(URL):
    user_id: int
    visits: list[Visit]

    @validator('visits')
    def visits_unpacker(cls, v):
        return [visit.date for visit in v]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class URLFilters(BaseModel):
    user: Optional[int]
    date_from: Optional[str]
    date_to: Optional[str]
    offset: Optional[int]
    limit: Optional[int]

    @validator('date_from', 'date_to')
    def date_validator(cls, v):
        return parse_date(v, ignoretz=True).strftime("%Y-%m-%d %H:%M:%S")
