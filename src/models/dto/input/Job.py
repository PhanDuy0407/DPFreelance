from datetime import datetime
from pydantic import BaseModel

class Job(BaseModel):
    name: str
    category_id: str
    description: str
    jd_file: str
    price: int
    price_unit: str
    type: str
    estimate_time: str
    end_date: datetime