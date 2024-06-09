from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class JobApplyDTO(BaseModel):
    pricing: int
    experience_description: str
    plan_description: str
    status: str
    created_at: datetime
    applied_at: Optional[datetime] = None