import csv
import json
import os

from ..kafka_settings.producer import produce


def read_csv(csv_path: str):
    try:
        with open(csv_path, mode='r', encoding='iso-8859-1') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


terror_data_path = "./data/globalterrorismdb_0718dist-1000 rows.csv"


def read_and_produce_terror_data():
    terror_data = read_csv(terror_data_path)
    batch_size = 200
    batch = []
    for terror in terror_data:
        batch.append(terror)
        if len(batch) == batch_size:
            produce(batch, os.environ['TOPIC_TERROR_DATA'])
            batch = []
    if batch:
        produce(batch, os.environ['TOPIC_TERROR_DATA'])