from app.dtos.update_stock_attempt_dto import UpdateAttemptDTO
from app.models.update_stock_attempt import UpdateStockAttempt, UpdateStatus
from datetime import datetime
from app.dtos.product_update_dto import ProductUpdateDTO
from typing import List

def map_pubsub_message_to_update_attempt_dto(message: dict) -> UpdateAttemptDTO:
    return UpdateAttemptDTO(**message)

def map_update_attempt_dto_to_model(dto: UpdateAttemptDTO) -> UpdateStockAttempt:
    return UpdateStockAttempt(
        transaction_id=dto.id,
        status=UpdateStatus.RECEIVED,
        creation_date=datetime.utcnow(),
        last_update_date=datetime.utcnow()
    )


def map_pubsub_message_to_product_updates(message: list) -> List[ProductUpdateDTO]:
    return [ProductUpdateDTO(**item) for item in message]