from app.core.db import SessionLocal

class UnitOfWork:
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = SessionLocal()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()
