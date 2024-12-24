from dotenv import load_dotenv
from .api.fetch_data import fetch_articles_and_produce

load_dotenv(verbose=True)

if __name__ == '__main__':
    fetch_articles_and_produce()