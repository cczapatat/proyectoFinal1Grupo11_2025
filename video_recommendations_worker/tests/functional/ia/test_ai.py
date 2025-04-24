import asyncio
import pytest
from unittest.mock import patch, MagicMock
from app.ai.configuration import OpenAIConfig
from app.ai.recommendations_handler import RecommendationsHandler

def test_validate_config_valid():
    with patch("app.ai.configuration.OpenAIConfig.validate_config") as mock_validate_config:
        mock_validate_config.return_value = None
        try:
            OpenAIConfig.validate_config()
        except ValueError:
            pytest.fail("validate_config raised ValueError unexpectedly!")

def test_validate_config_invalid():
    with patch("app.ai.configuration.OpenAIConfig.validate_config") as mock_validate_config:
        mock_validate_config.side_effect = ValueError("OpenAI API key is not set")
        with pytest.raises(ValueError, match="OpenAI API key is not set"):
            OpenAIConfig.validate_config()

@pytest.fixture
def mock_openai_client():
    with patch("app.ai.recommendations_handler.OpenAI") as mock_client:
        yield mock_client

def test_recommendations_handler_initialization(mock_openai_client):
    handler = RecommendationsHandler()
    assert handler.client == mock_openai_client.return_value
    assert handler.prompt_template is not None

def test_generate_recommendations_success(mock_openai_client):
    handler = RecommendationsHandler()
    mock_openai_client.return_value.chat.completions.create.return_value = MagicMock(
        choices=[
            MagicMock(message=MagicMock(content="Recomendación generada exitosamente."))
        ]
    )

    result = asyncio.run(handler.generate_recommendations("etiqueta1, etiqueta2"))
    assert result == "Recomendación generada exitosamente."
    mock_openai_client.return_value.chat.completions.create.assert_called_once()

def test_generate_recommendations_failure(mock_openai_client):
    handler = RecommendationsHandler()
    mock_openai_client.return_value.chat.completions.create.side_effect = Exception("Error de OpenAI")

    with pytest.raises(Exception, match="Error de OpenAI"):
        asyncio.run(handler.generate_recommendations("etiqueta1, etiqueta2"))

