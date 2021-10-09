# -*- coding: utf-8 -*-
"""
Description
"""

__version__ = '0.1'
__author__ = 'Utkarsh Srivastava'

import traceback
import logging
import json
import string
from json import JSONEncoder
import requests

# Enable logging
from kafka import KafkaProducer

from utils.yaml_parser import Config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsGenActor:

    def __init__(self):
        kafka_broker_url = Config.get_config_val("properties.kafka.broker_url")
        self.kafka_topic = Config.get_config_val("properties.kafka.topic")
        self.newsgen_url = Config.get_config_val("properties.external.newsgen_url")
        logger.info(f"NewsGenActor :: URL : {self.newsgen_url}")

        logger.error(kafka_broker_url)
        self.producer = KafkaProducer(
            bootstrap_servers=[kafka_broker_url],
            api_version=(2, 5, 0),
            value_serializer=lambda v: json.dumps(v, default=string).encode('utf-8'))

    def execute(self):
        logger.info("\n\nexecuting ----->>>>>>> newsgen actor\n\n")
        data = self.capture_data(2)
        print(f"newsgen_actor -> {data}")
        self.kafka_producer(data=data)

    def kafka_producer(self, data):
        try:
            if isinstance(data, list):
                for item in data:
                    logger.info(f"sending data : {item}")
                    self.producer.send(self.kafka_topic, value=item)
                    logger.info(f"data sent")
        except Exception as e:
            logger.error(e)
            traceback.print_exc()

    def capture_data(self, n_articles):
        result = None
        try:
            payload = "{\"n_articles\":"+str(n_articles)+"}"
            headers = {'Content-Type': 'application/json'}

            response = requests.request("POST", self.newsgen_url, headers=headers, data=payload)
            result = json.loads(response.text)
            logger.info(result)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            result = None
        return result
