from sqlalchemy import Column, Integer, String
from models.base import Base

class Area(Base):
    __tablename__ = 'areas'

    areaid = Column(Integer, primary_key=True)
    areaname = Column(String, unique=True, nullable=False)
