from typing import Optional
from pydantic import BaseModel

class CategoryDTO(BaseModel):
    id: str
    name: str
    parent_id: Optional[str]
    level: int