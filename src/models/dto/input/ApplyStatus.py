from pydantic import BaseModel

class ApplyStatus(BaseModel):
    status: str