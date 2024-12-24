import json
import os
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv(verbose=True)

bootstrap_servers = os.environ["BOOTSTRAP_SERVERS"]

def consume_topic(topic, process_message):
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        for message in consumer:
            process_message(message.value)
            print(message)
            # for data in message.value:
            #     process_message(data)
    except Exception as e:
        print(str(e))