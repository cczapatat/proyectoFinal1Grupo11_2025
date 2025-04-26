import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.orm import Session
from app.repositories.video_recommendation_repository import VideoRecommendationRepository
from app.models.video_recommendation import VideoRecommendation
import uuid

@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_recommendations_handler():
    handler = AsyncMock()
    handler.generate_recommendations = AsyncMock(return_value="Mocked Recommendation")
    return handler

@pytest.fixture
def repository(mock_session, mock_recommendations_handler, monkeypatch):
    repo = VideoRecommendationRepository(mock_session)
    monkeypatch.setattr(repo, 'recommendations_handler', mock_recommendations_handler)
    return repo

@pytest.mark.asyncio
async def test_create_recommendation(repository, mock_session):
    video_id = "123e4567-e89b-12d3-a456-426614174000"
    document_id = "123e4567-e89b-12d3-a456-426614174001"
    tags = "example tags"

    recommendation = await repository.create_recommendation(video_id, document_id, tags)

    assert recommendation.video_simulation_id == uuid.UUID(video_id)
    assert recommendation.document_id == uuid.UUID(document_id)
    assert recommendation.recommendations == "Mocked Recommendation"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_create_recommendation_exception(repository, mock_session):
    video_id = "123e4567-e89b-12d3-a456-426614174000"
    document_id = "123e4567-e89b-12d3-a456-426614174001"
    tags = "example tags"

    mock_session.add.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        await repository.create_recommendation(video_id, document_id, tags)

    mock_session.rollback.assert_called_once()

def test_get_recommendations_by_video_id(repository, mock_session):
    video_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_session.query.return_value.filter_by.return_value.all.return_value = [
        VideoRecommendation(video_simulation_id=uuid.UUID(video_id), document_id=uuid.uuid4(), recommendations="Test")
    ]

    recommendations = repository.get_recommendations_by_video_id(video_id)

    assert len(recommendations) == 1
    assert recommendations[0].video_simulation_id == uuid.UUID(video_id)

def test_get_recommendations_by_video_id_exception(repository, mock_session):
    video_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_session.query.side_effect = Exception("Query error")

    recommendations = repository.get_recommendations_by_video_id(video_id)

    assert recommendations == []

def test_get_recommendation_by_id(repository, mock_session):
    recommendation_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_session.query.return_value.filter_by.return_value.first.return_value = VideoRecommendation(
        id=uuid.UUID(recommendation_id), video_simulation_id=uuid.uuid4(), document_id=uuid.uuid4(), recommendations="Test"
    )

    recommendation = repository.get_recommendation_by_id(recommendation_id)

    assert recommendation.id == uuid.UUID(recommendation_id)

def test_get_recommendation_by_id_exception(repository, mock_session):
    recommendation_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_session.query.side_effect = Exception("Query error")

    recommendation = repository.get_recommendation_by_id(recommendation_id)

    assert recommendation is None