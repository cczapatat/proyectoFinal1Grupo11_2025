from .models.declarative_base import Base, engine
from .models.bulk_task_model import BulkTask
from .models.manufacturer_model import Manufacturer

print("[DB-Init] Running...")

print("BulkTask:: {}".format(BulkTask.__table__))
print("Manufacturer:: {}".format(Manufacturer.__table__))
Base.metadata.create_all(engine)
print("[DB-Init] Finished")