#!/bin/bash
airflow resetdb --yes
airflow initdb

python3 /scripts/create_account.py

if [ -d "/output/pipelines" ]
then
mkdir /output/pipelines_backup/$(date +"%d-%m-%Y")
cp -r /output/pipelines /output/pipelines_backup/$(date +"%d-%m-%Y")
rm -rf /output/pipelines
fi

airflow webserver