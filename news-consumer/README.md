# News Consumer
> Project to consume news from multiple resources <br />
> This project consumes from the kafka queue and pushes the data to MongoDB

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

### *Running Code Directly (Non Docker)*

There are 2 ways to run this code
1. Run local server
    ```
    python3 executor.py
    ```
2. Run docker version - For building the project :
    ```shell
    docker build -t usrivastava24/news-consumer:latest .
    ```
    
    For deploying the project :
    ```shell
    DEV
    docker run --rm -d --name news-consumer \
        -e ENVIRONMENT_VAR=DEV \
        -e KAFKA_BROKER_URL=${HOST_IP}:9092 \
        -e MONGO_URL=${HOST_IP} \
        -e MONGO_PORT=27017 \
        -e MONGO_USERNAME=root \
        -e MONGO_PASSWORD=passw0rd \
    usrivastava24/news-consumer; docker logs -f news-consumer;
    ```
   