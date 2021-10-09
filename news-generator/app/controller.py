from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import numpy as np
import json

app = FastAPI()
news = pd.read_json("../resources/news_data_v2.json", lines=True)


class NewsRequest(BaseModel):

    n_articles: int = 5
    category: Optional[str] = None


class NewsResponse(BaseModel):
    title: str
    author: Optional[str] = None
    published_date: datetime
    link: Optional[str] = None
    summary: Optional[str] = None
    topic: str


class NewsCategories(BaseModel):
    categories: list


@app.post("/getnewsfeed", response_model=list[NewsResponse])
async def read_root(news_request: NewsRequest):
    temp_data = None
    news_data = news.copy(deep=True)
    if news_request.category is not None and news_request.category != "":
        news_data = news_data[news_data['category'] == news_request.category]
    print(news_request)
    if news_data is not None and news_data.shape[0] != 0:
        if news_request.n_articles is not None and news_request.n_articles > 0 :
            temp_data = news_data.sample(news_request.n_articles)
        else:
            temp_data = news_data.sample(news_request.n_articles)
        temp_data = temp_data.sort_values(by="date")
    else:
        temp_data = None
    temp_data.rename(columns={'headline': 'title', 'authors': 'author', 'link': 'link', 'short_description': 'summary', 'date': 'published_date', 'category': 'topic'}, inplace=True)

    readings = [NewsResponse(**kwargs) for kwargs in temp_data.to_dict(orient='records')]
    return readings


@app.get("/getcategories")
async def read_item():
    print(type(news['category'].unique().tolist()))
    categories = news['category'].unique().tolist()
    news_categories = NewsCategories(categories=categories)
    print(news_categories)
    return news_categories
