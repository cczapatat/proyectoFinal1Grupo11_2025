import os
import logging

logger = logging.getLogger(__name__)

# Path to migration files
migrations_path = os.path.dirname(os.path.abspath(__file__))