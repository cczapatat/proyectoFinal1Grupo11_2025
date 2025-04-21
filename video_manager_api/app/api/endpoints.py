from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime
from app.uow.unit_of_work import UnitOfWork
from app.core.db import SessionLocal
from app.models.video_simulation import VideoSimulation
from app.dtos.video_simulation_dto import VideoSimulationDTO
from app.repositories.video_simulation_repository import VideoSimulationRepository

# Pydantic response models
class VideoSimulationResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    file_path: str
    tags: Optional[str] = None
    enabled: bool
    update_date: datetime
    creation_date: datetime
    
    class Config:
        orm_mode = True

class VideoSimulationListResponse(BaseModel):
    mensaje: str
    cantidad: int
    videos: List[VideoSimulationResponse]

class VideoSimulationCreateResponse(BaseModel):
    mensaje: str
    resultado: VideoSimulationResponse

router = APIRouter()

@router.get("/video/health")
def health_check():
    return {"estado": "ok"}

@router.post("/video/create", response_model=VideoSimulationCreateResponse)
def create_video_simulation(request: VideoSimulationDTO):
    try:
        with UnitOfWork() as uow:
            repo = VideoSimulationRepository(uow.session)
            resultado = repo.create_video_simulation(request)
        return {"mensaje": "Actualización procesada", "resultado": resultado}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@router.post("/video/get_all", response_model=VideoSimulationListResponse)
async def get_all_video_simulations():   
    session = SessionLocal()
    try:
        repo = VideoSimulationRepository(session)
        video_simulations = repo.get_all_video_simulations()
        return {"mensaje": "Productos cargados exitosamente", "cantidad": len(video_simulations), "videos": video_simulations}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    finally:
        session.close()

@router.post("/video/get", response_model=VideoSimulationResponse)
def get_video_simulation_by_id(video_simulation_id: str):
    session = SessionLocal()
    try:
        repo = VideoSimulationRepository(session)
        video_simulation = repo.get_video_simulation_by_id(video_simulation_id)
        if not video_simulation:
            raise HTTPException(status_code=404, detail="Video simulation not found")
        return video_simulation
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    finally:
        session.close()

@router.put("/video/update", response_model=VideoSimulationCreateResponse)
def update_video_simulation(video_simulation_id: str, request: VideoSimulationDTO):
    session = SessionLocal()
    try:
        repo = VideoSimulationRepository(session)
        video_simulation = repo.get_video_simulation_by_id(video_simulation_id)
        if not video_simulation:
            raise HTTPException(status_code=404, detail="Video simulation not found")
        updated_video_simulation = repo.update_video_simulation(video_simulation_id, request)
        session.commit()
        return {"mensaje": "Video simulation updated successfully", "resultado": updated_video_simulation}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    finally:
        session.close()