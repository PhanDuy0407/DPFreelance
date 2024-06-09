from typing import Optional
from datetime import datetime
from pydantic import BaseModel

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