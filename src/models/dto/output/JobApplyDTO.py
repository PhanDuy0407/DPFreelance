from datetime import datetime
from pydantic import BaseModel
from models.dto.output.JobDTO import JobDTO 

class JobApplyDTO(BaseModel):
    job: JobDTO
    pricing: int
    experience_description: str
    plan_description: str
    status: str
    created_at: datetime