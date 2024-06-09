from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.dto.output.UserInformation import UserInformation

class ApplicantDTO(BaseModel):
    id: str
    information: Optional[UserInformation] = None
    bio: Optional[str] = None
    skills: Optional[list] = []
    phone: str = ""
    city: Optional[str] = None
    address: Optional[str] = None
    cv_link: Optional[str] = None
    work_time: int
    created_at: datetime
    updated_at: datetime