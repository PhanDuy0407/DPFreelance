from pydantic import BaseModel

class Recruiter(BaseModel):
    recruiter_email: str
    phone: str