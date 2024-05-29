from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from models.data.BaseModel import BaseModel

from common.database_connection import Base


class Category(Base, BaseModel):
    __tablename__ = "category"

    id = Column(String, primary_key=True)
    name = Column(String, unique=True)
    parent_id = Column(String)
    level = Column(Integer)