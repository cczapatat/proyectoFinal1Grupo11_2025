import pytest
from unittest.mock import patch

@pytest.fixture(scope="module")
def mock_main():
    """Mock the main function of the video recommendations worker."""
    with (
        patch("app.pubsub.consumer.consume_messages") as mock_consume_messages,
        patch("app.core.db.create_tables") as mock_create_tables,
        patch("app.ai.configuration.OpenAIConfig.validate_config") as mock_validate_config
    ):
        mock_consume_messages.return_value = None
        mock_create_tables.return_value = None
        mock_validate_config.return_value = None

        yield {
            "mock_consume_messages": mock_consume_messages,
            "mock_create_tables": mock_create_tables,
            "mock_validate_config": mock_validate_config
        }