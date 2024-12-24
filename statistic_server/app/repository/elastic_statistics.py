from ..db.elastic_db import elastic_client
import os
from dotenv import load_dotenv

from ..service.queries_service import normalize_elastic_response

load_dotenv(verbose=True)


def search_multiple_indexes_fuzzy(keyword, limit=10):
    query = {
        "query": {
            "match": {
                "description": {
                    "query": keyword,
                    "fuzziness": "AUTO"
                }
            }
        },
        "size": limit
    }

    response = elastic_client.search(
        index=f"{os.environ['HISTORICAL_DATA_INDEX']},{os.environ['NOWADAYS_DATA_INDEX']}",
        body=query
    )
    return normalize_elastic_response(response)


def search_news_fuzzy(limit, keyword):
    query = {
        "query": {
            "match": {
                "description": {
                    "query": keyword,
                    "fuzziness": "AUTO"
                }
            }
        },
        "size": limit
    }
    response = elastic_client.search(index=os.environ["NOWADAYS_DATA_INDEX"], body=query)
    return normalize_elastic_response(response)

def search_historic_fuzzy(limit, keyword):
    query = {
        "query": {
            "match": {
                "description": {
                    "query": keyword,
                    "fuzziness": "AUTO"
                }
            }
        },
        "size": limit
    }
    response = elastic_client.search(index=os.environ["HISTORICAL_DATA_INDEX"], body=query)
    return normalize_elastic_response(response)

print(search_historic_fuzzy(10, "kill"))
def search_combined_with_date_fuzzy(limit, keyword, start_date, end_date):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "description": {
                                "query": keyword,
                                "fuzziness": "AUTO"
                            }
                        }
                    }
                ],
                "filter": {
                    "range": {
                        "timestamp": {
                            "gte": start_date,
                            "lte": end_date
                        }
                    }
                }
            }
        },
        "size": limit
    }
    response = elastic_client.search(
        index=f"{os.environ['HISTORICAL_DATA_INDEX']},{os.environ['NOWADAYS_DATA_INDEX']}",
        body=query
    )
    return normalize_elastic_response(response)


