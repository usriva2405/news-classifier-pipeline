# -*- coding: utf-8 -*-
"""
Description
"""

__version__ = '0.1'
__author__ = 'Utkarsh Srivastava'

import traceback
import logging
from pymongo import MongoClient

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

url = "mongodb://root:passw0rd@192.168.18.23:27017"
client = MongoClient(url)
collection = client.news_feed.raw_news
print(collection.find_one())