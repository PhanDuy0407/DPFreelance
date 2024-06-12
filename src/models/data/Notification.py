from sqlalchemy import Boolean, Column, String, DateTime
from models.data.BaseModel import BaseModel
from datetime import datetime

from common.database_connection import Base


class Notification(Base, BaseModel):
    __tablename__ = "notification"

    id = Column(String, primary_key=True)
    receiver_id = Column(String)
    avatar = Column(String)
    content = Column(String)
    nav_link = Column(String)
    is_read = Column(Boolean, default=0)
    created_at = Column(DateTime, default=datetime.now)