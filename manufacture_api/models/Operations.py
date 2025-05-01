from enum import Enum

class Operation(Enum):
    CREATE = "CREATE"

class BULK_STATUS(Enum):
    BULK_QUEUED = "BULK QUEUED"
    BUlK_FAILED = "FAILED"
    BULK_COMPLETED = "COMPLETED"