from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.dto.output.UserInformation import UserInformation

class RecruiterDTO(BaseModel):
    id: str
    recruiter_email: str
    phone: str
    information: Optional[UserInformation] = None

class RecruiterInfoDTO(RecruiterDTO):
    free_post_attempt: int
    remain_post_attempt: int