from typing import Optional
from pydantic import BaseModel

class ResponseModel(BaseModel):
    data: Optional[object] = None
    detail: Optional[str] = None

class ListResponseModel(ResponseModel):
    total: Optional[int]