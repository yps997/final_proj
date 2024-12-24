import os
from dotenv import load_dotenv

from ..db.elastic_connect import elastic_client
from ..service.normalize_data import normalize_data

load_dotenv(verbose=True)

def insert(data):
    try:
        print(data)
        if data["groq_response"]['category'] == 'historical terror attack':
            historic_data_entry = {
                "groq_response": data["groq_response"],
                "title": data["title"],
                "body": data["body"]
            }
            res = normalize_data(historic_data_entry)
            elastic_client.index(index=os.environ["HISTORICAL_DATA_INDEX"], document=res)
            print(f"Insert to elastic: {historic_data_entry}")
        if data["groq_response"]['category'] == 'nowadays terror attack':
            new_data_entry = {
                "groq_response": data["groq_response"],
                "title": data["title"],
                "body": data["body"]
            }
            res = normalize_data(new_data_entry)
            elastic_client.index(index=os.environ["NOWADAYS_DATA_INDEX"], document=res)
            print(f"Insert to elastic: {new_data_entry}")
    except Exception as e:
        print(str(e))