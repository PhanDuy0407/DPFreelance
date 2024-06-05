from sqlalchemy import JSON, Column, Integer, String, DateTime
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
    min_price = Column(Integer)
    max_price = Column(Integer)
    price_unit = Column(String)
    require_skills = Column(JSON)
    type = Column(String)
    status = Column(String)
    estimate_time = Column(String)
    end_date = Column(DateTime)
    created_at = Column(DateTime)

    @staticmethod
    def filter_fields():
        return ["name", "category_id", "min_price", "max_price", "type", "status", "estimate_time", "created_at"]
    
    @staticmethod
    def order_by_fields():
        return ["name", "min_price", "max_price", "type", "status", "estimate_time", "created_at"]