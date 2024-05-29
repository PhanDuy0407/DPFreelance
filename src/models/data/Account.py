from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from models.data.BaseModel import BaseModel
from datetime import datetime

from common.database_connection import Base


class Account(Base, BaseModel):
    __tablename__ = "account"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    fname = Column(String)
    lname = Column(String)
    avatar = Column(String)
    enable = Column(Boolean, default=1)
    is_admin = Column(Boolean, default=0)
    created_at = Column(DateTime, default=datetime.now)