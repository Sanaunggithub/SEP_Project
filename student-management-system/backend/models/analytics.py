from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True, index=True)
    metric = Column(String)
    value = Column(Float)
