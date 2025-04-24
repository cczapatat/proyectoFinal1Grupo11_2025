import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.db import Base, engine

import sys
import os

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../..")

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Creates the database schema before running tests and drops it afterward.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """
    Provides a TestClient instance for testing the FastAPI application.
    """
    with TestClient(app) as test_client:
        yield test_client