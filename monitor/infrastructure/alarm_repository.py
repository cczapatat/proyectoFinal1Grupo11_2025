import uuid
from datetime import datetime
from typing import List

from ..config.db import db
from ..dtos.alarm_in_dto import AlarmInDTO
from ..models.alarm import Alarm
from ..models.alarm_trigger import AlarmTrigger


class AlarmRepository:

    @staticmethod
    def create_alarm(alarm_id: uuid, alarm_dto: AlarmInDTO) -> Alarm:
        alarm = Alarm()
        alarm.id = alarm_id,
        alarm.user_id = alarm_dto.user_id
        alarm.manufacture_id = alarm_dto.manufacture_id
        alarm.product_id = alarm_dto.product_id
        alarm.minimum_value = alarm_dto.minimum_value
        alarm.maximum_value = alarm_dto.maximum_value
        alarm.notes = alarm_dto.notes
        alarm.created_at = datetime.now()
        alarm.updated_at = datetime.now()

        db.session.add(alarm)
        return alarm

    @staticmethod
    def create_alarms_trigger(alarms: list[dict]) -> list[AlarmTrigger]:
        alarms_triggered = []
        for alarm in alarms:
            alarm_trigger = AlarmTrigger()
            alarm_trigger.id = uuid.uuid4()
            alarm_trigger.alarm_id = alarm['alarm_id']
            alarm_trigger.stock_id = alarm['stock_id']
            alarm_trigger.product_id = alarm['product_id']
            alarm_trigger.minimum_value = alarm['minimum_value']
            alarm_trigger.maximum_value = alarm['maximum_value']
            alarm_trigger.new_stock_unit = alarm['new_stock_unit']
            alarm_trigger.created_at = datetime.now()
            alarm_trigger.updated_at = datetime.now()

            db.session.add(alarm_trigger)
            alarms_triggered.append(alarm_trigger)

        db.session.commit()
        return alarms_triggered

    @staticmethod
    def get_alarm_by_product_id_and_limits(product_id: str, new_stock_unit: int) -> List[Alarm]:
        alarms = db.session.query(Alarm).filter(
            Alarm.product_id == product_id,
            (
                    (new_stock_unit < Alarm.minimum_value) |
                    (new_stock_unit > Alarm.maximum_value)
            )
        ).all()

        return alarms
