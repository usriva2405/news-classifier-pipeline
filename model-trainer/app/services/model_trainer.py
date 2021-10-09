# -*- coding: utf-8 -*-
"""
Description
"""

__version__ = '0.1'
__author__ = 'Utkarsh Srivastava'

import traceback
import logging
from pyspark.sql import SparkSession
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Enable logging

from utils.yaml_parser import Config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:

    def __init__(self):
        # use this in case of spark cluster is used
        # spark = SparkSession.builder.master("spark://192.168.18.23:7077").appName('PySpark_tutorial') \

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
            .config("spark.mongodb.input.uri", mongo_db_url) \
            .config("spark.mongodb.output.uri", mongo_db_url) \
            .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
            .getOrCreate()

        # .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
        # .config('spark.jars', 'file:///resources/jars/mongo-spark-connector_2.12-3.0.1.jar') \

        # .config('job.local.dir', 'file:///resources/') \

    """
    retrain a model and persist it to a location
    """
    def retrain_model(self):

        df = self.spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
        df.printSchema()
        print(df.head(4))

        # drop dataframes not relevant
        drop_list = ['author', 'link', 'published_date', 'title', '_id']
        data = df.select([column for column in df.columns if column not in drop_list])
        print(data)

        # regular expression tokenizer
        regexTokenizer = RegexTokenizer(inputCol="summary", outputCol="words", pattern="\\W")
        # stop words
        add_stopwords = ["http", "https", "amp", "rt", "t", "c", "the"]
        stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)
        # bag of words count
        countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)

        label_stringIdx = StringIndexer(inputCol="topic", outputCol="label")
        pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx])
        # Fit the pipeline to training documents.
        pipelineFit = pipeline.fit(data)
        dataset = pipelineFit.transform(data)
        dataset.show(5)

        # set seed for reproducibility
        (trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed=100)
        print("Training Dataset Count: " + str(trainingData.count()))
        print("Test Dataset Count: " + str(testData.count()))

        lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
        lrModel = lr.fit(trainingData)
        predictions = lrModel.transform(testData)
        predictions.filter(predictions['prediction'] == 0) \
            .select("summary", "topic", "probability", "label", "prediction") \
            .orderBy("probability", ascending=False) \
            .show(n=10, truncate=30)

        evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
        evaluator.evaluate(predictions)

        pipeline = Pipeline(stages=[])

        pipelineFit.write().overwrite().save(self.pipeline_location)
        lrModel.write().overwrite().save(self.model_location)
        return "model retrained successfully"
