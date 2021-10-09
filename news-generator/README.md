# News Generator
> Project to generate random news <br />
> This project generates news from a corpus of news, and exposes an API to consumer this

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
    mkvirtualenv news_generator
    ```
    This setups up a new virtualenv called news_generator. <br />

3. Install the required libraries for this project
    ```shell
    pip3 install -r requirements.txt
    ```

### *Running Code Directly (Non Docker)*

There are 2 ways to run this code
1. Run local server
    ```
    uvicorn app.controller:app --reload
    ```
2. Run docker version - For building the project :
    ```shell
    docker build -t usrivastava24/news-generator:latest .
    ```
    
    For deploying the project :
    ```shell
    DEV
    docker run --rm -d -p 5002:8000 --name news-generator -e ENVIRONMENT_VAR=DEV usrivastava24/news-generator
    ```
   
# API Documentation
This project implements OpenAPI specs <br /> 

Refer to http://${HOST_API}:5002/docs to check all API specs
