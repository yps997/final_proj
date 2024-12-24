from ..models import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, autoincrement=True, primary_key=True)
    kill_number = Column(Float)
    wound_number = Column(Float)
    terror_group = Column(String)
    killers_number = Column(Integer)
    is_suicide = Column(Boolean)
    summary = Column(Text)

    date_id = Column(Integer, ForeignKey('dates.id'))
    date = relationship('TheDate', back_populates="events")

    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship('City', back_populates='events')

    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship('Country', back_populates='events')

    region_id = Column(Integer, ForeignKey('regions.id'))
    region = relationship('Region', back_populates='events')

    province_id = Column(Integer, ForeignKey('provinces.id'))
    province = relationship('Province', back_populates='events')

    target_type_id = Column(Integer, ForeignKey('target_types.id'))
    target_type = relationship('TargetType', back_populates='events')

    attack_type_id = Column(Integer, ForeignKey('attack_types.id'))
    attack_type = relationship("AttackType", back_populates="events")
