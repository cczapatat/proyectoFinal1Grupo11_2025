import os
import threading
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List
from app.core.db import engine, Base
from app.pubsub.consumer import consume_messages
from app.uow.unit_of_work import UnitOfWork
from app.repositories.stock_repository import StockRepository
from app.dtos.product_update_dto import ProductUpdateDTO

project_id = os.environ.get('GCP_PROJECT_ID', 'proyectofinalmiso2025')
stock_update_subscription_id = os.environ.get('GCP_STOCKS_SUB', 'commands_to_stock-sub')
stock_update_name_pub = os.environ.get('GCP_STOCKS_TOPIC', 'commands_to_stock')

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    thread = threading.Thread(target=consume_messages, daemon=True)
    thread.start()

@app.get("/health")
def health_check():
    return {"estado": "ok"}

@app.post("/update_stock_test")
def update_stock_test(request: List[ProductUpdateDTO]):
    try:
        with UnitOfWork() as uow:
            repo = StockRepository(uow.session)
            resultado = repo.update_stocks(request)
        return {"mensaje": "Actualización procesada", "resultado": resultado}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)