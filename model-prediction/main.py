# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from pyspark.sql import SparkSession
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

def print_hi(name):
    # spark = SparkSession.builder.master("spark://192.168.18.23:7077").appName('PySpark_tutorial')
    spark = SparkSession.builder.master("local[*]").appName('PySpark_tutorial')\
        .config("spark.mongodb.input.uri", "mongodb://root:passw0rd@192.168.18.23:27017/news_feed.raw_news?authSource=admin")\
        .config("spark.mongodb.output.uri", "mongodb://root:passw0rd@192.168.18.23:27017/news_feed.raw_news?authSource=admin") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
        .config('job.local.dir', 'file:///resources/') \
        .getOrCreate()
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    df.printSchema()
    print(df.head(4))

    # drop dataframes not relevant
    drop_list = ['author', 'link', 'published_date', 'title']
    data = df.select([column for column in df.columns if column not in drop_list])


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

    lrModel.write().overwrite().save('resources/models/')
    # spark.sparkContext.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
