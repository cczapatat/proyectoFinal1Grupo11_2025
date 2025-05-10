import uuid

from ..dtos.alarm_in_dto import AlarmInDTO
from ..infrastructure.alarm_repository import AlarmRepository
from ..infrastructure.transaction import Transaction
from ..models.alarm import Alarm


class AlarmManager:
    def __init__(self):
        self.alarm_repository = AlarmRepository()
        self.transaction = Transaction()

    def create_alarm(self, alarm_in_dto: AlarmInDTO) -> dict:
        def transaction_operations() -> [Alarm]:
            alarm_id = uuid.uuid4()
            alarm_internal = self.alarm_repository.create_alarm(alarm_id, alarm_in_dto)
            return [alarm_internal]

        [alarm] = self.transaction.run(transaction_operations)

        return alarm.to_dict()
