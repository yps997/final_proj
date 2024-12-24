from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .attack_type import AttackType
from .target_type import TargetType
from .city import City
from .date import TheDate
from .event import Event
from .region import Region
from .country import Country
from .province import Province
