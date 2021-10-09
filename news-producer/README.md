# News Producer
> Project to consumer news from multiple resources <br />

## Installing / Getting started

This is a python project, and should run fine on version >= 3. 
1. Install python 3.x
2. Create a virtual environment for python

    ```shell
    pip3 install virtualenv
    mkdir ~/.virtualenvs
    
    pip3 install virtualenvwrapper
    
    # Add following to bash_profile
    export WORKON_HOME=$HOME/.virtualenvs
    export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
    export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
    source ~/.bash_profile
    
    source /usr/local/bin/virtualenvwrapper.sh
    
    workon
    mkvirtualenv news_consumer
    ```
    This setups up a new virtualenv called news_consumer. <br />

3. Install the required libraries for this project
    ```shell
    pip3 install -r requirements.txt
    ```

# Dependencies

### ZOOKEEPER
#### Start Zookeeper
```
./bin/zkServer.sh start conf/zoo_sample.cfg
```

#### Stop Zookeeper
```
./bin/zkServer.sh stop conf/zoo_sample.cfg
```

### KAFKA MQ
https://www.tutorialspoint.com/apache_kafka/apache_kafka_fundamentals.htm
#### Start kafka
```
sudo ./bin/kafka-server-start.sh config/server.properties \
--override delete.topic.enable=true
```
Use this override if you need to change log directories
```
--override log.dirs=/tmp/kafka-logs-100
```

Use this override if you need to change broker id
```
--override broker.id=100
```

#### Creating topic
```
./bin/kafka-topics.sh --zookeeper localhost:2181 \
--create \
--replication-factor 1 \
--partitions 1 \
--topic news_feed
```

#### List Topics
```
./bin/kafka-topics.sh --zookeeper localhost:2181 --list
```

#### Describe Topics
```
./bin/kafka-topics.sh --zookeeper localhost:2181 --describe --topic news_feed
```

#### Deleting Topics
https://jaceklaskowski.gitbooks.io/apache-kafka/content/kafka-topic-deletion.html
```
./bin/kafka-topics.sh --delete --zookeeper localhost:2181  --topic acquiring_transaction_replica3

### *Running Code Directly (Non Docker)*

There are 2 ways to run this code
1. Run local server
    ```
    python3 executor.py
    ```
2. Run docker version - For building the project :
    ```shell
    docker build -t usrivastava24/news-producer:latest .
    ```
    
    For deploying the project :
    ```shell
    DEV
    docker run --rm -d --name news-producer \
        -e ENVIRONMENT_VAR=DEV \
        -e KAFKA_BROKER_URL=${HOST_ID}:9092 \
    usrivastava24/news-producer; docker logs -f news-producer;
    ```
