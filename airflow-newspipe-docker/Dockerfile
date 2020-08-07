FROM ubuntu:18.04
LABEL maintainer="stevenmi - Steven Mi <s0558366@htw-berlin.de>"

# Python
ARG PYTHON_VERSION=3.7

# TFX
ARG TFX_VERSION=0.21.0

# NewsCrawler version
ARG NEWSCRAWLER_VERSION=0.1.2

# Airflow
ARG AIRFLOW_HOME=/airflow
ARG AIRFLOW_VERSION=1.10.9
ARG AIRFLOW_PORT=8080

# NewsCrawler
ARG NEWSCRAWLER_VRSION=0.1.1

# Set enviroment variables
ENV AIRFLOW_HOME=${AIRFLOW_HOME}
ENV LANG=C.UTF-8

# Install python and pip
RUN apt-get update \
    && apt-get install -y \
            git \
            nano \
            python${PYTHON_VERSION} \
            python3-pip \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install python packages
RUN pip3 install --upgrade pip \
    && pip install apache-airflow==${AIRFLOW_VERSION} \
    && pip install NewsCrawler3==${NEWSCRAWLER_VERSION} \
    && pip install SQLAlchemy==1.3.15 \
    && pip install tfx==${TFX_VERSION} \
    && pip install flask-bcrypt

# Setup Airflow
RUN airflow initdb

# Change default settings
RUN sed -i'.orig' 's/dag_dir_list_interval = 300/dag_dir_list_interval = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/job_heartbeat_sec = 5/job_heartbeat_sec = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/scheduler_heartbeat_sec = 5/scheduler_heartbeat_sec = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/dag_default_view = tree/dag_default_view = graph/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/load_examples = True/load_examples = False/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/max_threads = 2/max_threads = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/authenticate = False/authenticate = True\nauth_backend = airflow.contrib.auth.backends.password_auth/g' ${AIRFLOW_HOME}/airflow.cfg


# Apply new config
RUN airflow resetdb --yes \
    && airflow initdb

# Start inside airflow folder
WORKDIR ${AIRFLOW_HOME}

# Copy scripts into container
COPY scripts /scripts

# Create user account
RUN python3 /scripts/create_account.py

# Start Airflow and Scheduler
RUN chmod u+x /scripts/start-airflow.sh
CMD /scripts/start-airflow.sh
