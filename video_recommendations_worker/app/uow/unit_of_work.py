from contextlib import asynccontextmanager
from app.core.db import SessionLocal

class UnitOfWork:
    """
    Context manager for database transactions
    Ensures proper session management and rollback on errors
    """
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = SessionLocal()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Rollback on error
            self.session.rollback()
        else:
            # Commit if no error
            self.session.commit()
        
        # Always close the session
        self.session.close()

