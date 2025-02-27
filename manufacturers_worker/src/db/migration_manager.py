import os
import logging
from sqlalchemy import text
from flask import current_app
from .migrations import migrations_path
from ..models.model import db

logger = logging.getLogger(__name__)

class MigrationManager:
    """Manages database migrations using SQL files"""
    
    @staticmethod
    def apply_migrations():
        """Apply all migrations in the migrations directory"""
        logger.info("Applying database migrations...")
        
        # Get all SQL files in the migrations directory
        migration_files = []
        for filename in sorted(os.listdir(migrations_path)):
            if filename.endswith('.sql'):
                migration_files.append(os.path.join(migrations_path, filename))
        
        # Execute each migration file
        for file_path in migration_files:
            try:
                # Read the SQL file
                with open(file_path, 'r') as f:
                    sql = f.read()
                
                # Execute the SQL with schema context
                db_schema = os.environ.get('DB_SCHEMA', 'manufacturers')
                logger.info(f"Executing migration: {os.path.basename(file_path)}")
                # Use the connection with the correct search path to execute the SQL
                with db.engine.connect() as connection:
                    connection.execute(text(f"SET search_path TO {db_schema}"))
                    connection.execute(text(sql))
                    connection.commit()
                logger.info(f"Successfully applied migration: {os.path.basename(file_path)}")
                
            except Exception as e:
                logger.error(f"Error applying migration {os.path.basename(file_path)}: {str(e)}")
                db.session.rollback()
                raise
        
        logger.info("All migrations applied successfully")