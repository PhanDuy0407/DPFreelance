from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from models.data.BaseModel import BaseModel
from datetime import datetime

from common.database_connection import Base


class JobApply(Base, BaseModel):
    __tablename__ = "job_apply"

    applicant_id = Column(String, primary_key=True)
    job_id = Column(String, primary_key=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    applied_at = Column(DateTime)
    done_at = Column(DateTime)

    @staticmethod
    def filter_fields():
        return ["applied_at", "created_at", "done_at", "status"]