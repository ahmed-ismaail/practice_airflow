FROM apache/airflow:3.0.4


USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean


USER airflow

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt