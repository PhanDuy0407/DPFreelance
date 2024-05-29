from typing import Optional
from pydantic import BaseModel

class Applicant(BaseModel):
    bio: Optional[str] = None
    skills: Optional[dict] = {}
    cv_link: Optional[str] = None
    work_time: int
    phone: str