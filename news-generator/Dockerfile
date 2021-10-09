FROM python:3.9-slim-buster
MAINTAINER Utkarsh Srivastava <utkarshsrivastava.cse@gmail.com>
WORKDIR /
COPY ./requirements.txt /requirements.txt
RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install --trusted-host pypi.python.org --verbose -r requirements.txt
COPY ./app /app
COPY ./resources /resources
COPY ./utils /utils
COPY ./conf /conf
# COPY ./.env /.env
CMD [ "uvicorn", "app.controller:app", "--host", "0.0.0.0", "--port", "8000"]
