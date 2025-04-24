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
        self.session : Session = session

    def create_video_simulation(self, video_simulation: VideoSimulationDTO) -> VideoSimulation:
        """
        Crea una nueva simulación de video y la guarda en la base de datos.
        También envía un evento de simulación de video al sistema de pubsub.
        
        Args:
            video_simulation: DTO con los datos del video
            
        Returns:
            Instancia de VideoSimulation creada
        """
        video_data = {k: v for k, v in video_simulation.dict(exclude_unset=True).items() if v is not None}
        video_simulation_instance = VideoSimulation(**video_data)
        self.session.add(video_simulation_instance)
        self.session.commit()
        self.session.refresh(video_simulation_instance)
        # Solo enviar un evento al sistema pubsub si está disponible
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
                logging.warning(f"Error al enviar evento de simulación de video: {e}")
        else:
            logging.info("Omitiendo envío a Pub/Sub en modo de desarrollo")

        return video_simulation_instance

    def get_all_video_simulations(self) -> List[VideoSimulation]:
        """
        Obtiene todas las simulaciones de video.
        
        Returns:
            Lista de instancias de VideoSimulation
        """
        return self.session.query(VideoSimulation).all()
    
    def get_video_simulation_by_id(self, video_simulation_id: str) -> Optional[VideoSimulation]:
        """
        Obtiene una simulación de video por su ID.
        
        Args:
            video_simulation_id: ID de la simulación a buscar
            
        Returns:
            Instancia de VideoSimulation si se encuentra, None en caso contrario
        """
        return self.session.query(VideoSimulation).filter_by(id=uuid.UUID(video_simulation_id)).first()