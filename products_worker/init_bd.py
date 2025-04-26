from .models.declarative_base import Base, engine
from .models.bulk_task_model import BulkTask
from .models.product_model import Product

print("[DB-Init] Running...")

with engine.connect() as connection:
    connection.commit()
    print("[DB-Init] Finished Schema Creation")

print("BulkTask:: {}".format(BulkTask.__table__))
print("Product:: {}".format(Product.__table__))
Base.metadata.create_all(engine)
print("[DB-Init] Finished")