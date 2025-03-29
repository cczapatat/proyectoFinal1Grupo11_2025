from seller.config import db

def test_db_connection():
    # Verify that the db instance is available
    assert db is not None