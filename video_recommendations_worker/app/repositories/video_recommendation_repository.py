from datetime import datetime
import uuid
import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.video_recommendation import VideoRecommendation
from app.AI.recommendations_handler import RecommendationsHandler

class VideoRecommendationRepository:
    def __init__(self, session: Session):
        self.session = session
        self.recommendations_handler = RecommendationsHandler()
    
    async def create_recommendation(self, video_id: str, document_id: str, tags: str) -> VideoRecommendation:
        """
        Genera recomendaciones usando IA y guárdalas en la base de datos
        
        Args:
            video_id: ID de la simulación de video
            document_id: ID del documento asociado
            tags: Etiquetas para basar las recomendaciones
            
        Returns:
            Instancia de VideoRecommendation creada
        """
        try:
            # Generar recomendaciones usando IA
            recommendations = await self.recommendations_handler.generate_recommendations(tags)
            
            # Crear y guardar recomendación
            recommendation = VideoRecommendation(
                video_simulation_id=uuid.UUID(video_id),
                document_id=uuid.UUID(document_id),
                recommendations=recommendations
            )
            
            self.session.add(recommendation)
            self.session.commit()
            
            logging.info(f"Recomendación creada para el video {video_id}")
            return recommendation
            
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error al crear recomendación para el video {video_id}: {e}")
            raise
    
    def get_recommendations_by_video_id(self, video_id: str) -> List[VideoRecommendation]:
        """
        Obtiene todas las recomendaciones para un video específico
        
        Args:
            video_id: ID de la simulación de video
            
        Returns:
            Lista de instancias de VideoRecommendation
        """
        try:
            return self.session.query(VideoRecommendation).filter_by(
                video_simulation_id=uuid.UUID(video_id)
            ).all()
        except Exception as e:
            logging.error(f"Error al recuperar recomendaciones para el video {video_id}: {e}")
            return []
    
    def get_recommendation_by_id(self, recommendation_id: str) -> Optional[VideoRecommendation]:
        """
        Obtiene una recomendación específica por ID
        
        Args:
            recommendation_id: ID de la recomendación
            
        Returns:
            Instancia de VideoRecommendation si se encuentra, None en caso contrario
        """
        try:
            return self.session.query(VideoRecommendation).filter_by(
                id=uuid.UUID(recommendation_id)
            ).first()
        except Exception as e:
            logging.error(f"Error al recuperar la recomendación {recommendation_id}: {e}")
            return None

