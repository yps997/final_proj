import json
from kafka import KafkaProducer

from dotenv import load_dotenv

load_dotenv(verbose=True)

def produce(data, topic):
    print(f"producer sending to {topic}")
    producer = KafkaProducer(
        bootstrap_servers="172.19.116.76:9092",
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.send(
        topic,
        value=data,
    )
    producer.flush()
    print(data)
    print(f"producer finished sending to {topic}")
