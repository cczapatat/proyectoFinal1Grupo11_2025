import os
import logging
from flask import Flask
from sqlalchemy import text
from .models.model import db
from .services.manufacturer_service import ManufacturerService
from .pubsub.subscriber import PubSubSubscriber

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)
    
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Set schema configuration
    db_schema = os.environ.get('DB_SCHEMA', 'manufacturers')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "connect_args": {"options": f"-csearch_path={db_schema}"}
    }
    
    # Initialize database with the app
    db.init_app(app)
    
    return app

def get_database_uri():
    """Create database connection URI from environment variables"""
    db_name = os.environ.get('DB_NAME', 'project_final')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    db_user = os.environ.get('DB_USER', 'user_final')
    db_password = os.environ.get('DB_PASSWORD', 'pass_final')
    db_schema = os.environ.get('DB_SCHEMA', 'manufacturers')
    
    return f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

def create_db_tables(app):
    """Create database tables if they don't exist"""
    with app.app_context():
        # Create the schema if it doesn't exist
        db_schema = os.environ.get('DB_SCHEMA', 'manufacturers')
        with db.engine.connect() as connection:
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {db_schema}"))
            logger.info(f"Schema '{db_schema}' created or already exists")
        
        # Apply migrations first
        from .db.migration_manager import MigrationManager
        try:
            MigrationManager.apply_migrations()
            logger.info("Database migrations applied successfully")
        except Exception as e:
            logger.error(f"Error applying migrations: {str(e)}")
            
        # Create any remaining tables using SQLAlchemy models
        db.create_all()
        logger.info("Database tables created")

def start_subscriber(app):
    """Initialize and start the PubSub subscriber"""
    with app.app_context():
        # Create service instances
        manufacturer_service = ManufacturerService()
        
        # Create and start subscriber
        subscriber = PubSubSubscriber(manufacturer_service, app=app)
        subscriber.start_subscription()

def main():
    """Main entry point for the application"""
    try:
        # Create and configure Flask app
        app = create_app()
        
        # Create database tables
        create_db_tables(app)
        
        # Start subscriber
        start_subscriber(app)
        
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        raise

if __name__ == "__main__":
    main()