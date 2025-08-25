FROM apache/airflow:3.0.4


USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean


USER airflow