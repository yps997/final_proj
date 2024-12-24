import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv(verbose=True)

elastic_client = Elasticsearch(
   ['http://localhost:9200'],
   basic_auth=("elastic", "eda7CkVD"),
   verify_certs=False
)
