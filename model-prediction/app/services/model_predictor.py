# -*- coding: utf-8 -*-
"""
Description
"""

__version__ = '0.1'
__author__ = 'Utkarsh Srivastava'

import traceback
import logging
import numpy as np
from pyspark.sql.types import IntegerType, Row
from pyspark.sql import SparkSession
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer, StringIndexerModel, IndexToString
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Enable logging
from pyspark.sql import SparkSession

from utils.yaml_parser import Config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelPredictor:

    def __init__(self):

        self.mongo_url = Config.get_config_val("properties.mongo.url")
        self.mongo_port = Config.get_config_val("properties.mongo.port")
        self.mongo_username = Config.get_config_val("properties.mongo.username")
        self.mongo_password = Config.get_config_val("properties.mongo.password")

        self.model_location = Config.get_config_val("properties.model.location")
        self.pipeline_location = Config.get_config_val("properties.model.pipeline_location")

        mongo_db_url = "mongodb://" + \
                       self.mongo_username + \
                       ":" + self.mongo_password + \
                       "@" + self.mongo_url + \
                       ":" + str(self.mongo_port) + \
                       "/news_feed.raw_news?authSource=admin"
        self.spark = SparkSession.builder.master("local[*]").appName('PySpark_tutorial') \
            .getOrCreate()

        # .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \

        # self.spark.sparkContext.add

    def predict(self, data: str):
        response = "N/A"
        try:
            pipeline = PipelineModel.load(self.pipeline_location)
            model = LogisticRegressionModel.load(self.model_location)
            data_list = [data]
            row = map(lambda x: Row(x), data_list)

            df = self.spark.createDataFrame(row, ['summary'])

            df_preprocessed = pipeline.transform(df)
            prediction = model.predictRaw(df_preprocessed.head().features)

            # get label value
            labels = {x._java_obj.getOutputCol(): x.labels for x in pipeline.stages if isinstance(x, StringIndexerModel)}
            response = list(labels.values())[0][np.argmax(prediction)]
        except Exception as e:
            response = "Some Error Occurred"
            logger.error(e)
            traceback.print_exc()

        return response
