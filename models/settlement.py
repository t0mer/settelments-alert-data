from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.area import Area

class Settlement(Base):
    __tablename__ = 'settlements'

    settlementid = Column(Integer, primary_key=True)
    settlementname = Column(String, nullable=False)
    migun_time = Column(Integer, nullable=False)
    rashut = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    areaid = Column(Integer, ForeignKey('areas.areaid'))

    area = relationship("Area", back_populates="settlements")

Area.settlements = relationship("Settlement", order_by=Settlement.settlementid, back_populates="area")
