FROM ubuntu:18.04
LABEL maintainer="stevenmi - Steven Mi <s0558366@htw-berlin.de>"

# RABBITMQ need to be injected
ARG RABBITMQ_USER
ARG RABBITMQ_PASS

# POSTGRES need to be injected
ARG POSTGRES_USER
ARG POSTGRES_PASS

# Python
ARG PYTHON_VERSION=3.6

# NewsCrawler version
ARG NEWSCRAWLER_VERSION=0.1.2

# Airflow
ARG AIRFLOW_HOME=/airflow
ARG AIRFLOW_VERSION=1.10.12
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
    && pip install --upgrade setuptools \
    && pip install apache-airflow==${AIRFLOW_VERSION} \
    && pip install NewsCrawler3==${NEWSCRAWLER_VERSION} \
    && pip install SQLAlchemy==1.3.15 \
    && pip3 install --upgrade six>=1.13.0 \
    && pip install celery==4.3.0 \
    && pip install tfx \
    && pip install flask-bcrypt \ 
    && pip install psycopg2-binary \
    && pip install pyamqp 

# Setup Airflow
RUN airflow initdb

# Change default settings
RUN sed -i'.orig' 's/dag_dir_list_interval = 300/dag_dir_list_interval = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/job_heartbeat_sec = 5/job_heartbeat_sec = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/scheduler_heartbeat_sec = 5/scheduler_heartbeat_sec = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/dag_default_view = tree/dag_default_view = graph/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/load_examples = True/load_examples = False/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/max_threads = 2/max_threads = 4/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/authenticate = False/authenticate = True\nauth_backend = airflow.contrib.auth.backends.password_auth/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' "s|sql_alchemy_conn = sqlite:////airflow/airflow.db|sql_alchemy_conn = postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASS}@postgres:5432/airflow|g" ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' "s|broker_url = sqla+mysql://airflow:airflow@localhost:3306/airflow|broker_url = pyamqp://${RABBITMQ_USER}:${RABBITMQ_PASS}@rabbitmq:5672/|g" ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/executor = SequentialExecutor/executor = CeleryExecutor/g' ${AIRFLOW_HOME}/airflow.cfg 

# Start inside airflow folder
WORKDIR ${AIRFLOW_HOME}

# Copy scripts into container
COPY scripts /scripts

# Start Airflow and Scheduler
RUN chmod u+x /scripts/start-airflow.sh
CMD /scripts/start-airflow.sh