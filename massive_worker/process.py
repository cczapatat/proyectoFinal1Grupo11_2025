import os
import gc
import json
import datetime
import requests
import csv
import io
from typing import Union
from google.cloud import pubsub_v1
from models.attempt import Attempt
from models.manufacture_batch import ManufactureBatch, OPERATION_BATCH
from models.declarative_base import session

project_id = os.environ.get('GCP_PROJECT_ID', 'proyectofinalmiso2025')
attemps_subscription_id = os.environ.get('GCP_MANUFACTURE_MASSIVE_SUB', 'commands_to_massive-sub')
attemps_name_pub = os.environ.get('GCP_MANUFACTURE_MASSIVE_TOPIC', 'commands_to_massive')

manufactures_name_pub = os.environ.get('GCP_MANUFACTURE_TOPIC', 'commands_to_manufactures')
host_document_manager = os.environ.get('DOCUMENT_MANAGER_PATH', 'http://130.211.32.9')
x_token = os.environ.get('INTERNAL_TOKEN', 'internal_token')

headers = {
    'x-token': x_token
}

publisher_manufactures = pubsub_v1.PublisherClient()
topic_path_manufacture = publisher_manufactures.topic_path(project_id, manufactures_name_pub)

publisher_retry_attemp = pubsub_v1.PublisherClient()
topic_path_attempt = publisher_retry_attemp.topic_path(project_id, attemps_name_pub)


def __create_attempt__(operation, entity, process_id, file_id, user_email) -> bool:
    try:
        attempt = Attempt(
            operation=operation.upper(),
            entity=entity.upper(),
            process_id=process_id,
            file_id=file_id,
            user_email=user_email,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )

        session.add(attempt)
        session.commit()

        print('[Process Attemps][__create_attemp__] process_id: {}, attempt: {}'.format(str(process_id), str(attempt)))

        return attempt
    except Exception as ex:
        session.rollback()
        print('[Process Attemps][__create_attemp__] process_id: {}, error {}'.format(str(process_id), str(ex)))
        return False


def __create_manufacture_proccessed__(process_id, file_id, user_email, future, current_batch,
                                      number_of_batches) -> bool:
    try:
        manufacture_batch = ManufactureBatch(
            operation=OPERATION_BATCH.EXECUTED,
            process_id=process_id,
            file_id=file_id,
            user_email=user_email,
            future=future,
            current_batch=current_batch,
            number_of_batches=number_of_batches,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        session.add(manufacture_batch)
        session.commit()

        print('[Process Attemps][__create_manufacture_proccessed__] process_id: {}, manufacture_batch: {}'.format(
            str(process_id), str(manufacture_batch.__dict__)))

        return manufacture_batch
    except Exception as ex:
        session.rollback()
        print('[Process Attemps][__create_manufacture_proccessed__] process_id: {}, error {}'.format(str(process_id),
                                                                                                     str(ex)))
        return False


def __create_and_process__(operation, entity, process_id, file_id, user_email) -> Union[Attempt, bool]:
    attempt = __create_attempt__(operation, entity, process_id, file_id, user_email)

    if not attempt:
        print('[Process Attemps][__create_and_process__] process_id: {}, error {}'.format(str(process_id),
                                                                                          'Error creating attempt'))
        return Attempt()

    return attempt


def publish_massive_manufactures(process_id, file_id, user_email, json_data):
    batch_size = 100
    total_rows = len(json_data)
    current_batch = 0
    number_of_batches = total_rows / batch_size
    batch = {}

    for i in range(0, total_rows, batch_size):
        batch["transaction_id"] = process_id
        batch["batch_number"] = current_batch
        batch["manufacturers"] = json_data[i:i + batch_size]
        print(f"[Process Manufactures] batch: {batch}")

        data_str = json.dumps(batch).encode("utf-8")
        print(f"[Process Manufactures] Publishing to {topic_path_manufacture} the message: {data_str}")

        future = publisher_manufactures.publish(topic_path_manufacture, data_str)
        result = future.result()
        print(f"[Process Manufactures] process_id: {process_id} future: {result}")
        __create_manufacture_proccessed__(process_id, file_id, user_email, str(result), current_batch,
                                          number_of_batches)

        current_batch += 1


def get_json_object_from_document(file_id):
    url = f"{host_document_manager}/document-manager/document/{file_id}/file"
    print(f"[GET Document] Getting file from {url}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[Get Document] Failed to get file from {url}, status code: {response.status_code}")
        return None

    csv_content = response.text
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    json_data = [row for row in csv_reader]

    return json_data


def process_attemps(message):
    print(f"[Process Attemps] Received on pubSub: {message}")
    gc.collect()
    try:
        input_data = json.loads(message.data.decode("utf-8"))

        print('[Process Attemps] input_data: {}'.format(str(input_data)))

        operation = input_data["operation"]
        entity = input_data["entity"]
        process_id = input_data["process_id"]
        file_id = input_data["file_id"]
        user_email = input_data["user_email"]

        if operation is None:
            print('[Process Attemps] operation is incorrect, input: {}'.format(str(input_data)))
            return

        if entity is None:
            print('[Process Attemps] entity {} is not exists'.format(str(entity)))
            return

        if process_id is None:
            print('[Process Attemps] process_id {} is not exists'.format(str(process_id)))
            return

        if file_id is None:
            print('[Process Attemps] bulk_file_url {} is not exists'.format(str(file_id)))
            return

        if user_email is None:
            print('[Process Attemps] user_email {} is not exists'.format(str(user_email)))
            return

        json_data_file = get_json_object_from_document(file_id)

        if json_data_file is None:
            print('[Process Attemps] json_data_file is None')

            future = publisher_retry_attemp.publish(topic_path_attempt, message.data)
            print(future.result())

            return

        attempt = __create_and_process__(operation, entity, process_id, file_id, user_email)

        if not attempt:
            print("[Process Attemps] Error creating attempt")
            return

        print(
            f"[Process Attemps] attempt {str(attempt.id)} with process_id {str(attempt.process_id)} by user {attempt.user_email} created")

        publish_massive_manufactures(process_id, file_id, user_email, json_data_file)

    except Exception as ex:
        print(f"[Process Attemps] Error Generate during PubSub, {str(ex)}")

    message.ack()
    gc.collect()


if __name__ == '__main__':
    subscriber = pubsub_v1.SubscriberClient()
    attemps_subscription_path = subscriber.subscription_path(project_id, attemps_subscription_id)

    flow_control = pubsub_v1.types.FlowControl(max_messages=1)

    streaming_pull_future = subscriber.subscribe(
        attemps_subscription_path,
        callback=process_attemps
    )

    print(f"[Process Attemps] Process_Listening for messages on {attemps_subscription_path}..\n")

    with subscriber:
        try:
            streaming_pull_future.result()
        except Exception as ex:
            print(f"[Process Attemps] Listening generated an error: {str(ex)}")
            streaming_pull_future.cancel()
            streaming_pull_future.result()
