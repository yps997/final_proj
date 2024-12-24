import os
import requests
import time
import json

from dotenv import load_dotenv

from ..kafka_settings.producer import produce

load_dotenv(verbose=True)

def fetch_articles_and_produce():
    page_number = 1
    url = "https://eventregistry.org/api/v1/article/getArticles"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "action": "getArticles",
        "keyword": "terror attack",
        "ignoreSourceGroupUri": "paywall/paywalled_sources",
        "articlesPage": page_number,
        "articlesCount": 10,
        "articlesSortBy": "socialScore",
        "articlesSortByAsc": False,
        "dataType": ["news", "pr"],
        "forceMaxDataTimeWindow": 31,
        "resultType": "articles",
        "apiKey": os.environ.get("NEWS_API_KEY")
    }
    while True:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                page_number += 1
                print(response.json())
                produce(response.json(), os.environ['TOPIC_NEWS_DATA'])
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        time.sleep(120)

