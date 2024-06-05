from typing import Optional
from pydantic import BaseModel

class Account(BaseModel):
    username: str
    password: str

class RegisterAccount(Account):
    fname : Optional[str]
    lname : Optional[str]
    email: str
