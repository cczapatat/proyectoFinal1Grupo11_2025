import os
import threading
import uvicorn
from fastapi import FastAPI
from app.core.db import engine, Base
from app.pubsub.consumer import consume_messages
from app.api.endpoints import router as api_router

app = FastAPI()
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    #thread = threading.Thread(target=consume_messages, daemon=True)
    #thread.start()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)