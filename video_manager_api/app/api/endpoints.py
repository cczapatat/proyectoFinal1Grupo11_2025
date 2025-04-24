from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from app.dtos.video_simulation_responses import VideoSimulationCreateResponse, VideoSimulationListResponse, VideoSimulationResponse
from pydantic import BaseModel
import uuid
from datetime import datetime
from app.uow.unit_of_work import UnitOfWork
from app.core.db import SessionLocal
from app.models.video_simulation import VideoSimulation
from app.dtos.video_simulation_dto import VideoSimulationDTO
from app.repositories.video_simulation_repository import VideoSimulationRepository


router = APIRouter()

@router.get("/video/health")
def health_check():
    return {"estado": "ok"}

@router.post("/video/create", response_model=VideoSimulationCreateResponse)
def create_video_simulation(request: VideoSimulationDTO):
    try:
        with UnitOfWork() as uow:
            repo = VideoSimulationRepository(uow.session)
            # El id se generará automáticamente si no se proporciona
            resultado = repo.create_video_simulation(request)
            # Convertir a modelo Pydantic mientras la sesión está abierta
            response_data = VideoSimulationResponse.from_orm(resultado)
        return {"mensaje": "Información de video cargada correctamente", "resultado": response_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@router.get("/video/get_all", response_model=VideoSimulationListResponse)
async def get_all_video_simulations():   
    session = SessionLocal()
    try:
        repo = VideoSimulationRepository(session)
        video_simulations = repo.get_all_video_simulations()
        # Convertir a modelos Pydantic mientras la sesión está abierta
        response_videos = [VideoSimulationResponse.from_orm(v) for v in video_simulations]
        return {"mensaje": "Videos cargados en sistema", "cantidad": len(response_videos), "videos": response_videos}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    finally:
        session.close()

@router.get("/video/get_by_id", response_model=VideoSimulationResponse)
def get_video_simulation_by_id(video_simulation_id: str):
    session = SessionLocal()
    try:
        repo = VideoSimulationRepository(session)
        video_simulation = repo.get_video_simulation_by_id(video_simulation_id)
        if not video_simulation:
            raise HTTPException(status_code=404, detail="Simulación de video no encontrada")
        # Convertir a modelo Pydantic antes de cerrar la sesión
        response_data = VideoSimulationResponse.from_orm(video_simulation)
        return response_data
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    finally:
        session.close()