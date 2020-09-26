#!/bin/bash
sed -i'.orig' 's/dag_dir_list_interval = 300/dag_dir_list_interval = 600/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/job_heartbeat_sec = 5/job_heartbeat_sec = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/scheduler_heartbeat_sec = 5/scheduler_heartbeat_sec = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/dag_default_view = tree/dag_default_view = graph/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/load_examples = True/load_examples = False/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/parallelism = 32/parallelism = 2/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/max_active_runs_per_dag = 16/max_active_runs_per_dag = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/dagbag_import_timeout = 30/dagbag_import_timeout = 600/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/load_examples = True/load_examples = False/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/max_threads = 2/max_threads = 1/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/authenticate = False/authenticate = True\nauth_backend = airflow.contrib.auth.backends.password_auth/g' ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' "s|sql_alchemy_conn = sqlite:////airflow/airflow.db|sql_alchemy_conn = postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASS}@${POSTGRES_IP}:5432/airflow|g" ${AIRFLOW_HOME}/airflow.cfg \
    && sed -i'.orig' 's/executor = SequentialExecutor/executor = LocalExecutor/g' ${AIRFLOW_HOME}/airflow.cfg

airflow resetdb --yes
airflow initdb

python3 /scripts/create_account.py || :

if [ -d "/output/pipelines" ]
then
foldername=$(date +"%d-%m-%Y")

mkdir -p /output/pipelines_backup/$foldername
cp -r /output/pipelines /output/pipelines_backup/$foldername
rm -rf /output/pipelines
fi

rm -rf $AIRFLOW_HOME/airflow-webserver*
airflow webserver -D -w 2
airflow scheduler
