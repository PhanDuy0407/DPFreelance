from typing import Optional
from pydantic import BaseModel, validator
import re

class Account(BaseModel):
    username: str
    password: str

class RegisterAccount(Account):
    username: str
    password: str
    fname : Optional[str]
    lname : Optional[str]
    avatar: Optional[str]
    email: str

    @validator('username')
    def username_pattern(cls, v):
        # Username must be alphanumeric and underscores only, between 3 to 20 characters
        if not v.isalnum() or len(v) < 3 or len(v) > 20:
            raise ValueError('Username must be alphanumeric, underscores only, between 3 to 20 characters')
        return v

    @validator('password')
    def password_pattern(cls, v):
        # Password must be at least 6 characters long, containing at least one uppercase letter, one lowercase letter, one digit, and one special character
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
        if not re.match(pattern, v):
            raise ValueError('Password must be at least 6 characters long with at least one uppercase letter, one lowercase letter, one digit, and one special character (@$!%*?&)')
        return v

class ResetPassword(BaseModel):
    old_password: str
    new_password: str