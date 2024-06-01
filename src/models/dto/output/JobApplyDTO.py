from datetime import datetime
from pydantic import BaseModel
from models.dto.output.JobDTO import JobDTO 
from models.dto.output.ApplicantDTO import ApplicantDTO 

class JobApplyDTO(BaseModel):
    pricing: int
    experience_description: str
    plan_description: str
    status: str
    created_at: datetime

class RecruiterJobPricing(JobApplyDTO):
    applicant: ApplicantDTO

class ApplicantJobPricing(JobApplyDTO):
    job: JobDTO