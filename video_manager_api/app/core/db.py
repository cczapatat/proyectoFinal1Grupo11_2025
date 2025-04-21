import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_NAME = os.environ.get('DB_NAME', 'project_final')
DB_TYPE = os.environ.get('DB_TYPE', 'postgresql')

database_url = URL.create(
    drivername=DB_TYPE,
    host=DB_HOST,
    port=DB_PORT,
    username=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)

def create_db_if_not_exists(url):
    target_db = url.database
    url_without_db = url.set(database="postgres")
    engine_without_db = create_engine(url_without_db)
    with engine_without_db.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{target_db}'"))
        exists = result.scalar() is not None
        if not exists:
            conn.execute(text(f"CREATE DATABASE {target_db}"))
    engine_without_db.dispose()

create_db_if_not_exists(database_url)
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)
Base = declarative_base()