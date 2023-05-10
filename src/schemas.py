from typing import Optional
from pydantic import BaseModel, validator
from dateutil.parser import parse as parse_date

class URLFilters(BaseModel):
    user: Optional[int]
    date_from: Optional[str]
    date_to: Optional[str]
    offset: Optional[int]
    limit: Optional[int]

    @validator('date_from', 'date_to')
    def date_validator(cls, v):
        return parse_date(v, ignoretz=True).strftime("%Y-%m-%d %H:%M:%S")
