import json
import os
from google.cloud import pubsub_v1

from ..infrastructure.alarm_repository import AlarmRepository
from ..infrastructure.firebase_database import FirebaseDatabase

project_id = os.environ.get('GCP_PROJECT_ID', 'proyectofinalmiso2025')
commands_to_stock_update_name_sub = os.environ.get('GCP_STOCK_UPDATE_SUB', 'commands_to_stock_update-sub')


def _get_subscriber():
    if str(os.getenv('TESTING')).lower() == 'true':
        return subscriber_stock_update
    return pubsub_v1.SubscriberClient()


subscriber_stock_update = pubsub_v1.SubscriberClient()
subscription_path = subscriber_stock_update.subscription_path(project_id, commands_to_stock_update_name_sub)

_alarm_repository: AlarmRepository
_firebase_database: FirebaseDatabase
_flask_app = None


def read_messages(message):
    try:
        payload = json.loads(message.data.decode("utf-8"))
        print(f"[Read Message] Received: payload: {payload}")

        with _flask_app.app_context():
            alarms = _alarm_repository.get_alarm_by_product_id_and_limits(
                product_id=payload['product_id'],
                new_stock_unit=payload['stock_unit']
            )
            if len(alarms) > 0:
                new_triggered_alarms = []
                for alarm in alarms:
                    new_triggered_alarms.append({
                        'alarm_id': alarm.id,
                        'stock_id': payload['stock_id'],
                        'product_id': payload['product_id'],
                        'minimum_value': alarm.minimum_value,
                        'maximum_value': alarm.maximum_value,
                        'new_stock_unit': payload['stock_unit'],
                        'notes': alarm.notes,
                    })
                alarms_triggered = _alarm_repository.create_alarms_trigger(new_triggered_alarms)
                print(f"[Read Message] Alarms triggered: {len(alarms_triggered)}")
                alarms_to_publish = [{
                    'trigger_id': str(alarm_trigger.id),
                    'alarm_id': str(alarm_trigger.alarm_id),
                    'stock_id': alarm_trigger.stock_id,
                    'product_id': alarm_trigger.product_id,
                    'minimum_value': alarm_trigger.minimum_value,
                    'maximum_value': alarm_trigger.maximum_value,
                    'new_stock_unit': alarm_trigger.new_stock_unit,
                    'notes': alarm_trigger.notes,
                } for alarm_trigger in alarms_triggered]
                status = _firebase_database.set_data('/', {'news': alarms_to_publish})
                print(f"[Read Message] Alarms published to Firebase: {len(alarms_to_publish)}, Status: {status}")
            else:
                print("[Read Message] No alarms found for the given product and stock unit.")
                status = _firebase_database.set_data('/', {'news': []})
                print(f"[Read Message] Alarms published to Firebase: 0, Status: {status}")
    except Exception as e:
        print(f"Exception in subscriber: {e}")
    message.ack()


def stock_update_consume_messages(app):
    global _alarm_repository, _firebase_database, _flask_app
    _flask_app = app

    with app.app_context():
        _alarm_repository = AlarmRepository()
        _firebase_database = FirebaseDatabase()

    streaming_pull_future = _get_subscriber().subscribe(subscription_path, callback=read_messages)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result()
    except Exception as e:
        print(f"Exception in subscriber ({subscription_path}): {e}")
        streaming_pull_future.cancel()
