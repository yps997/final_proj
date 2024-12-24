import pandas as pd
from pandas import DataFrame
from sqlalchemy.orm import Query
from toolz import *
import numpy as np



def convert_to_dataframe(results):
    column_names = [
        "terror_group", "date", "country", "region", "city", "latitude", "longitude", "target_type"
    ]
    data = [
        {column: value for column, value in zip(column_names, row)}
        for row in results
    ]
    return DataFrame(data)

def calculate_fatal_score(df: DataFrame, limit):
    df["fatal_score"] = (df["kill_number"].fillna(0) * 2) + (df["wound_number"].fillna(0) * 1)
    top_events = df.sort_values(by="fatal_score", ascending=False).head(limit)
    return top_events


def calculate_correlation_from_results(result1, result2, key1, key2):
    values1 = [row[key1] for row in result1]
    values2 = [row[key2] for row in result2]

    correlation = np.corrcoef(values1, values2)[0, 1]

    return correlation


def calculate_percentage_change_attacks_by_region(res):
    df = pd.DataFrame(res, columns=["country", "city", "region", "date", "attack_count", "longitude", "latitude"])
    df["percentage_change"] = (
            df.groupby("region")["attack_count"]
            .pct_change() * 100
    )
    df = df.dropna()
    return df.to_dict(orient="records")
