from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.dto.output.RecruiterDTO import RecruiterInfoDTO
from models.dto.output.ApplicantDTO import ApplicantDTO

class Account(BaseModel):
    id : str
    username : str
    email : str
    fname : Optional[str]
    lname : Optional[str]
    avatar : Optional[str]
    enable : bool
    applicant: Optional[ApplicantDTO]
    recruiter: Optional[RecruiterInfoDTO]
    is_admin: bool
    created_at : datetime