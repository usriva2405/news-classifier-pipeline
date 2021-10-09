# -*- coding: utf-8 -*-
"""
Description
"""

__version__ = '0.1'
__author__ = 'Utkarsh Srivastava'

import json
import string
import traceback
import logging

# Enable logging
from concurrent.futures import thread
from datetime import datetime
from typing import Optional

from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads

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


def json_deserializer(v):
    try:
        return json.loads(v.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        logger.exception('Unable to decode: %s', v)
        return None


class NewsConsumerActor:

    def __init__(self):
        self.kafka_broker_url = Config.get_config_val("properties.kafka.broker_url")
        self.kafka_topic = Config.get_config_val("properties.kafka.topic")
        self.mongo_url = Config.get_config_val("properties.mongo.url")
        self.mongo_port = Config.get_config_val("properties.mongo.port")
        self.mongo_username = Config.get_config_val("properties.mongo.username")
        self.mongo_password = Config.get_config_val("properties.mongo.password")

        self.newsapi_url = Config.get_config_val("properties.external.newsapi_url")
        self.rapidapi_token = Config.get_config_val("properties.external.rapidapi_token")

    def receiveMessage(self):
        try:

            consumer = KafkaConsumer(
                auto_offset_reset='latest',
                bootstrap_servers=[self.kafka_broker_url],
                value_deserializer=json_deserializer
            )
            consumer.subscribe(['news_feed'])

            mongo_db_url = "mongodb://" + \
                           self.mongo_username + \
                           ":" + self.mongo_password + \
                           "@" + self.mongo_url + \
                           ":" + str(self.mongo_port)
            client = MongoClient(mongo_db_url)
            collection = client.news_feed.raw_news

            for message in consumer:
                logger.info("\n\n\n\n CONSUMER ------->>>>>>>")
                logger.info(message.value)
                # logger.info(type(message))
                collection.insert_one(message.value)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()


