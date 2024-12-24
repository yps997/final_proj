from ..models import Base
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship


class TheDate(Base):
    __tablename__ = 'dates'
    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(Date)

    events = relationship('Event', back_populates='date')

    def __repr__(self):
        return f"<Date(id={self.id}, date={self.date})>"