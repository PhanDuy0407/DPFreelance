from sqlalchemy import Boolean, Column, DateTime, Integer, String, JSON
from models.data.BaseModel import BaseModel

from common.database_connection import Base


class Recruiter(Base, BaseModel):
    __tablename__ = "recruiter"

    id = Column(String, primary_key=True)
    account_id = Column(String)
    phone = Column(String, unique=True)
    city = Column(String)
    address = Column(String)
    free_post_attempt = Column(Integer)
    remain_post_attempt = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
