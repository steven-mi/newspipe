FROM ubuntu:18.04
LABEL maintainer="stevenmi - Steven Mi <s0558366@htw-berlin.de>"

# POSTGRES need to be injected
ARG POSTGRES_USER
ARG POSTGRES_PASS
ARG POSTGRES_IP

# Python
ARG PYTHON_VERSION=3.6

# TFX Version
ARG TENSORFLOW_VERSION=1.15.0
ARG TFX_VERSION=0.15.0

# NewsCrawler version
ARG NEWSCRAWLER_VERSION=0.1.9

# Airflow
ARG AIRFLOW_HOME=/airflow
ARG AIRFLOW_VERSION=1.10.12
ARG AIRFLOW_PORT=8080

# Set enviroment variables
ENV AIRFLOW_HOME=${AIRFLOW_HOME}
ENV LANG=C.UTF-8
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASS=${POSTGRES_PASS}
ENV POSTGRES_IP=${POSTGRES_IP}

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
RUN pip3 install --upgrade pip==19.2 \
    && pip install --upgrade setuptools==46.1.3 \
    && pip install apache-airflow==${AIRFLOW_VERSION} \
    && pip install NewsCrawler3==${NEWSCRAWLER_VERSION} \
    && pip install tensorflow==${TENSORFLOW_VERSION} \
    && pip install tensorflow-serving-api==${TENSORFLOW_VERSION} \
    && pip install tfx==${TFX_VERSION} \
    && pip install SQLAlchemy==1.3.15 \
    && pip install --upgrade six==1.13.0 \
    && pip install flask-bcrypt \
    && pip install psycopg2-binary \
    && pip install pyarrow==0.14.0

# Setup Airflow
RUN airflow initdb

# Change default settings
#RUN sed -i'.orig' 's/dag_dir_list_interval = 300/dag_dir_list_interval = 600/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/job_heartbeat_sec = 5/job_heartbeat_sec = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/scheduler_heartbeat_sec = 5/scheduler_heartbeat_sec = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/dag_default_view = tree/dag_default_view = graph/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/load_examples = True/load_examples = False/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/parallelism = 32/parallelism = 2/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/max_active_runs_per_dag = 16/max_active_runs_per_dag = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/dagbag_import_timeout = 30/dagbag_import_timeout = 600/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/load_examples = True/load_examples = False/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/max_threads = 2/max_threads = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/authenticate = False/authenticate = True\nauth_backend = airflow.contrib.auth.backends.password_auth/g' ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' "s|sql_alchemy_conn = sqlite:////airflow/airflow.db|sql_alchemy_conn = postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASS}@${POSTGRES_IP}:5432/airflow|g" ${AIRFLOW_HOME}/airflow.cfg \
#    && sed -i'.orig' 's/executor = SequentialExecutor/executor = LocalExecutor/g' ${AIRFLOW_HOME}/airflow.cfg
#RUN cat /airflow/airflow.cfg | grep sql_alchemy_conn

# Start inside airflow folder
WORKDIR ${AIRFLOW_HOME}

# Copy scripts into container
COPY scripts /scripts

# Start Airflow and Scheduler
RUN chmod u+x /scripts/startup.sh
CMD /scripts/startup.sh
