import os
import time

import faust
from dotenv import load_dotenv
from ..service.send_to_groq_service import merge_response_with_message

load_dotenv(verbose=True)

app = faust.App(
    'terror_data_streaming',
    broker="172.19.116.76:9092",
    value_serializer='json'
)

news_topic = app.topic('fetch_news_topic')

elastic_topic = os.environ['ELASTIC_TOPIC']

processed_topic_for_elastic = app.topic(elastic_topic)

@app.agent(news_topic)
async def process_elastic(messages):
    async for message in messages:
        for sub in message["articles"]["results"]:
            normalize_data = merge_response_with_message(sub)
            if normalize_data:
                await processed_topic_for_elastic.send(value=normalize_data)
                print(f"Processed and sent: {normalize_data}")
                time.sleep(5)
