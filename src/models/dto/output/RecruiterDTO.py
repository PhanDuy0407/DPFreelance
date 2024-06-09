from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.dto.output.UserInformation import UserInformation

class RecruiterDTO(BaseModel):
    id: str
    phone: str
    city: Optional[str] = None
    address: Optional[str] = None
    information: Optional[UserInformation] = None

class RecruiterInfoDTO(RecruiterDTO):
    free_post_attempt: int
    remain_post_attempt: int