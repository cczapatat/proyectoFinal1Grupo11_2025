from threading import Thread
from typing import List, Dict, Any, Optional, Union
import logging
import uuid
from sqlalchemy.orm import Session
from app.dtos.video_simulation_dto import VideoSimulationDTO
from app.models.video_simulation import VideoSimulation
from app.pubsub.publisher import dispatch_video_simulation_event, pubsub_publisher_available


class VideoSimulationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_video_simulation(self, video_simulation: VideoSimulationDTO) -> VideoSimulation:
        video_simulation_instance = VideoSimulation(**video_simulation.dict())
        self.session.add(video_simulation_instance)
        self.session.commit()
        # Only dispatch an event to the pubsub system if it's available
        if pubsub_publisher_available:
            try:
                dispatch_thread = Thread(
                    target=dispatch_video_simulation_event,
                    args=(
                        str(video_simulation_instance.id), 
                        str(video_simulation_instance.document_id), 
                        video_simulation_instance.file_path,
                        video_simulation_instance.enabled, 
                        video_simulation_instance.tags)
                )
                dispatch_thread.start()
            except Exception as e:
                logging.warning(f"Failed to dispatch video simulation event: {e}")
        else:
            logging.info("Skipping Pub/Sub dispatch in development mode")

        return video_simulation_instance


    def update_video_simulation(self, video_simulation_id: str, video_simulation: VideoSimulationDTO) -> VideoSimulation:
        video_simulation_instance = self.session.query(VideoSimulation).filter_by(id=uuid.UUID(video_simulation_id)).first()
        if not video_simulation_instance:
            return None
        for key, value in video_simulation.dict().items():
            setattr(video_simulation_instance, key, value)
        self.session.commit()
        return video_simulation_instance
    def get_all_video_simulations(self) -> List[VideoSimulation]:
        return self.session.query(VideoSimulation).all()
    
    def get_video_simulation_by_id(self, video_simulation_id: str) -> Optional[VideoSimulation]:
        return self.session.query(VideoSimulation).filter_by(id=uuid.UUID(video_simulation_id)).first()
