from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from models.data.BaseModel import BaseModel

from common.database_connection import Base


class JobApply(Base, BaseModel):
    __tablename__ = "job_apply"

    applicant_id = Column(String, primary_key=True)
    job_id = Column(String, primary_key=True)
    pricing = Column(Integer)
    experience_description = Column(String)
    plan_description = Column(String)
    status = Column(String)
    created_at = Column(DateTime)