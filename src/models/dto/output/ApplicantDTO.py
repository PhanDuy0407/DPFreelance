from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.dto.output.UserInformation import UserInformation

class ApplicantDTO(BaseModel):
    id: str
    information: Optional[UserInformation] = None
    bio: Optional[str] = None
    skills: Optional[dict] = {}
    phone: str = ""
    cv_link: Optional[str] = None
    created_at: datetime
    updated_at: datetime