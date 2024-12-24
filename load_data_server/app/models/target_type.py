from ..models import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class TargetType(Base):
    __tablename__ = "target_types"
    id = Column(Integer, autoincrement=True, primary_key=True)
    target_type = Column(String)

    events = relationship('Event', back_populates='target_type')