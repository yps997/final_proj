from dotenv import load_dotenv

from .kafka_settings.admin import init_topics
from .service.read_file import read_and_produce_terror_data

load_dotenv(verbose=True)

if __name__ == '__main__':
    try:
        init_topics()
        try:
            read_and_produce_terror_data()
        except Exception as e:
            print(str(e))
    except Exception as e:
        print(str(e))
