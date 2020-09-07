#!/bin/bash
airflow resetdb --yes
airflow initdb

python3 /scripts/create_account.py

if [ -d "/output/pipelines" ]
then

foldername=$(date +"%d-%m-%Y")

mkdir -p /output/pipelines_backup/$foldername
cp -r /output/pipelines /output/pipelines_backup/$foldername
rm -rf /output/pipelines
fi

rm $AIRFLOW_HOME/airflow-webserver*
airflow webserver -D
airflow scheduler
