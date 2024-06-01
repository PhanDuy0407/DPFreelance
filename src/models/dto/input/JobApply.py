from datetime import datetime
from pydantic import BaseModel

class JobApply(BaseModel):
    pricing: int
    experience_description: str
    plan_description: str

class JobApplyStatus(BaseModel):
    status: str