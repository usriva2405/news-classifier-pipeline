FROM python:3.9-slim-buster
MAINTAINER Utkarsh Srivastava <utkarshsrivastava.cse@gmail.com>
WORKDIR /
COPY ./requirements.txt /requirements.txt

# install packages

RUN apt-get update

RUN apt-get install -y apt-utils build-essential gcc

ENV JAVA_FOLDER jdk-10

ENV JVM_ROOT /usr/lib/jvm

ENV JAVA_PKG_NAME openjdk-10+44_linux-x64_bin_ri.tar.gz
ENV JAVA_TAR_GZ_URL https://download.java.net/openjdk/jdk10/ri/$JAVA_PKG_NAME

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*    && \
    apt-get clean                                                               && \
    apt-get autoremove                                                          && \
    echo Downloading $JAVA_TAR_GZ_URL                                           && \
    wget -q $JAVA_TAR_GZ_URL                                                    && \
    tar -xvf $JAVA_PKG_NAME                                                     && \
    rm $JAVA_PKG_NAME                                                           && \
    mkdir -p /usr/lib/jvm                                                       && \
    mv ./$JAVA_FOLDER $JVM_ROOT                                                 && \
    update-alternatives --install /usr/bin/java java $JVM_ROOT/$JAVA_FOLDER/bin/java 1        && \
    update-alternatives --install /usr/bin/javac javac $JVM_ROOT/$JAVA_FOLDER/bin/javac 1     && \
    java -version

RUN update-ca-certificates -f

RUN pip3 install --upgrade pip
RUN pip3 install --trusted-host pypi.python.org --verbose -r requirements.txt
RUN wget https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/3.0.1/mongo-spark-connector_2.12-3.0.1.jar


COPY ./app /app
COPY ./resources /resources
COPY ./utils /utils
COPY ./conf /conf
# COPY ./.env /.env
CMD [ "uvicorn", "app.controller:app", "--host", "0.0.0.0", "--port", "8000"]
