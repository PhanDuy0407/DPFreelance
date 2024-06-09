from sqlalchemy import Boolean, Column, DateTime, Integer, String, JSON
from models.data.BaseModel import BaseModel

from common.database_connection import Base


class Applicant(Base, BaseModel):
    __tablename__ = "applicant"

    id = Column(String, primary_key=True)
    account_id = Column(String, primary_key=True)
    bio = Column(String)
    skills = Column(JSON)
    phone = Column(String, unique=True)
    work_time = Column(Integer)
    cv_link = Column(String)
    city = Column(String)
    address = Column(String)
    saved_jobs = Column(JSON, default="[]")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
