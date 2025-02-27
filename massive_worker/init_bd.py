from sqlalchemy import text
from models.declarative_base import Base, engine

print("[DB-Init] Running...")

# Create custom schema if it does not exist
custom_schema = 'massive_worker'
with engine.connect() as connection:
    connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {custom_schema}"))
Base.metadata.schema = custom_schema
Base.metadata.create_all(engine)
print("[DB-Init] Finished")