from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class NotificationDTO(BaseModel):
    id: str
    content: Optional[str] = ""
    avatar: Optional[str] = ""
    receiver_id: str
    nav_link: Optional[str] = ""
    is_read: Optional[bool] = False
    created_at: Optional[datetime] = None
