from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from app.dtos.product_update_dto import ProductUpdateDTO
from app.utilities.bulk_processor import process_bulk_file
from app.uow.unit_of_work import UnitOfWork
from app.repositories.stock_repository import StockRepository
from app.core.db import SessionLocal
from app.models.stock import Stock

router = APIRouter()

'''
Los endpoints expuestos en este archivo son utilitiarios para probar la funcionalidad de actualización de stock
y realizar una carga masiva de productos en stock inicial.
'''

@router.get("/health")
def health_check():
    return {"estado": "ok"}

@router.post("/update_stock_test")
def update_stock_test(request: List[ProductUpdateDTO]):
    try:
        with UnitOfWork() as uow:
            repo = StockRepository(uow.session)
            resultado = repo.update_stocks(request)
        return {"mensaje": "Actualización procesada", "resultado": resultado}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@router.post("/upload_bulk")
async def upload_bulk(file: UploadFile = File(...)):
    file_bytes = await file.read()
    products_data = process_bulk_file(file_bytes)
    session = SessionLocal()
    try:
        stocks = [Stock(**data) for data in products_data]
        session.bulk_save_objects(stocks)
        session.commit()
        return {"mensaje": "Productos cargados exitosamente", "cantidad": len(stocks)}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    finally:
        session.close()

@router.post("/reset")
def reset():
    session = SessionLocal()
    try:
        session.execute("TRUNCATE TABLE stocks RESTART IDENTITY CASCADE;")
        session.execute("TRUNCATE TABLE update_stock_attempts RESTART IDENTITY CASCADE;")
        session.commit()
        return {"mensaje": "Tablas reseteadas exitosamente"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    finally:
        session.close()