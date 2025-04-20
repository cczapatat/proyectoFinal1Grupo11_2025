import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

# PostgresSQL configuration
host = os.environ.get('DB_HOST', 'localhost')
port = os.environ.get('DB_PORT', 5432)
user = os.environ.get('DB_USER', 'postgres')
password = os.environ.get('DB_PASSWORD', 'postgres')
database_name = os.environ.get('DB_NAME', 'project_final')

url = URL.create(
    drivername="postgresql",
    host=host,
    port=port,
    username=user,
    password=password,
    database=database_name
)
engine = create_engine(url)
Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
session = Session()

