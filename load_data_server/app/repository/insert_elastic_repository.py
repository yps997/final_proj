from elasticsearch import helpers

from ..db.elastic_db import elastic_client
from ..service.normalize_data import normalize_data_for_elastic
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

def insert_to_elastic(row):
    try:
        print(row)
        res = normalize_data_for_elastic(row)
        elastic_client.index(index=os.environ["HISTORICAL_DATA_INDEX"], document=res)
        print(f"Insert to elastic: {res}")
    except Exception as e:
        print(str(e))

def insert_to_elastic_batch(elastic_messages):
    actions = [
        {
            "_index": os.environ["HISTORICAL_DATA_INDEX"],
            "_source": message
        }
        for message in elastic_messages
    ]
    try:
        helpers.bulk(elastic_client, actions)
    except Exception as e:
        print(f"Error inserting batch to Elasticsearch: {e}")