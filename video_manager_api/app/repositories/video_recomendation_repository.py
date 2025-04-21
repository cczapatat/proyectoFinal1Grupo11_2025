from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from threading import Thread
from app.models.video_simulation import VideoSimulation
from app.models.video_recomendation import VideoRecommendation


class VideoRecomendationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_recommendation(self, video_simulation: VideoSimulation) -> List:
        pass