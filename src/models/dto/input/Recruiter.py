from typing import Optional
from pydantic import BaseModel

class Recruiter(BaseModel):
    city: Optional[str] = None
    address: Optional[str] = None
    cccd: Optional[str] = None
    company_name: Optional[str] = None
    phone: str