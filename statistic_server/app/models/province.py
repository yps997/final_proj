from ..models import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Province(Base):
    __tablename__ = 'provinces'
    id = Column(Integer, autoincrement=True, primary_key=True)
    province = Column(String)

    events = relationship('Event', back_populates='province')

    def __repr__(self):
        return f"<Province(id={self.id}, city='{self.province}')>"