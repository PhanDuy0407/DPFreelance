from typing import Optional
from pydantic import BaseModel

class UserInformation(BaseModel):
    fname: Optional[str]
    lname: Optional[str]
    avatar: Optional[str]
    email: Optional[str]
