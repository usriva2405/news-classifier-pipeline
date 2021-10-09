FROM python:3.9-slim-buster
MAINTAINER Utkarsh Srivastava <utkarshsrivastava.cse@gmail.com>
WORKDIR /
COPY ./requirements.txt /requirements.txt
RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install --trusted-host pypi.python.org --verbose -r requirements.txt
RUN apt-get update && apt-get install -y iputils-ping
COPY . /
# COPY ./.env /.env
CMD [ "python3", "executor.py"]
