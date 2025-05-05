from enum import Enum

class Operation(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"

class BULK_STATUS(Enum):
    BULK_QUEUED = "QUEUED"
    BUlK_FAILED = "FAILED"
    BULK_COMPLETED = "COMPLETED"