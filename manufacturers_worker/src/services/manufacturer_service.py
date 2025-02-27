import logging
import uuid
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from ..models.model import db, Manufacturer, ManufacturerSchema, Error, ErrorSchema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManufacturerService:
    def __init__(self):
        """Initialize the manufacturer service with validation schemas"""
        self.manufacturer_schema = ManufacturerSchema(session=db.session)
        self.error_schema = ErrorSchema()
    
    def _validate_batch_against_database(self, valid_manufacturers):
        """Validate a batch of manufacturers against the database
        
        Args:
            valid_manufacturers (list): List of validated Manufacturer objects
            
        Returns:
            tuple: (list of non-duplicate manufacturers, dict of duplicates with their indices)
        """
        # Extract nombre and nit pairs from valid manufacturers
        nombres_nits = [(m.nombre, m.nit) for m in valid_manufacturers]
        
        # If empty batch, just return
        if not nombres_nits:
            return [], {}
            
        # Build a query to find all existing nombre/nit combinations in one database query
        # This is much more efficient than checking one by one
        from sqlalchemy import or_
        conditions = []
        for nombre, nit in nombres_nits:
            conditions.append(
                db.and_(
                    Manufacturer.nombre == nombre,
                    Manufacturer.nit == nit
                )
            )
        
        # Execute the query to get existing records
        existing_records = Manufacturer.query.filter(
            or_(*conditions)
        ).with_entities(Manufacturer.nombre, Manufacturer.nit).all()
        
        # Convert to set for faster lookup
        existing_pairs = set((rec.nombre, rec.nit) for rec in existing_records)
        
        # Find duplicates and their indices
        non_duplicates = []
        duplicates = {}
        
        for i, manufacturer in enumerate(valid_manufacturers):
            pair = (manufacturer.nombre, manufacturer.nit)
            if pair in existing_pairs:
                duplicates[i] = manufacturer
            else:
                non_duplicates.append(manufacturer)
                
        return non_duplicates, duplicates

    def process_batch(self, transaction_id, batch_number, manufacturers):
        """Process a batch of manufacturer objects

        Args:
            transaction_id (str): UUID for tracking the batch transaction
            batch_number (int): Sequential number of the batch
            manufacturers (list): List of manufacturer dictionaries to process
        """
        logger.info(f"Processing batch {batch_number} with {len(manufacturers)} manufacturers")
        
        # Ensure we don't process more than 100 items per batch
        max_batch_size = 100
        if len(manufacturers) > max_batch_size:
            logger.warning(f"Batch size exceeds maximum of {max_batch_size}. Truncating to {max_batch_size} items.")
            manufacturers = manufacturers[:max_batch_size]
        
        try:
            # Convert string transaction_id to UUID if necessary
            if isinstance(transaction_id, str):
                transaction_id = uuid.UUID(transaction_id)
                
            # Pre-validate all manufacturers to check for duplicates within the current batch
            valid_manufacturers = []
            nombre_nit_to_index = {}  # For tracking original indices
            
            # First pass: validate and check for duplicates within the batch
            for index, manufacturer_data in enumerate(manufacturers):
                try:
                    # Basic validation using schema
                    manufacturer = self.manufacturer_schema.load(manufacturer_data)
                    
                    # Check for duplicates within the batch
                    pair = (manufacturer.nombre, manufacturer.nit)
                    if pair in nombre_nit_to_index:
                        self._handle_error(
                            transaction_id=transaction_id,
                            batch_number=batch_number,
                            line_number=index + 1,
                            error_dict={"batch_duplicate": f"Duplicate nombre and nit within batch: {manufacturer.nombre}, {manufacturer.nit}"}
                        )
                        continue
                    
                    # Add to valid list and record the nombre/nit
                    valid_manufacturers.append(manufacturer)
                    nombre_nit_to_index[pair] = index
                    
                except ValidationError as ve:
                    # Handle validation errors
                    self._handle_error(
                        transaction_id=transaction_id,
                        batch_number=batch_number,
                        line_number=index + 1,
                        error_dict=ve.messages
                    )
            
            # Validate the batch against the database
            non_duplicates, duplicates = self._validate_batch_against_database(valid_manufacturers)
            
            # Handle duplicates found in the database
            for idx, duplicate in duplicates.items():
                original_index = list(nombre_nit_to_index.values()).index(idx)
                self._handle_error(
                    transaction_id=transaction_id,
                    batch_number=batch_number,
                    line_number=original_index + 1,
                    error_dict={"database": f"Duplicate record: nombre '{duplicate.nombre}' and nit '{duplicate.nit}' already exist in database"}
                )
            
            # Save non-duplicates to the database in bulk
            if non_duplicates:
                try:
                    db.session.bulk_save_objects(non_duplicates)
                    db.session.commit()
                    logger.info(f"Saved {len(non_duplicates)} manufacturers")
                except IntegrityError as ie:
                    # Unexpected integrity error (should not happen after validation)
                    db.session.rollback()
                    logger.error(f"Unexpected integrity error during bulk save: {str(ie)}")
                except Exception as e:
                    # Handle unexpected errors
                    db.session.rollback()
                    logger.error(f"Unexpected error during bulk save: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error processing batch: {str(e)}")
            db.session.rollback()
            
    def _handle_error(self, transaction_id, batch_number, line_number, error_dict):
        """Handle errors by saving to the errors table

        Args:
            transaction_id (uuid.UUID): Transaction identifier
            batch_number (int): Batch number
            line_number (int): Line number in the batch where error occurred
            error_dict (dict): Dictionary of validation errors
        """
        # Concatenate error messages
        error_messages = []
        
        # Flatten nested errors if any
        for field, messages in error_dict.items():
            if isinstance(messages, list):
                for message in messages:
                    error_messages.append(message)
            else:
                error_messages.append(messages)
        
        # Create joined error description
        error_description = " and ".join(error_messages)
        
        # Create error record
        error = Error(
            transaction_id=transaction_id,
            batch_number=batch_number,
            line_number=line_number,
            description=error_description
        )
        
        # Save error to database
        db.session.add(error)
        db.session.commit()
        
        logger.warning(f"Error saved for batch {batch_number}, line {line_number}: {error_description}")