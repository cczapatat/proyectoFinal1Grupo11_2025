import os
import pytest
from seller import create_app
from seller.config.db import db as _db
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture(scope='function')
def app():
    app = create_app()
    app.config['TESTING'] = True
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def db(app):
    """Get the database instance."""
    return _db

@pytest.fixture
def db_session(db):
    """Session for SQLAlchemy."""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    session = scoped_session(
        sessionmaker(bind=connection)
    )
    
    db.session = session
    
    yield session
    
    transaction.rollback()
    session.remove()
    connection.close()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def headers():
    return {
        'x-token': os.getenv('INTERNAL_TOKEN', default='internal_token'),
        'Content-Type': 'application/json'
    }