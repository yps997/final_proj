from ..models import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, autoincrement=True, primary_key=True)
    city = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)

    events = relationship('Event', back_populates='city')

    def __repr__(self):
        return f"<City(id={self.id}, city='{self.city}', longitude={self.longitude}, latitude={self.latitude})>"