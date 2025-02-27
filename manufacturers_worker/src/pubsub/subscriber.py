import json
import os
import logging
from google.cloud import pubsub_v1
from ..services.manufacturer_service import ManufacturerService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PubSubSubscriber:
    def __init__(self, manufacturer_service, app=None):
        """Initialize the PubSub subscriber with service dependencies

        Args:
            manufacturer_service (ManufacturerService): Service to process manufacturer data
            app: Flask application instance for creating application context
        """
        self.manufacturer_service = manufacturer_service
        self.app = app
        self.project_id = os.environ.get('GCP_PROJECT_ID')
        self.subscription_id = os.environ.get('SUBSCRIPTION_ID')
        
        # Initialize subscriber client
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(
            self.project_id, self.subscription_id
        )
        
    def start_subscription(self):
        """Start listening for messages from the subscription"""
        logger.info(f"Starting subscription to {self.subscription_path}")
        
        # Configure the flow control settings
        flow_control = pubsub_v1.types.FlowControl(max_messages=10)
        
        # Start subscribing
        streaming_pull_future = self.subscriber.subscribe(
            self.subscription_path, 
            callback=self._process_message,
            flow_control=flow_control
        )
        
        # Keep the main thread alive
        try:
            streaming_pull_future.result()
        except Exception as e:
            logger.error(f"Listening for messages on {self.subscription_path} raised an exception: {e}")
            streaming_pull_future.cancel()
            self.subscriber.close()
            
    def _process_message(self, message):
        """Process incoming message from PubSub

        Args:
            message: PubSub message object
        """
        try:
            logger.info(f"Received message: {message.message_id}")
            
            # Parse message data
            data = json.loads(message.data.decode('utf-8'))
            
            # Process the manufacturers batch within app context
            if self.app:
                with self.app.app_context():
                    self._process_within_context(data, message)
            else:
                # Fallback with warning - should not happen in production
                logger.warning("No Flask app provided to subscriber, may cause context issues")
                self._process_within_context(data, message)
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            # Don't acknowledge message so it can be retried
            # This assumes the PubSub subscription has a retry policy set up
            
    def _process_within_context(self, data, message):
        """Process message data within the Flask application context
        
        Args:
            data (dict): Parsed message data
            message: PubSub message object
        """
        # Process the manufacturers batch
        self.manufacturer_service.process_batch(
            transaction_id=data.get('transaction_id'),
            batch_number=data.get('batch_number'),
            manufacturers=data.get('manufacturers', [])
        )
        
        # Acknowledge message after successful processing
        message.ack()
        logger.info(f"Message {message.message_id} acknowledged")