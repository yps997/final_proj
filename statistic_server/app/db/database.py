import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(verbose=True)

database_url = os.environ['POSTGRES_URL']
engine = create_engine(database_url)

_session_maker = sessionmaker(bind=engine)

def session_maker():
    return _session_maker()