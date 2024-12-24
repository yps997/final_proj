from ..models import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, autoincrement=True, primary_key=True)
    region = Column(String)

    events = relationship('Event', back_populates='region')

    def __repr__(self):
        return f"<Region(id={self.id}, region='{self.region}')>"