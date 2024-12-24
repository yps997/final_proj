import os
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
from dotenv import load_dotenv

load_dotenv(verbose=True)

def init_topics():
    client = KafkaAdminClient(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'])
    topics = [os.environ['TOPIC_TERROR_DATA']]

    topics = [NewTopic(
        name=topic,
        num_partitions=int(os.environ['NUM_PARTITIONS']),
        replication_factor=int(os.environ['NUM_REPLICATIONS'])
    ) for topic in topics]

    try:
        client.create_topics(topics)
    except TopicAlreadyExistsError as e:
        print(str(e))
    finally:
        client.close()

if __name__ == '__main__':
    init_topics()