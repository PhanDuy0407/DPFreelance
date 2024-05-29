from typing import Optional
from pydantic import BaseModel

class Account(BaseModel):
    username: str
    password: str

class RegisterAccount(Account):
    fname : str
    lname : str
    email: Optional[str] = None
