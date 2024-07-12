from typing import Optional
from pydantic import BaseModel, validator, ValidationError
from datetime import datetime, timedelta

class Job(BaseModel):
    name: str
    category_id: str
    description: str
    jd_file: Optional[str] = None
    min_price: int
    max_price: int
    price_unit: str
    require_skills: Optional[list] = []
    type: str
    end_date: datetime

    @validator('max_price')
    def check_price(cls, v, values):
        if 'min_price' in values and v <= values['min_price']:
            raise ValueError('max_price must be greater than min_price')
        return v

    @validator('type')
    def check_type(cls, v):
        if v not in ('PER_PRJ', 'PER_HOUR'):
            raise ValueError("type must be 'PER_PRJ' or 'PER_HOUR'")
        return v

    @validator('end_date')
    def check_end_date(cls, v):
        if v - datetime.now() < timedelta(days=1):
            raise ValueError('end_date must be at least 1 day from now')
        return v