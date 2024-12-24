from .db.psql_db import create_tables, create_db, create_indexes
from .service.insert_service import read_and_insert_terror_data

if __name__ == '__main__':
    create_db()
    create_tables()
    read_and_insert_terror_data()
    create_indexes()