from typing import Optional
from pydantic import BaseModel, validator
import re
class Applicant(BaseModel):
    title: str
    bio: str
    city: str
    address: str
    skills: Optional[list] = []
    cv_link: Optional[str] = None
    work_time: int
    phone: str

    @validator('work_time')
    def username_pattern(cls, v):
        if not v > 0:
            raise ValueError('Work time must be greater than 0')
        return v
    
    @validator('phone')
    def validate_phone_number(cls, v):
        pattern = re.compile(r"^(0[3|5|7|8|9][0-9]{8}|(\+84)[3|5|7|8|9][0-9]{8})$")
        if not pattern.match(v):
            raise ValueError('Invalid phone number. A valid phone number must be 10 digits long and begin with 0 or +84 followed by 3, 5, 7, 8, or 9.')
        return v if not v.startswith('+84') else ('0' + v[3:])