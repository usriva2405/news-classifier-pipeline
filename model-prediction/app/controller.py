from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.services.model_predictor import ModelPredictor

app = FastAPI()
model_predictor = ModelPredictor()

class NewsArticle(BaseModel):
    summary: str
    topic: Optional[str] = None


@app.post("/predict", response_model=str)
async def predict(news_article: NewsArticle):
    response = ""
    if news_article.summary is not None and news_article.summary != "":
        response = model_predictor.predict(news_article.summary)
    else:
        response = "failure"
    return response
