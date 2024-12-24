from ..db.psql_db import session_maker
from ..repository.insert_elastic_repository import insert_to_elastic, insert_to_elastic_batch
from ..repository.insert_psql_repository import insert_psql
from ..service.normalize_data import normalize_message, normalized_message_to_model, normalize_data_for_elastic
from ..service.read_file import read_csv, terror_data_path1


# def read_and_insert_terror_data():
#     insert_number = 1
#     terror_data = read_csv(terror_data_path1)
#     for terror in terror_data:
#         normalize_data = normalize_message(terror)
#         insert_normalized_message(normalize_data, session=session_maker)
#         insert_to_elastic(terror)
#         print(insert_number)
#         insert_number+=1



def read_and_insert_terror_data(batch_size=2000):
    insert_num = batch_size
    terror_data = read_csv(terror_data_path1)
    normalized_batch = []
    elastic_batch = []

    for terror in terror_data:
        normalize_data = normalized_message_to_model(terror)
        normalized_batch.append(normalize_data)

        elastic_data = normalize_data_for_elastic(terror)
        elastic_batch.append(elastic_data)

        if len(normalized_batch) == batch_size:
            insert_psql(session=session_maker, normalized_messages=normalized_batch)
            insert_to_elastic_batch(elastic_batch)
            print(f"Inserted batch {len(normalized_batch)}")
            insert_num += len(normalized_batch)

            normalized_batch.clear()
            elastic_batch.clear()

    if normalized_batch:
        insert_psql(session=session_maker, normalized_messages=normalized_batch)
        insert_to_elastic_batch(elastic_batch)
        print(f"Inserted last batch {batch_size}")
        batch_size += len(normalized_batch)
