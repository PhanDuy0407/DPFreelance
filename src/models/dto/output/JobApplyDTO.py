from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class JobApplyDTO(BaseModel):
    status: str
    created_at: datetime
    applied_at: Optional[datetime] = None
    done_at: Optional[datetime] = None