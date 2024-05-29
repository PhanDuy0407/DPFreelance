from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.dto.output.RecruiterDTO import RecruiterDTO
from models.dto.output.CategoryDTO import CategoryDTO

class JobDTO(BaseModel):
    id: str
    name: str
    category: CategoryDTO
    poster: RecruiterDTO
    description: str
    jd_file: str
    price: int
    price_unit: str
    type: str
    status: str
    estimate_time: str
    end_date: datetime
    created_at: datetime