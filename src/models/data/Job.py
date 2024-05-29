from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from models.data.BaseModel import BaseModel

from common.database_connection import Base


class Job(Base, BaseModel):
    __tablename__ = "job"

    id = Column(String, primary_key=True)
    name = Column(String)
    category_id = Column(String)
    poster_id = Column(String)
    description = Column(String)
    jd_file = Column(String)
    price = Column(Integer)
    price_unit = Column(String)
    type = Column(String)
    status = Column(String)
    estimate_time = Column(String)
    end_date = Column(DateTime)
    created_at = Column(DateTime)