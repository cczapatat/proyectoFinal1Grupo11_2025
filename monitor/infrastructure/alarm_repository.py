from typing import List
import uuid
from datetime import datetime

from sqlalchemy import cast, String
from werkzeug.exceptions import InternalServerError

from ..config.db import db
from ..dtos.alarm_in_dto import AlarmInDTO
from ..models.alarm import Alarm


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
