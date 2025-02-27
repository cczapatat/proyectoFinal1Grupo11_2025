import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

# PostgresSQL configuration
host = os.environ.get('HOST_PG', 'localhost')
port = os.environ.get('PORT_PG', 5432)
user = os.environ.get('USER_PG', 'postgres')
password = os.environ.get('PWD_PG', 'postgres')
database_name = os.environ.get('DB_NAME_PG', 'massive_worker')

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

