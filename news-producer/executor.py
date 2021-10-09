# -*- coding: utf-8 -*-
"""
Description
"""

__version__ = '0.1'
__author__ = 'Utkarsh Srivastava'

import traceback
import logging
import schedule
import time


# Enable logging
from app.actors.newsapi_actor import NewsAPIActor
from app.actors.newsgen_actor import NewsGenActor

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

newsapi = NewsAPIActor()
newsgen = NewsGenActor()

logger.info("STARTING ----->>>>>>> newsgen actor")
logger.info("STARTING ----->>>>>>> newsapi actor")
schedule.every(10).seconds.do(newsgen.execute)
schedule.every().hour.do(newsapi.execute)


while True:
    schedule.run_pending()
    time.sleep(1)
