# Model Trainer
> Project to train the model <br />
> This project loads the data from MongoDB onto Spark, trains the model and serialises it. <br /><br />
> Running this on docker consumes lot of memory on local system. So preferred mode is to run it locally.

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
    mkvirtualenv model_trainer
    ```
    This setups up a new virtualenv called model_trainer. <br />

3. Install the required libraries for this project
    ```shell
    pip3 install -r requirements.txt
    ```

### *Running Code Directly (Non Docker)*

There are 2 ways to run this code. However for running locally, use local server instead of docker (memory constraint).
1. (PREFERRED) - Run local server
    ```
    uvicorn app.controller:app --reload
    ```
2. (NOT PREFERRED) - Run docker version - For building the project :
    ```shell
    docker build -t usrivastava24/model-trainer:latest .
    ```
    
    For deploying the project :
    ```shell
    DEV
    docker run --rm -d -p 5005:8000 --name model-trainer -e ENVIRONMENT_VAR=DEV usrivastava24/model-trainer
    ```

# API Documentation
This project uses OpenAPI specs for API documentation. Refer to ```http://${HOST_IP}:8000/docs``` for details.