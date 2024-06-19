from typing import Optional
from pydantic import BaseModel

class Applicant(BaseModel):
    title: Optional[str] = None
    bio: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    skills: Optional[list] = []
    cv_link: Optional[str] = None
    work_time: int
    phone: str