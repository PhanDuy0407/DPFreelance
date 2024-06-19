from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.dto.output.UserInformation import UserInformation

class RecruiterDTO(BaseModel):
    id: str
    phone: str
    city: Optional[str] = None
    address: Optional[str] = None
    company_name: Optional[str] = None
    information: Optional[UserInformation] = None
    created_at: datetime

class RecruiterInfoDTO(RecruiterDTO):
    cccd: Optional[str] = None
    free_post_attempt: int
    remain_post_attempt: int

class RecruiterStatistic(BaseModel):
    job_posted: Optional[int] = 0
    job_done: Optional[int] = 0
    job_in_progress: Optional[int] = 0