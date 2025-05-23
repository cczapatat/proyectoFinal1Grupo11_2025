from sqlalchemy import text

from .models.declarative_base import Base, engine
from .models.attempt import Attempt
from .models.attempt_error import AttemptError
from .models.entity_batch import EntityBatch

print("[DB-Init] Running...")

# Create custom schema if it does not exist
custom_schema = 'massive_worker'
with engine.connect() as connection:
    connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {custom_schema}"))
    connection.commit()
    print("[DB-Init] Finished Schema Creation")

Base.metadata.schema = custom_schema
print("Attempt:: {}".format(Attempt.__table__))
print("EntityBatch:: {}".format(EntityBatch.__table__))
print("AttemptError:: {}".format(AttemptError.__table__))
Base.metadata.create_all(engine)
print("[DB-Init] Finished")