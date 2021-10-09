from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.services.model_predictor import ModelPredictor
from app.services.model_trainer import ModelTrainer

app = FastAPI()
model_trainer = ModelTrainer()
model_predictor = ModelPredictor()

class NewsArticle(BaseModel):
    summary: str
    topic: Optional[str] = None

@app.get("/retrain")
async def retrain_model():
    print("starting model retraining")
    return model_trainer.retrain_model()