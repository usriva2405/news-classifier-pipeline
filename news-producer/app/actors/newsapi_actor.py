# -*- coding: utf-8 -*-
"""
Description
"""

__version__ = '0.1'
__author__ = 'Utkarsh Srivastava'

import traceback
import logging
import json
import random
import string
from datetime import datetime
from json import JSONEncoder
from typing import Optional

import requests
import redis

# Enable logging
from kafka import KafkaProducer

from utils.yaml_parser import Config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsResponse:
    title: str
    author: Optional[str] = None
    published_date: datetime
    link: Optional[str] = None
    summary: Optional[str] = None
    topic: str

    def __init__(self, title, author, published_date, link, summary, topic):
        self.title = title
        self.author = author
        self.published_date = published_date
        self.link = link
        self.summary = summary
        self.topic = topic


class NewsAPIActor:

    def __init__(self):
        kafka_broker_url = Config.get_config_val("properties.kafka.broker_url")
        self.kafka_topic = Config.get_config_val("properties.kafka.topic")

        self.newsapi_url = Config.get_config_val("properties.external.newsapi_url")
        self.rapidapi_token = Config.get_config_val("properties.external.rapidapi_token")
        logger.info(f"NewsGenActor :: URL : {self.newsapi_url}")

        self.producer = KafkaProducer(
            bootstrap_servers=[kafka_broker_url],
            api_version=(2, 5, 0),
            value_serializer=lambda v: json.dumps(v, default=string).encode('utf-8'))

        redis_host = Config.get_config_val("properties.cache.redis_host")
        redis_port = Config.get_config_val("properties.cache.redis_port")
        redis_user = Config.get_config_val("properties.cache.redis_user")
        redis_password = Config.get_config_val("properties.cache.redis_password")

        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password)

        self.category_map = {
            "news": "IMPACT",
            "sport": "SPORTS",
            "tech": "TECH",
            "world": "WORLD NEWS",
            "finance": "MONEY",
            "politics": "POLITICS",
            "business": "BUSINESS",
            "economics": "MONEY",
            "entertainment": "ENTERTAINMENT",
            "beauty": "STYLE & BEAUTY",
            "gaming": "SPORTS"
        }

        # random parameter is selected for querying.
        self.query_params = ["news", "sport", "tech", "finance", "politics", "business", "economics", "entertainment", "beauty", "gaming", 'earning reports','quarterly results','financial statement', 'silver','gold','commodities', 'real estate', 'GDP','jobs','unemployment','housing','economy', 'global finance','imf','ECB','RMB devaluation','international finance', 'cricket', 'tennis', 'golf', 'artificial intelligence', 'machine learning', 'deep learning', 'facebook', 'google', 'apple', 'yahoo', 'amazon']

    def execute(self):
        logger.info("\n\nexecuting ----->>>>>>> newsapi actor\n\n")
        data = self.capture_data(2)
        self.kafka_producer(data=data)

    def kafka_producer(self, data):
        try:
            if isinstance(data, list):
                for item in data:
                    logger.info(f"sending data : {item}")
                    self.producer.send(self.kafka_topic, value=item)
                    logger.info(f"data sent")
        except Exception as e:
            traceback.print_exc()

    def capture_data(self, n_articles):
        data_list = []
        try:
            querystring = {"q": random.choice(self.query_params), "lang": "en", "page_size": n_articles}
            headers = {
                'x-rapidapi-host': "free-news.p.rapidapi.com",
                'x-rapidapi-key': self.rapidapi_token
            }

            response = requests.request("GET", self.newsapi_url, headers=headers, params=querystring)
            result = json.loads(response.text)
            if result is not None and result['articles'] is not None and len(result['articles']) > 0:
                items = result['articles']
                for item in items:
                    formatted_item = NewsResponse(
                        title=item['title'],
                        author=item['author'],
                        published_date=item['published_date'],
                        link=item['link'],
                        summary=item['summary'],
                        topic=self.category_map[item['topic']]
                    )

                    # logger.info(vars(formatted_item))
                    data_list.append(vars(formatted_item))
                    self.redis.mset({"last_aggregation": str(vars(formatted_item))})
                    # logger.info("")
        except Exception as e:
            traceback.print_exc()
            data_list = []
        return data_list
