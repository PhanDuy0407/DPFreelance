from typing import Optional
from pydantic import BaseModel

class Recruiter(BaseModel):
    city: Optional[str] = None
    address: Optional[str] = None
    phone: str