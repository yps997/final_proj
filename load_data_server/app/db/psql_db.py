import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Index
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from ..models import Base, Event, AttackType, TargetType, Province, Region, Country, City, TheDate

load_dotenv(verbose=True)

database_url = os.environ['POSTGRES_URL']
engine = create_engine(database_url)

_session_maker = sessionmaker(bind=engine)

def create_db():
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
    except Exception as e:
        print(str(e))

def create_tables():
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    except Exception as e:
        print(str(e))

def session_maker():
    return _session_maker()

def create_indexes():
    try:
        Index("idx_tergro", Event.terror_group)
        Index("idx_city", City.city)
        Index("idx_country", Country.country)
        Index("idx_region", Region.region)
        Index("idx_province", Province.province)
        Index("idx_tarty", TargetType.target_type)
        Index("idx_atty", AttackType.attack_type)
        Index("idx_date", TheDate.date)

    except Exception as e:
        print(str(e))
