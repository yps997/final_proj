from ..models import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class AttackType(Base):
    __tablename__ = "attack_types"
    id = Column(Integer, autoincrement=True, primary_key=True)
    attack_type = Column(String)

    events = relationship('Event', back_populates='attack_type')